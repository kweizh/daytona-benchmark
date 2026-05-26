import json
import os
import re
import subprocess

import pytest

LOG_FILE = "/home/user/myproject/output.log"
LOG_LINE_RE = re.compile(r"^Sandbox ID:\s+(?P<id>[A-Za-z0-9_-]+)\s*$", re.MULTILINE)


@pytest.fixture(scope="session")
def run_id():
    value = os.environ.get("ZEALT_RUN_ID")
    assert value, "ZEALT_RUN_ID environment variable must be set for verification."
    return value


@pytest.fixture(scope="session")
def expected_sandbox_name(run_id):
    return f"sb-{run_id}"


@pytest.fixture(scope="session")
def daytona_login():
    api_key = os.environ.get("DAYTONA_API_KEY")
    assert api_key, "DAYTONA_API_KEY environment variable must be set for verification."
    result = subprocess.run(
        ["daytona", "login", "--api-key", api_key],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"'daytona login' failed (exit {result.returncode}): "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    return True


@pytest.fixture(scope="session")
def logged_sandbox_id():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    match = LOG_LINE_RE.search(content)
    assert match, (
        f"Log file {LOG_FILE} does not contain a line matching "
        f"'Sandbox ID: <id>'. Actual content: {content!r}"
    )
    return match.group("id")


@pytest.fixture(scope="session")
def sandbox_list(daytona_login):
    result = subprocess.run(
        ["daytona", "list", "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"'daytona list --format json' failed (exit {result.returncode}): "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"'daytona list --format json' output is not valid JSON: {exc}. "
            f"stdout={result.stdout!r}"
        )
    assert isinstance(data, list), (
        f"Expected 'daytona list --format json' to return a JSON array, "
        f"got: {type(data).__name__} -- {result.stdout!r}"
    )
    return data


def _extract_name(entry):
    for key in ("name", "Name"):
        if key in entry and entry[key]:
            return entry[key]
    labels = entry.get("labels") or entry.get("Labels") or {}
    if isinstance(labels, dict):
        for key in ("name", "Name"):
            if key in labels and labels[key]:
                return labels[key]
    return None


def _extract_id(entry):
    for key in ("id", "Id", "ID"):
        if key in entry and entry[key]:
            return entry[key]
    return None


def test_log_file_contains_sandbox_id_line(logged_sandbox_id):
    assert logged_sandbox_id, "Expected a non-empty sandbox ID in the log file."


def test_sandbox_with_expected_name_exists(sandbox_list, expected_sandbox_name):
    names = [_extract_name(entry) for entry in sandbox_list if isinstance(entry, dict)]
    assert expected_sandbox_name in names, (
        f"Expected a sandbox named {expected_sandbox_name!r} in 'daytona list' output. "
        f"Got names: {names}"
    )


def test_logged_id_matches_actual_sandbox_id(
    sandbox_list, expected_sandbox_name, logged_sandbox_id
):
    matched_entry = None
    for entry in sandbox_list:
        if not isinstance(entry, dict):
            continue
        if _extract_name(entry) == expected_sandbox_name:
            matched_entry = entry
            break
    assert matched_entry is not None, (
        f"No sandbox entry with name {expected_sandbox_name!r} found in "
        f"'daytona list' output."
    )
    actual_id = _extract_id(matched_entry)
    assert actual_id, (
        f"Sandbox entry for {expected_sandbox_name!r} has no 'id' field: {matched_entry!r}"
    )
    assert logged_sandbox_id == actual_id, (
        f"Sandbox ID in log file ({logged_sandbox_id!r}) does not match the actual "
        f"sandbox ID from Daytona ({actual_id!r})."
    )
