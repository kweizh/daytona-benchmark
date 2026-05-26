import os
import time
from daytona import Daytona, CreateSandboxBaseParams, SessionExecuteRequest

def main():
    run_id = os.environ.get("ZEALT_RUN_ID", "default")
    sandbox_name = f"sess-{run_id}"
    session_id = "mysession"
    
    daytona_client = Daytona()
    
    print(f"Creating sandbox {sandbox_name}...")
    sandbox = daytona_client.create(CreateSandboxBaseParams(name=sandbox_name, image="ubuntu:22.04"))
    
    try:
        print(f"Creating session {session_id}...")
        sandbox.process.create_session(session_id)
        
        # 1. cd /tmp
        req1 = SessionExecuteRequest(command="cd /tmp")
        res1 = sandbox.process.execute_session_command(session_id, req1)
        
        # 2. export MYVAR=session-${ZEALT_RUN_ID}
        req2 = SessionExecuteRequest(command=f"export MYVAR=session-{run_id}")
        res2 = sandbox.process.execute_session_command(session_id, req2)
        
        # 3. pwd
        req3 = SessionExecuteRequest(command="pwd")
        res3 = sandbox.process.execute_session_command(session_id, req3)
        logs3 = sandbox.process.get_session_command_logs(session_id, res3.cmd_id)
        pwd_output = logs3.stdout.strip()
        
        # 4. echo $MYVAR
        req4 = SessionExecuteRequest(command="echo $MYVAR")
        res4 = sandbox.process.execute_session_command(session_id, req4)
        logs4 = sandbox.process.get_session_command_logs(session_id, res4.cmd_id)
        myvar_output = logs4.stdout.strip()
        
        # Write to log file
        log_file_path = "/home/user/myproject/output.log"
        with open(log_file_path, "w") as f:
            f.write(f"PWD: {pwd_output}\n")
            f.write(f"MYVAR: {myvar_output}\n")
            
        print(f"Wrote outputs to {log_file_path}")
        
    finally:
        print("Cleaning up...")
        try:
            sandbox.process.delete_session(session_id)
        except Exception as e:
            print(f"Error deleting session: {e}")
        sandbox.delete()
        print("Sandbox deleted.")

if __name__ == "__main__":
    main()
