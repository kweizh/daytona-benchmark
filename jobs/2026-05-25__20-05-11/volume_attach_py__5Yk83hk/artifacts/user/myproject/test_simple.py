import os
from daytona import Daytona

def main():
    daytona = Daytona()
    run_id = os.environ.get("ZEALT_RUN_ID")
    volume_name = f"vol-{run_id}"
    try:
        print(f"Getting or creating volume: {volume_name}")
        volume = daytona.volume.get(volume_name, create=True)
        print(f"Volume ID: {volume.id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
