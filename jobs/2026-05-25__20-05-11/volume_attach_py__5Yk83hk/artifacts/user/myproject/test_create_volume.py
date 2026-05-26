import os
from daytona import Daytona

def main():
    daytona = Daytona()
    run_id = os.environ.get("ZEALT_RUN_ID")
    volume_name = f"vol-{run_id}"
    try:
        print(f"Creating volume: {volume_name}")
        volume = daytona.volume.create(volume_name)
        print(f"Created volume ID: {volume.id}")
    except Exception as e:
        print(f"Error creating volume: {e}")

if __name__ == "__main__":
    main()
