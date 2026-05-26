import os
from daytona import Daytona

def main():
    daytona = Daytona()
    try:
        # Try to find anything that might give organization info
        sandboxes = list(daytona.list())
        if sandboxes:
            print(f"Org ID from sandbox: {sandboxes[0].organization_id}")
        else:
            print("No sandboxes found")
            
        snapshots = list(daytona.snapshot.list())
        if snapshots:
            # The list returns a dict-like object sometimes?
            # From previous output: [('items', [...]), ('total', 17), ...]
            # Wait, it was a list of tuples? No, that's just how print(list(gen)) looked.
            pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
