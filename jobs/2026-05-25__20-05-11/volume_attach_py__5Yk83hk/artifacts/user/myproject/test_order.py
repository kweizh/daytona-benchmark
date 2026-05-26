import os
from daytona import Daytona, CreateSandboxFromSnapshotParams

def main():
    daytona = Daytona()
    run_id = os.environ.get("ZEALT_RUN_ID")
    sandbox_name = f"vol-py-{run_id}"
    try:
        print(f"Creating sandbox: {sandbox_name}")
        sandbox = daytona.create(CreateSandboxFromSnapshotParams(name=sandbox_name))
        print(f"Created sandbox ID: {sandbox.id}")
        
        try:
            # Try to list volumes now
            print("Listing volumes...")
            volumes = list(daytona.volume.list())
            print(f"Volume count: {len(volumes)}")
        except Exception as e:
            print(f"Error listing volumes: {e}")
            
        daytona.delete(sandbox)
        print("Deleted sandbox")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
