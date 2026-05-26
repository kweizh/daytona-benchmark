# Create a Daytona Sandbox with the Python SDK

## Background
You have the Daytona Python SDK (`daytona`) installed and a valid `DAYTONA_API_KEY` available in the environment. Daytona is a SaaS sandbox platform that lets you programmatically create isolated Linux sandboxes for running untrusted code. In this task, you will write a small one-off Python script that provisions a new sandbox on the hosted Daytona service, records its identifier, and then tears the sandbox down again.

## Requirements
- Write a Python script that uses the Daytona Python SDK to:
  - Create a new sandbox on the hosted Daytona service (`https://app.daytona.io/api`).
  - Assign the sandbox a deterministic name that includes the current `run-id` as a suffix so that concurrent runs do not collide.
  - Write the resulting sandbox ID to a log file.
  - Delete the sandbox afterwards as a cleanup step so no resources are leaked.
- The script must authenticate using the `DAYTONA_API_KEY` environment variable (the SDK reads it automatically).
- The script must run end-to-end as a single invocation (one-off job).

## Implementation Hints
- Import the SDK with `from daytona import Daytona`.
- The SDK reads `DAYTONA_API_KEY` from the environment by default, so no explicit configuration object is required for authentication.
- Read the value of `run-id` from the `ZEALT_RUN_ID` environment variable and append it to the base sandbox name.
- Use the SDK's sandbox creation API with a `name` parameter and the SDK's delete API for cleanup.
- Make sure to flush/close the log file so its contents are durable before the script exits.

## Acceptance Criteria
- Project path: /home/user/myproject
- Log file: /home/user/myproject/output.log
- Read `run-id` from the `ZEALT_RUN_ID` environment variable.
- The sandbox name must be `harbor-daytona-${run-id}` (base name `harbor-daytona` with the `run-id` appended as a suffix).
- The sandbox must be created on the hosted Daytona service via the Python SDK (no mocking).
- The log file must contain a line in the exact format: `Sandbox ID: <sandbox_id>` where `<sandbox_id>` is the non-empty identifier returned by the SDK for the newly created sandbox.
- After the script finishes, the sandbox must have been deleted via the SDK as a cleanup step.

