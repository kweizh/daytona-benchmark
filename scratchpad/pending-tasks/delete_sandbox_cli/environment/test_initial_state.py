import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/myproject"


def test_daytona_binary_available():
    assert shutil.which("daytona") is not None, "daytona binary not found in PATH."


def test_jq_binary_available():
    assert shutil.which("jq") is not None, "jq binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_daytona_api_key_env_set():
    api_key = os.environ.get("DAYTONA_API_KEY")
    assert api_key is not None and api_key.strip() != "", (
        "DAYTONA_API_KEY environment variable is not set."
    )


def test_zealt_run_id_env_set():
    run_id = os.environ.get("ZEALT_RUN_ID")
    assert run_id is not None and run_id.strip() != "", (
        "ZEALT_RUN_ID environment variable is not set."
    )


def test_daytona_version_runs():
    result = subprocess.run(
        ["daytona", "version"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"`daytona version` failed (rc={result.returncode}): "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
