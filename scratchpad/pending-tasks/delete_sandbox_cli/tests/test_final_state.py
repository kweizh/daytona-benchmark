import json
import os
import re
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")
BEFORE_FILE = os.path.join(PROJECT_DIR, "before-delete.json")

TERMINAL_STATES = {
    "destroyed",
    "deleted",
    "archived",
    "stopped",
    "removing",
    "destroying",
    "terminated",
}


@pytest.fixture(scope="session")
def run_id():
    rid = os.environ.get("ZEALT_RUN_ID")
    assert rid, "ZEALT_RUN_ID environment variable is not set in verifier env."
    return rid


@pytest.fixture(scope="session")
def sandbox_name(run_id):
    return f"del-{run_id}"


@pytest.fixture(scope="session")
def before_delete_json():
    assert os.path.isfile(BEFORE_FILE), (
        f"Expected sandbox metadata file at {BEFORE_FILE}, but it does not exist."
    )
    with open(BEFORE_FILE) as f:
        text = f.read()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        pytest.fail(f"{BEFORE_FILE} is not valid JSON: {e}; content head={text[:200]!r}")
    return data


@pytest.fixture(scope="session")
def sandbox_id(before_delete_json, sandbox_name):
    """Extract the sandbox id from the before-delete metadata file."""
    data = before_delete_json
    # Common id field names
    candidates = []
    if isinstance(data, dict):
        for key in ("id", "ID", "Id", "sandboxId", "sandbox_id"):
            if key in data and isinstance(data[key], str) and data[key].strip():
                candidates.append(data[key])
    assert candidates, (
        f"Could not find a sandbox id field in {BEFORE_FILE}; data keys: "
        f"{list(data.keys()) if isinstance(data, dict) else type(data).__name__}"
    )
    return candidates[0]


def _daytona_login():
    api_key = os.environ.get("DAYTONA_API_KEY")
    assert api_key, "DAYTONA_API_KEY env var is not set in verifier env."
    result = subprocess.run(
        ["daytona", "login", "--api-key", api_key],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"`daytona login` failed in verifier: rc={result.returncode} "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )


@pytest.fixture(scope="session", autouse=True)
def verifier_login():
    _daytona_login()
    yield


def test_before_delete_json_contains_sandbox_name(before_delete_json, sandbox_name):
    """The pre-delete metadata JSON must mention the sandbox name."""
    serialized = json.dumps(before_delete_json)
    assert sandbox_name in serialized, (
        f"Expected sandbox name {sandbox_name!r} to appear in {BEFORE_FILE}, "
        f"but it was not found. Content: {serialized[:500]}"
    )
    if isinstance(before_delete_json, dict) and "name" in before_delete_json:
        assert before_delete_json["name"] == sandbox_name, (
            f"Expected top-level 'name' field to equal {sandbox_name!r}, "
            f"got {before_delete_json['name']!r}."
        )


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), f"Expected log file at {LOG_FILE}."


def test_log_contains_sandbox_id_line(sandbox_id):
    with open(LOG_FILE) as f:
        content = f.read()
    pattern = re.compile(
        rf"^Sandbox ID:\s*{re.escape(sandbox_id)}\s*$", re.MULTILINE
    )
    assert pattern.search(content), (
        f"Expected a line `Sandbox ID: {sandbox_id}` in {LOG_FILE}; "
        f"actual content:\n{content}"
    )


def test_log_contains_deleted_line(sandbox_id):
    with open(LOG_FILE) as f:
        content = f.read()
    pattern = re.compile(
        rf"^Deleted:\s*{re.escape(sandbox_id)}\s*$", re.MULTILINE
    )
    assert pattern.search(content), (
        f"Expected a line `Deleted: {sandbox_id}` in {LOG_FILE}; "
        f"actual content:\n{content}"
    )


def test_deleted_line_appears_after_sandbox_id_line(sandbox_id):
    with open(LOG_FILE) as f:
        content = f.read()
    sb_idx = content.find(f"Sandbox ID: {sandbox_id}")
    del_idx = content.find(f"Deleted: {sandbox_id}")
    assert sb_idx >= 0 and del_idx >= 0, (
        f"Both `Sandbox ID:` and `Deleted:` lines must be present in {LOG_FILE}."
    )
    assert del_idx > sb_idx, (
        "The `Deleted:` line must appear AFTER the `Sandbox ID:` line in "
        f"{LOG_FILE}."
    )


def test_sandbox_not_active_in_daytona_list(sandbox_name):
    """Using the Daytona CLI, verify the sandbox is gone (or in a terminal state)."""
    result = subprocess.run(
        ["daytona", "list", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"`daytona list --format json` failed in verifier: rc={result.returncode} "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    stdout = result.stdout.strip()
    if not stdout or stdout in ("null", "[]"):
        return  # No sandboxes -> definitely gone.

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as e:
        pytest.fail(
            f"Could not parse `daytona list --format json` output as JSON: {e}; "
            f"stdout head={stdout[:300]!r}"
        )

    # Normalize to list of dicts.
    if isinstance(data, dict):
        # Some CLIs wrap results in an object; flatten any list values.
        items = []
        for v in data.values():
            if isinstance(v, list):
                items.extend(v)
        if not items:
            items = [data]
    elif isinstance(data, list):
        items = data
    else:
        pytest.fail(
            f"Unexpected JSON shape from `daytona list`: {type(data).__name__}"
        )

    matching = []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("name") or item.get("Name")
        if name == sandbox_name:
            matching.append(item)

    if not matching:
        # Sandbox is gone -> success.
        return

    # If still present, every matching entry must be in a terminal/non-active state.
    for entry in matching:
        state = (
            entry.get("state")
            or entry.get("status")
            or entry.get("State")
            or entry.get("Status")
            or ""
        )
        state_l = str(state).strip().lower()
        assert state_l in TERMINAL_STATES, (
            f"Sandbox {sandbox_name!r} is still listed with non-terminal "
            f"state {state!r}; full entry: {entry}"
        )
