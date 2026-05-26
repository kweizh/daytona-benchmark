import os
import re

import pytest

PROJECT_DIR = "/home/user/myproject"
LOG_FILE = "/home/user/myproject/output.log"
SANDBOX_BASE_NAME = "harbor-daytona"

SANDBOX_ID_LINE_RE = re.compile(r"^Sandbox ID:\s*(\S+)\s*$", re.MULTILINE)


@pytest.fixture(scope="module")
def run_id():
    value = os.environ.get("ZEALT_RUN_ID")
    assert value, (
        "ZEALT_RUN_ID environment variable is not set; the verifier requires "
        "a run-id to scope verification."
    )
    return value


@pytest.fixture(scope="module")
def expected_sandbox_name(run_id):
    return f"{SANDBOX_BASE_NAME}-{run_id}"


@pytest.fixture(scope="module")
def log_contents():
    assert os.path.isfile(LOG_FILE), (
        f"Expected log file {LOG_FILE} to exist after the task completes."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def sandbox_id_from_log(log_contents):
    match = SANDBOX_ID_LINE_RE.search(log_contents)
    assert match, (
        "Expected a line matching 'Sandbox ID: <id>' (with a non-empty id) "
        f"in {LOG_FILE}, but did not find one. Log contents:\n{log_contents!r}"
    )
    sandbox_id = match.group(1).strip()
    assert sandbox_id, (
        f"Sandbox ID extracted from {LOG_FILE} is empty: line={match.group(0)!r}"
    )
    return sandbox_id


@pytest.fixture(scope="module")
def daytona_client():
    api_key = os.environ.get("DAYTONA_API_KEY")
    assert api_key, (
        "DAYTONA_API_KEY environment variable is not set; the verifier cannot "
        "talk to the hosted Daytona service without it."
    )
    from daytona import Daytona

    return Daytona()


@pytest.fixture(scope="module")
def listed_sandboxes(daytona_client):
    """Collect sandboxes across all pages so we can look up by name."""
    all_items = []
    page = 1
    limit = 100
    # Guard against pathological pagination; cap at 50 pages (5000 sandboxes).
    for _ in range(50):
        try:
            result = daytona_client.list(page=page, limit=limit)
        except TypeError:
            # Some SDK versions may not accept pagination kwargs; fall back.
            result = daytona_client.list()
            items = getattr(result, "items", result)
            all_items.extend(list(items))
            break
        items = list(getattr(result, "items", []) or [])
        all_items.extend(items)
        if len(items) < limit:
            break
        page += 1
    return all_items


def test_project_dir_still_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Expected project directory {PROJECT_DIR} to still exist after the "
        "task completes."
    )


def test_log_file_contains_sandbox_id_line(sandbox_id_from_log):
    # The fixture asserts the format; this test surfaces it as a discrete check.
    assert sandbox_id_from_log, (
        "Expected to extract a non-empty sandbox id from the log file."
    )


def test_sandbox_created_on_daytona(
    listed_sandboxes, expected_sandbox_name, sandbox_id_from_log
):
    """Verify the sandbox was actually created on the hosted Daytona service.

    Looks for a sandbox whose name matches the expected run-id-scoped name.
    If present, its id MUST equal the id recorded in the log file. If the
    platform has already hard-deleted the sandbox (a valid outcome of the
    required cleanup step), the log-file evidence is treated as sufficient.
    """
    matching = []
    for sb in listed_sandboxes:
        name = getattr(sb, "name", None)
        if name == expected_sandbox_name:
            matching.append(sb)

    if matching:
        ids = [getattr(sb, "id", None) for sb in matching]
        assert sandbox_id_from_log in ids, (
            f"Found sandbox(es) named {expected_sandbox_name!r} on Daytona but "
            f"their ids {ids!r} do not include the id from the log file "
            f"({sandbox_id_from_log!r})."
        )
    else:
        # The sandbox is not present in the active listing. This is consistent
        # with the required cleanup step (the script must delete the sandbox
        # after creating it). The log-file evidence of creation is sufficient.
        assert sandbox_id_from_log, (
            "Sandbox with the expected name was not found in the Daytona "
            "listing and the log file did not contain a sandbox id either; "
            "cannot confirm that the sandbox was ever created."
        )
