# Stateful Shell Sessions with the Daytona Python SDK

## Background
Daytona sandboxes expose a `process` module that supports stateful shell sessions. Unlike one-shot command execution, a session preserves the shell's working directory, environment variables, and other process state across multiple commands, allowing you to script multi-step workflows that depend on each other.

In this task, you will use the Daytona Python SDK to spin up a real sandbox, drive a single shell session through a sequence of state-dependent commands, capture each command's stdout via the session log API, and persist the results to a log file before tearing everything down.

## Requirements
- Use the official Daytona Python SDK (`pip install daytona`) and authenticate via the `DAYTONA_API_KEY` environment variable.
- Create a new sandbox whose name includes the current `run-id` so concurrent trials do not collide.
- Inside that sandbox, create a single named shell session and run a sequence of commands within it so that environment variables and working directory persist across calls.
- Retrieve each command's logs through the session log API and append summary lines to a log file on the local task host.
- Clean up by deleting the session and the sandbox once the work has been recorded.

## Implementation Hints
- Read `run-id` from the `ZEALT_RUN_ID` environment variable and use it as a suffix when naming the sandbox and as content inside the exported variable.
- Look at the Daytona Python SDK methods on `sandbox.process`: `create_session`, `execute_session_command`, `get_session_command_logs`, and `delete_session`.
- The `execute_session_command` call accepts a `SessionExecuteRequest` describing the command to run; the returned object exposes a command id you can use to fetch logs.
- Make sure you reuse the same session id for every command so that `cd` and `export` carry over to the subsequent `pwd` and `echo` calls.
- Strip surrounding whitespace from each command's stdout before writing it into the log file.

## Acceptance Criteria
- Project path: /home/user/myproject
- Log file: /home/user/myproject/output.log
- Sandbox name: `sess-${ZEALT_RUN_ID}` (created and then deleted by the task).
- Session name inside the sandbox: `mysession` (created and then deleted by the task).
- The session must be used to run, in order, the equivalent of: `cd /tmp`, `export MYVAR=session-${ZEALT_RUN_ID}`, `pwd`, and `echo $MYVAR`.
- The log file must contain exactly two lines in this order:
  - `PWD: <pwd output>`
  - `MYVAR: <echo output>`
  where each `<...>` is the trimmed stdout of the corresponding session command.

