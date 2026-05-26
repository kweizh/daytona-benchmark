import os
import sys

from daytona import Daytona, CreateSandboxBaseParams


def main() -> int:
    run_id = os.getenv("ZEALT_RUN_ID")
    if not run_id:
        print("ZEALT_RUN_ID is not set", file=sys.stderr)
        return 1

    os.environ.setdefault("DAYTONA_API_URL", "REDACTED")

    sandbox_name = f"harbor-daytona-{run_id}"
    sandbox = None
    daytona = Daytona()

    try:
        sandbox = daytona.create(CreateSandboxBaseParams(name=sandbox_name))
        if not getattr(sandbox, "id", None):
            raise RuntimeError("Sandbox creation did not return an id")

        log_path = "/home/user/myproject/output.log"
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(f"Sandbox ID: {sandbox.id}\n")
            log_file.flush()
    finally:
        if sandbox is not None:
            sandbox.delete()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
