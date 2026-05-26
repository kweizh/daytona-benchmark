import os
import time
from daytona import Daytona, CreateSandboxFromSnapshotParams, VolumeMount

def main():
    api_key = os.environ.get("DAYTONA_API_KEY")
    run_id = os.environ.get("ZEALT_RUN_ID")
    
    if not api_key or not run_id:
        print("Missing environment variables")
        return

    daytona = Daytona()
    
    volume_name = f"vol-{run_id}"
    sandbox_name = f"vol-py-{run_id}"
    log_file = "/home/user/myproject/output.log"
    
    try:
        # Get or create volume
        print(f"Getting or creating volume: {volume_name}")
        volume = daytona.volume.get(volume_name, create=True)
        
        # Create sandbox with volume mount
        print(f"Creating sandbox: {sandbox_name}")
        sandbox = daytona.create_sandbox(CreateSandboxFromSnapshotParams(
            name=sandbox_name,
            volumes=[
                VolumeMount(volume_id=volume.id, mount_path="/data")
            ]
        ))
        
        try:
            # Write marker file
            marker_content = f"persistent {run_id}"
            print(f"Writing marker to sandbox...")
            sandbox.process.exec(f"echo '{marker_content}' > /data/marker.txt")
            
            # Read marker file
            print(f"Reading marker from sandbox...")
            result = sandbox.process.exec("cat /data/marker.txt")
            read_content = result.stdout.strip()
            
            # List volumes
            print(f"Listing volumes...")
            volumes = daytona.volume.list()
            volume_count = len(volumes)
            
            # Write log file
            print(f"Writing to log file: {log_file}")
            with open(log_file, "w") as f:
                f.write(f"Marker: {read_content}\n")
                f.write(f"VolumeCount: {volume_count}\n")
            
            print("Task completed successfully")
            
        finally:
            # Clean up: delete sandbox
            print(f"Deleting sandbox: {sandbox_name}")
            daytona.remove_sandbox(sandbox.id)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
