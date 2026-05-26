import os
from daytona import Daytona, DaytonaConfig

def main():
    config = DaytonaConfig(organization_id="3ae0ced2-f32b-4c06-ba3b-51e5bb22e6e6")
    daytona = Daytona(config=config)
    try:
        print("Listing volumes with org_id...")
        volumes = list(daytona.volume.list())
        print(f"Count: {len(volumes)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
