# Generate Signed Preview URL for a Sandbox HTTP Server

## Background
You have the Daytona CLI installed and a real Daytona SaaS API key available. Daytona sandboxes expose preview URLs that allow accessing services running inside the sandbox over the public internet. You need to programmatically spin up a sandbox, start a simple HTTP server inside it, obtain a signed preview URL via the CLI, and verify the URL serves the expected content.

## Requirements
- Write a shell script that uses the Daytona CLI end-to-end.
- Authenticate with Daytona using the API key in the `DAYTONA_API_KEY` environment variable.
- Create a new sandbox whose name is derived from the current `run-id`.
- Inside the sandbox, start a simple HTTP server on port `8000` that serves a single file whose content is derived from the current `run-id`.
- Obtain a signed preview URL for port `8000` via the Daytona CLI.
- Fetch the preview URL with `curl` from the task environment (not the sandbox) and persist both the URL and the response body to disk.

## Implementation Hints
- Read the current `run-id` from the `ZEALT_RUN_ID` environment variable.
- The sandbox name must be `prev-${ZEALT_RUN_ID}`.
- The HTTP server must serve a file whose body contains the exact string `HELLO_${ZEALT_RUN_ID}`.
- Use `daytona login --api-key $DAYTONA_API_KEY` to authenticate before any other CLI calls.
- Use `daytona create --name prev-${ZEALT_RUN_ID}` to create the sandbox.
- Use `daytona exec` to run commands inside the sandbox. Because `daytona exec` is synchronous, you must launch the HTTP server in a way that detaches it from the exec session (for example, with `nohup ... &` and redirected output, or `setsid`/`disown`), so the exec call returns while the server keeps running. `python3 -m http.server 8000` is a convenient server choice.
- Use `daytona preview-url prev-${ZEALT_RUN_ID} --port 8000` to retrieve a signed preview URL. The URL may be the entire stdout, or you may need to parse it.
- The signed preview URL embeds an authentication token, so plain `curl <url>` should succeed without extra headers.

## Acceptance Criteria
- Project path: /home/user/myproject
- Log file: /home/user/myproject/output.log
- The current `run-id` must be read from the `ZEALT_RUN_ID` environment variable.
- A sandbox named `prev-${ZEALT_RUN_ID}` must exist in the Daytona account associated with `DAYTONA_API_KEY` after the task runs.
- The log file must contain a line in the format: `Preview URL: <url>` where `<url>` is the signed preview URL returned by `daytona preview-url`.
- The file `/home/user/myproject/preview-response.txt` must contain the body returned by fetching the preview URL with `curl`. Its content must include the string `HELLO_${ZEALT_RUN_ID}`.

