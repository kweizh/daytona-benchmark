#!/usr/bin/env python3
"""
Stateful Shell Session Demo with Daytona SDK
"""
import os
from daytona import Daytona, SessionExecuteRequest

# Get run ID from environment
RUN_ID = os.environ.get("ZEALT_RUN_ID", "default")
SANDBOX_NAME = f"sess-{RUN_ID}"
SESSION_ID = "mysession"
OUTPUT_FILE = "/home/user/myproject/output.log"

def main():
    # Initialize Daytona client
    client = Daytona()
    
    sandbox = None
    
    try:
        # Create a new sandbox
        print(f"Creating sandbox: {SANDBOX_NAME}")
        sandbox = client.create()
        print(f"Sandbox created: {sandbox.id}")
        
        # Create a session
        print(f"Creating session: {SESSION_ID}")
        sandbox.process.create_session(session_id=SESSION_ID)
        print(f"Session created: {SESSION_ID}")
        
        # Command 1: cd /tmp
        print("Executing: cd /tmp")
        req1 = SessionExecuteRequest(command="cd /tmp")
        cmd1 = sandbox.process.execute_session_command(
            session_id=SESSION_ID,
            req=req1,
        )
        print(f"Command 1 executed: {cmd1.cmd_id}")
        
        # Command 2: export MYVAR=session-${RUN_ID}
        print(f"Executing: export MYVAR=session-{RUN_ID}")
        req2 = SessionExecuteRequest(command=f"export MYVAR=session-{RUN_ID}")
        cmd2 = sandbox.process.execute_session_command(
            session_id=SESSION_ID,
            req=req2,
        )
        print(f"Command 2 executed: {cmd2.cmd_id}")
        
        # Command 3: pwd (capture output)
        print("Executing: pwd")
        req3 = SessionExecuteRequest(command="pwd")
        cmd3 = sandbox.process.execute_session_command(
            session_id=SESSION_ID,
            req=req3,
        )
        print(f"Command 3 executed: {cmd3.cmd_id}")
        
        # Get logs for pwd command
        logs3 = sandbox.process.get_session_command_logs(
            session_id=SESSION_ID,
            command_id=cmd3.cmd_id,
        )
        pwd_output = logs3.stdout.strip() if logs3.stdout else ""
        print(f"PWD output: {pwd_output}")
        
        # Command 4: echo $MYVAR (capture output)
        print("Executing: echo $MYVAR")
        req4 = SessionExecuteRequest(command="echo $MYVAR")
        cmd4 = sandbox.process.execute_session_command(
            session_id=SESSION_ID,
            req=req4,
        )
        print(f"Command 4 executed: {cmd4.cmd_id}")
        
        # Get logs for echo command
        logs4 = sandbox.process.get_session_command_logs(
            session_id=SESSION_ID,
            command_id=cmd4.cmd_id,
        )
        myvar_output = logs4.stdout.strip() if logs4.stdout else ""
        print(f"MYVAR output: {myvar_output}")
        
        # Write results to output file
        print(f"Writing results to {OUTPUT_FILE}")
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"PWD: {pwd_output}\n")
            f.write(f"MYVAR: {myvar_output}\n")
        
        print(f"Output written successfully")
        
    finally:
        # Clean up: delete session
        if sandbox:
            print(f"Deleting session: {SESSION_ID}")
            sandbox.process.delete_session(session_id=SESSION_ID)
            print("Session deleted")
        
        # Clean up: delete sandbox
        if sandbox:
            print(f"Deleting sandbox: {SANDBOX_NAME}")
            client.delete(sandbox)
            print("Sandbox deleted")

if __name__ == "__main__":
    main()