import os
from daytona import Daytona, CreateSandboxFromSnapshotParams

def main():
    # Read run-id from ZEALT_RUN_ID
    run_id = os.environ.get("ZEALT_RUN_ID", "default")
    sandbox_name = f"harbor-daytona-{run_id}"
    
    # Initialize Daytona SDK
    daytona = Daytona()
    
    # Create the sandbox with the specified name
    params = CreateSandboxFromSnapshotParams(name=sandbox_name)
    sandbox = daytona.create(params)
    
    # Write the sandbox ID to the log file
    log_file_path = "/home/user/myproject/output.log"
    with open(log_file_path, "w") as f:
        f.write(f"Sandbox ID: {sandbox.id}\n")
    
    # Delete the sandbox to clean up resources
    daytona.delete(sandbox)

if __name__ == "__main__":
    main()
