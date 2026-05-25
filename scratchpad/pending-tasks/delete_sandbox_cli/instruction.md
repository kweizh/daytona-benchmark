# Delete a Daytona Sandbox via the CLI

## Background
Daytona is a development environment manager that provisions isolated sandboxes for code execution. The Daytona CLI lets you log in, create, inspect, and delete sandboxes against the Daytona SaaS. In this task, you will exercise the full lifecycle of a sandbox: authenticate, create one, capture its metadata, delete it, and record the result in a log file.

## Requirements
- Authenticate the Daytona CLI using the API key supplied via the `DAYTONA_API_KEY` environment variable.
- Create a new sandbox whose name uses the `run-id` from the `ZEALT_RUN_ID` environment variable.
- Capture the created sandbox's metadata as JSON before deletion.
- Delete the sandbox using the Daytona CLI.
- Record creation and deletion events in a log file under the project directory.

## Implementation Hints
- Read `run-id` from the `ZEALT_RUN_ID` environment variable and build the sandbox name as `del-${run-id}`.
- Use `daytona login --api-key` with the value of `DAYTONA_API_KEY` to authenticate.
- Use `daytona create --name <name>` to create the sandbox, and `daytona info <name> --format json` to obtain its metadata.
- Use `daytona delete <name>` to remove the sandbox (the CLI may require confirmation; consult `daytona delete --help`).
- Use `jq` (already available) to extract fields such as the sandbox `id` from the captured JSON.

## Acceptance Criteria
- Project path: /home/user/myproject
- Log file: /home/user/myproject/output.log
- Metadata file: /home/user/myproject/before-delete.json
- The sandbox name must be `del-${run-id}` where `run-id` is read from the `ZEALT_RUN_ID` environment variable.
- `/home/user/myproject/before-delete.json` must contain the JSON output of `daytona info del-${run-id} --format json` captured BEFORE deletion. The JSON must include the sandbox name `del-${run-id}`.
- `/home/user/myproject/output.log` must contain (in order):
  - A line in the format `Sandbox ID: <id>` where `<id>` is the id of the created sandbox.
  - A line in the format `Deleted: <id>` where `<id>` is the same sandbox id, written after the sandbox has been deleted.
- After the task completes, the sandbox `del-${run-id}` must no longer be present in `daytona list --format json` (or it must be in a terminal DELETED-like state).

