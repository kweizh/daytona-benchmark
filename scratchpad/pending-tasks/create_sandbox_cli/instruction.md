# Create a Daytona Sandbox with the Daytona CLI

## Background
You have the Daytona CLI (`daytona`) installed in the environment. Daytona provides a hosted control plane for creating isolated sandboxes used for running development workloads or untrusted code. Your task is to author a shell script that authenticates with Daytona, provisions a new sandbox with a deterministic name, and records the assigned sandbox ID to a log file.

## Requirements
- Authenticate the Daytona CLI using the API key available in the `DAYTONA_API_KEY` environment variable.
- Create a new Daytona sandbox whose name uses the base `sb` with the current `run-id` appended as a suffix.
- Determine the resulting sandbox ID by listing existing sandboxes through the CLI and matching on the sandbox name.
- Write the discovered sandbox ID to a log file in a fixed format.

## Implementation Hints
- Read the current `run-id` from the `ZEALT_RUN_ID` environment variable and build the sandbox name as `sb-${run-id}`.
- Use the Daytona CLI subcommand for authentication that consumes an API key.
- The Daytona CLI's `list` command supports a JSON output format that includes both sandbox name and ID fields, which makes it suitable for downstream parsing.
- A small shell utility such as `jq` is helpful for extracting fields from the JSON response.
- Persist the result line to the log file with truncation (overwrite) semantics rather than appending, so the file ends with the latest sandbox ID line only.

## Acceptance Criteria
- Project path: /home/user/myproject
- Log file: /home/user/myproject/output.log
- Use the Daytona CLI to perform the sandbox creation.
- The sandbox name must be `sb-${run-id}` where `run-id` is read from the `ZEALT_RUN_ID` environment variable.
- The log file must contain a line in the exact format: `Sandbox ID: <sandbox_id>` where `<sandbox_id>` matches the ID Daytona assigned to the newly created sandbox.

