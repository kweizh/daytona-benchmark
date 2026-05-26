import os
import sys
from daytona import Daytona, CreateSandboxFromSnapshotParams

def main():
    # Read run-id from ZEALT_RUN_ID environment variable
    run_id = os.environ.get("ZEALT_RUN_ID")
    if not run_id:
        print("Error: ZEALT_RUN_ID environment variable is not set", file=sys.stderr)
        sys.exit(1)
    
    # The sandbox name must be harbor-daytona-${run-id}
    sandbox_name = f"harbor-daytona-{run_id}"
    
    # Initialize the Daytona client
    # The SDK reads DAYTONA_API_KEY from the environment by default.
    daytona = Daytona()
    
    sandbox = None
    try:
        # Create a new sandbox on the hosted Daytona service
        # Assign the sandbox a deterministic name
        params = CreateSandboxFromSnapshotParams(name=sandbox_name)
        
        print(f"Creating sandbox: {sandbox_name}...")
        sandbox = daytona.create(params)
        
        sandbox_id = sandbox.id
        
        # Write the resulting sandbox ID to a log file
        # Log file: /home/user/myproject/output.log
        # Format: Sandbox ID: <sandbox_id>
        log_file_path = "/home/user/myproject/output.log"
        with open(log_file_path, "w") as f:
            f.write(f"Sandbox ID: {sandbox_id}\n")
            f.flush()
            os.fsync(f.fileno())
            
        print(f"Sandbox created successfully. ID: {sandbox_id}")
        
    except Exception as e:
        print(f"An error occurred during sandbox operation: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if sandbox:
            # Delete the sandbox afterwards as a cleanup step so no resources are leaked
            print(f"Deleting sandbox: {sandbox_name} (ID: {sandbox.id})...")
            try:
                daytona.delete(sandbox)
                print("Sandbox deleted successfully.")
            except Exception as delete_error:
                print(f"Failed to delete sandbox: {delete_error}", file=sys.stderr)

if __name__ == "__main__":
    main()
