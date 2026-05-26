import os
import subprocess

import pytest

PROJECT_DIR = "/home/user/myproject"


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Expected project directory {PROJECT_DIR} to exist before the task starts."
    )


def test_python3_available():
    result = subprocess.run(
        ["python3", "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0, (
        f"python3 is not available in PATH (returncode={result.returncode}, "
        f"stderr={result.stderr!r})."
    )


def test_daytona_python_sdk_importable():
    result = subprocess.run(
        ["python3", "-c", "import daytona; from daytona import Daytona"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "Expected the Daytona Python SDK to be importable via "
        "`from daytona import Daytona`, but the import failed. "
        f"stderr={result.stderr!r}"
    )
