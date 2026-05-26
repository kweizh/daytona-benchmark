import os
from daytona import Daytona

def main():
    daytona = Daytona()
    try:
        print("Creating volume: testvol")
        v = daytona.volume.create("testvol")
        print(f"ID: {v.id}")
        daytona.volume.delete(v.id)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
