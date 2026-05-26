import os
from daytona import Daytona, CreateSandboxFromSnapshotParams, VolumeMount

def main():
    daytona = Daytona()
    run_id = os.environ.get("ZEALT_RUN_ID")
    volume_name = f"vol-{run_id}"
    sandbox_name = f"vol-py-{run_id}"
    
    try:
        print(f"Creating sandbox with volume name as ID: {sandbox_name}")
        sandbox = daytona.create(CreateSandboxFromSnapshotParams(
            name=sandbox_name,
            volumes=[
                VolumeMount(volume_id=volume_name, mount_path="/data")
            ]
        ))
        print(f"Created sandbox ID: {sandbox.id}")
        
        # Write marker
        marker_content = f"persistent {run_id}"
        print("Writing marker...")
        sandbox.process.exec(f"echo '{marker_content}' > /data/marker.txt")
        
        # Read marker
        print("Reading marker...")
        result = sandbox.process.exec("cat /data/marker.txt")
        read_content = result.stdout.strip()
        print(f"Read content: {read_content}")
        
        # Clean up
        daytona.delete(sandbox)
        print("Deleted sandbox")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
