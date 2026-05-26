import os
from daytona import Daytona, CreateSandboxFromSnapshotParams

def main():
    run_id = os.environ.get("ZEALT_RUN_ID")
    daytona = Daytona()
    try:
        sandbox_name = f"test-py-{run_id}"
        print(f"Creating test sandbox: {sandbox_name}")
        sandbox = daytona.create_sandbox(CreateSandboxFromSnapshotParams(name=sandbox_name))
        print(f"Created sandbox ID: {sandbox.id}")
        daytona.remove_sandbox(sandbox.id)
        print("Removed sandbox")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
