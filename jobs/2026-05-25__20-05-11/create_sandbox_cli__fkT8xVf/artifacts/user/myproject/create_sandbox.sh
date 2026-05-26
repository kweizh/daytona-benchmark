#!/bin/bash

# Exit on error
set -e

# Configuration
PROJECT_DIR="/home/user/myproject"
LOG_FILE="${PROJECT_DIR}/output.log"
RUN_ID="${ZEALT_RUN_ID}"
SANDBOX_NAME="sb-${RUN_ID}"

# Ensure project directory exists
mkdir -p "${PROJECT_DIR}"

# 1. Authenticate with Daytona using the API key
if [ -z "${DAYTONA_API_KEY}" ]; then
    echo "Error: DAYTONA_API_KEY is not set." >&2
    exit 1
fi

# Authenticate
daytona login --api-key "${DAYTONA_API_KEY}"

# 2. Create a new Daytona sandbox
# Use the sandbox name sb-${ZEALT_RUN_ID}
daytona create --name "${SANDBOX_NAME}"

# 3. Determine the resulting sandbox ID
# List sandboxes in JSON format and extract the ID matching the name
# We use jq to parse the JSON output
# The CLI is expected to return an object with an "items" array
SANDBOX_ID=$(daytona list --format json | jq -r ".items[] | select(.name == \"${SANDBOX_NAME}\") | .id")

# Check if SANDBOX_ID was found
if [ -z "${SANDBOX_ID}" ] || [ "${SANDBOX_ID}" == "null" ]; then
    echo "Error: Could not find sandbox ID for ${SANDBOX_NAME}" >&2
    exit 1
fi

# 4. Write the discovered sandbox ID to the log file in fixed format
# Truncate/overwrite the file
echo "Sandbox ID: ${SANDBOX_ID}" > "${LOG_FILE}"
