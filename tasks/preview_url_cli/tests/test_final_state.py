import json
import os
import re
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"
OUTPUT_LOG = os.path.join(PROJECT_DIR, "output.log")
PREVIEW_RESPONSE = os.path.join(PROJECT_DIR, "preview-response.txt")

PREVIEW_URL_LINE_RE = re.compile(r"^Preview URL:\s*(https://\S+)\s*$", re.MULTILINE)


def _run_id() -> str:
    run_id = os.environ.get("ZEALT_RUN_ID")
    assert run_id, "ZEALT_RUN_ID environment variable must be set."
    return run_id


def _sandbox_name() -> str:
    return f"prev-{_run_id()}"


def test_output_log_exists():
    assert os.path.isfile(OUTPUT_LOG), (
        f"Expected output log file {OUTPUT_LOG} to exist."
    )


def test_output_log_contains_preview_url():
    with open(OUTPUT_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    match = PREVIEW_URL_LINE_RE.search(content)
    assert match is not None, (
        "output.log must contain a line matching 'Preview URL: <https-url>'. "
        f"Actual content:\n{content}"
    )
    url = match.group(1)
    assert url.startswith("https://"), (
        f"Preview URL must start with https://, got: {url}"
    )
    assert "daytona" in url.lower(), (
        f"Preview URL host should look like a Daytona preview URL, got: {url}"
    )


def test_preview_response_contains_expected_marker():
    assert os.path.isfile(PREVIEW_RESPONSE), (
        f"Expected preview response file {PREVIEW_RESPONSE} to exist."
    )
    with open(PREVIEW_RESPONSE, "r", encoding="utf-8") as f:
        body = f.read()
    expected = f"HELLO_{_run_id()}"
    assert expected in body, (
        f"Preview response body must contain {expected!r}. Got: {body!r}"
    )


def test_sandbox_exists_in_daytona_account():
    api_key = os.environ.get("DAYTONA_API_KEY")
    assert api_key, "DAYTONA_API_KEY environment variable must be set for verification."

    login = subprocess.run(
        ["daytona", "login", "--api-key", api_key],
        capture_output=True,
        text=True,
    )
    assert login.returncode == 0, (
        f"'daytona login' failed during verification. "
        f"stdout: {login.stdout}\nstderr: {login.stderr}"
    )

    result = subprocess.run(
        ["daytona", "list", "--format", "json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"'daytona list --format json' failed. "
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    try:
        sandboxes = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"Could not parse 'daytona list --format json' output as JSON: {exc}\n"
            f"stdout was:\n{result.stdout}"
        )

    assert isinstance(sandboxes, list), (
        f"Expected 'daytona list --format json' to return a JSON array, "
        f"got: {type(sandboxes).__name__}"
    )

    expected_name = _sandbox_name()
    names = []
    for sb in sandboxes:
        if not isinstance(sb, dict):
            continue
        name = sb.get("name") or sb.get("Name")
        if name:
            names.append(name)

    assert expected_name in names, (
        f"Expected a Daytona sandbox named {expected_name!r} to exist. "
        f"Found sandboxes: {names}"
    )
