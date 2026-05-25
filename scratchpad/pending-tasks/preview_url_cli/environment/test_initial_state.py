import os
import shutil

PROJECT_DIR = "/home/user/myproject"


def test_daytona_cli_available():
    assert shutil.which("daytona") is not None, "daytona binary not found in PATH."


def test_curl_available():
    assert shutil.which("curl") is not None, "curl binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
