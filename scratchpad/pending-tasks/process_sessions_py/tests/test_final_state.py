import os

import pytest

OUTPUT_LOG = "/home/user/myproject/output.log"


@pytest.fixture(scope="module")
def log_lines():
    assert os.path.isfile(OUTPUT_LOG), (
        f"Expected log file {OUTPUT_LOG} does not exist."
    )
    with open(OUTPUT_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    assert content.strip(), f"Log file {OUTPUT_LOG} is empty."
    return content.splitlines()


def _find_prefixed_line(lines, prefix):
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return None


def test_pwd_line_matches_tmp(log_lines):
    value = _find_prefixed_line(log_lines, "PWD: ")
    assert value is not None, (
        "Log file is missing a line starting with 'PWD: '. "
        f"Lines: {log_lines!r}"
    )
    assert value == "/tmp", (
        f"Expected PWD value to be '/tmp', got '{value}'."
    )


def test_myvar_line_matches_run_id(log_lines):
    run_id = os.environ.get("ZEALT_RUN_ID")
    assert run_id, (
        "ZEALT_RUN_ID environment variable is not set in the verifier "
        "environment; cannot validate MYVAR."
    )
    expected = f"session-{run_id}"
    value = _find_prefixed_line(log_lines, "MYVAR: ")
    assert value is not None, (
        "Log file is missing a line starting with 'MYVAR: '. "
        f"Lines: {log_lines!r}"
    )
    assert value == expected, (
        f"Expected MYVAR value to be '{expected}', got '{value}'."
    )
