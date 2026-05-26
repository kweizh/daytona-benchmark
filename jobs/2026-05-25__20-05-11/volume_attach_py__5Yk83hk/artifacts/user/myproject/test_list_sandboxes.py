import os
from daytona import Daytona

def main():
    daytona = Daytona()
    try:
        sandboxes = list(daytona.list())
        print(f"Sandbox count: {len(sandboxes)}")
    except Exception as e:
        print(f"Error listing sandboxes: {e}")

if __name__ == "__main__":
    main()
