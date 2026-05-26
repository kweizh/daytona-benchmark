import os
from daytona import Daytona, DaytonaConfig

def main():
    config = DaytonaConfig(target="us")
    daytona = Daytona(config=config)
    try:
        print("Listing volumes with target=us...")
        volumes = list(daytona.volume.list())
        print(f"Count: {len(volumes)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
