import os
import time
from daytona_sdk import Daytona, CreateSandboxFromImageParams, SessionExecuteRequest

def run_task():
    run_id = os.getenv("ZEALT_RUN_ID")
    if not run_id:
        raise ValueError("ZEALT_RUN_ID environment variable is not set")

    api_key = os.getenv("DAYTONA_API_KEY")
    if not api_key:
        raise ValueError("DAYTONA_API_KEY environment variable is not set")

    sandbox_name = f"sess-{run_id}"
    session_id = "mysession"
    project_path = "/home/user/myproject"
    log_file_path = os.path.join(project_path, "output.log")

    daytona = Daytona()
    
    print(f"Creating sandbox: {sandbox_name}")
    # Using CreateSandboxFromImageParams since it inherits from CreateSandboxBaseParams 
    # and Daytona.create accepts it. We use a default image.
    params = CreateSandboxFromImageParams(image="ubuntu", name=sandbox_name)
    sandbox = daytona.create(params)
    
    try:
        print(f"Creating session: {session_id}")
        sandbox.process.create_session(session_id)

        commands = [
            "cd /tmp",
            f"export MYVAR=session-{run_id}",
            "pwd",
            "echo $MYVAR"
        ]

        results = {}

        for cmd in commands:
            print(f"Executing command: {cmd}")
            exec_request = SessionExecuteRequest(command=cmd)
            response = sandbox.process.execute_session_command(session_id, exec_request)
            
            # The search results showed response.cmd_id or response.command_id
            # Let's try response.cmd_id based on the most recent-looking docs
            command_id = response.cmd_id
            
            # If execute_session_command is synchronous (run_async=False by default),
            # we might already have the output in response.output.
            # However, the requirement says "Retrieve each command's logs through the session log API".
            
            logs_response = sandbox.process.get_session_command_logs(session_id, command_id)
            # logs_response is likely a SessionCommandLogsResponse with .stdout or .output
            if hasattr(logs_response, 'stdout'):
                output = logs_response.stdout
            elif hasattr(logs_response, 'output'):
                output = logs_response.output
            else:
                output = str(logs_response)
                
            trimmed_output = output.strip()
            
            if cmd == "pwd":
                results["PWD"] = trimmed_output
            elif cmd == "echo $MYVAR":
                results["MYVAR"] = trimmed_output

        print(f"Writing results to {log_file_path}")
        with open(log_file_path, "w") as f:
            f.write(f"PWD: {results.get('PWD', '')}\n")
            f.write(f"MYVAR: {results.get('MYVAR', '')}\n")

    finally:
        print("Cleaning up...")
        try:
            sandbox.process.delete_session(session_id)
        except Exception as e:
            print(f"Error deleting session: {e}")
            
        try:
            daytona.delete(sandbox)
        except Exception as e:
            print(f"Error removing sandbox: {e}")

if __name__ == "__main__":
    run_task()
