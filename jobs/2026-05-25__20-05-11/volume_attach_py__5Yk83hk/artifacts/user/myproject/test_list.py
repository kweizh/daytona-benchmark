import os
from daytona import Daytona

def main():
    api_key = os.environ.get("DAYTONA_API_KEY")
    daytona = Daytona()
    try:
        volumes = daytona.volume.list()
        print(f"Volume count: {len(volumes)}")
        for v in volumes:
            print(f"Volume: {v.name} (ID: {v.id})")
    except Exception as e:
        print(f"Error listing volumes: {e}")

if __name__ == "__main__":
    main()
