import os
from daytona import Daytona

def main():
    daytona = Daytona()
    try:
        volumes = daytona.volume.list()
        print(f"Volumes: {volumes}")
        for v in volumes:
            print(v)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
