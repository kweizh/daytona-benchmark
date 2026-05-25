import importlib.util
import os

PROJECT_DIR = "/home/user/myproject"


def test_daytona_sdk_importable():
    spec = importlib.util.find_spec("daytona")
    assert spec is not None, (
        "Daytona Python SDK is not importable. Install it with 'pip install daytona'."
    )


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR} does not exist."
    )
