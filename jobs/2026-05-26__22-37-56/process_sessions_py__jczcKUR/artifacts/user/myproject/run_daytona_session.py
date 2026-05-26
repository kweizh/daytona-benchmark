import os
from daytona import Daytona, CreateSandboxFromSnapshotParams, SessionExecuteRequest

RUN_ID = os.environ["ZEALT_RUN_ID"]
SANDBOX_NAME = f"sess-{RUN_ID}"
SESSION_ID = "mysession"
LOG_PATH = "/home/user/myproject/output.log"


def main() -> None:
    daytona = Daytona()
    sandbox = None
    try:
        params = CreateSandboxFromSnapshotParams(name=SANDBOX_NAME)
        sandbox = daytona.create(params)
        process = sandbox.process
        process.create_session(SESSION_ID)

        commands = [
            "cd /tmp",
            f"export MYVAR=session-{RUN_ID}",
            "pwd",
            "echo $MYVAR",
        ]

        command_ids = []
        for command in commands:
            response = process.execute_session_command(
                SESSION_ID,
                SessionExecuteRequest(command=command),
            )
            command_ids.append(response.cmd_id)

        logs = [
            process.get_session_command_logs(SESSION_ID, command_id)
            for command_id in command_ids
        ]

        pwd_output = (logs[2].stdout or "").strip()
        myvar_output = (logs[3].stdout or "").strip()

        with open(LOG_PATH, "w", encoding="utf-8") as log_file:
            log_file.write(f"PWD: {pwd_output}\n")
            log_file.write(f"MYVAR: {myvar_output}\n")
    finally:
        if sandbox is not None:
            try:
                sandbox.process.delete_session(SESSION_ID)
            except Exception:
                pass
            try:
                daytona.delete(sandbox)
            except Exception:
                pass


if __name__ == "__main__":
    main()
