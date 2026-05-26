import os
from daytona import Daytona

def main():
    daytona = Daytona()
    try:
        volumes = daytona.volume.list()
        print(f"Volumes: {list(volumes)}")
    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error: {e}")
        if hasattr(e, 'body'):
            print(f"Body: {e.body}")

if __name__ == "__main__":
    main()
