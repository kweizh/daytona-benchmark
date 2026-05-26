#!/bin/bash
set -e

# Read environment variables
API_KEY=$DAYTONA_API_KEY
RUN_ID=$ZEALT_RUN_ID
SANDBOX_NAME="prev-${RUN_ID}"
PROJECT_DIR="/home/user/myproject"
LOG_FILE="${PROJECT_DIR}/output.log"
RESPONSE_FILE="${PROJECT_DIR}/preview-response.txt"

mkdir -p "$PROJECT_DIR"

echo "Logging in to Daytona..."
daytona login --api-key "$API_KEY"

echo "Creating sandbox ${SANDBOX_NAME}..."
daytona delete "$SANDBOX_NAME" > /dev/null 2>&1 || true
daytona create --name "$SANDBOX_NAME"

echo "Waiting for sandbox to be ready..."
sleep 30

echo "Starting HTTP server inside sandbox..."
# Using direct command string to avoid host shell interference with redirection
daytona exec "$SANDBOX_NAME" "echo HELLO_${RUN_ID} > index.html && (nohup python3 -m http.server 8000 > server.log 2>&1 &)"

echo "Waiting for server to initialize..."
sleep 10

echo "Obtaining preview URL..."
# Extract URL only, ignoring potential warnings or extra text
PREVIEW_URL=$(daytona preview-url "$SANDBOX_NAME" --port 8000 | grep 'https://' | head -n 1 | tr -d '\r\n')

echo "Preview URL: $PREVIEW_URL" > "$LOG_FILE"
echo "Preview URL: $PREVIEW_URL"

echo "Fetching content from preview URL..."
curl -sL "$PREVIEW_URL" > "$RESPONSE_FILE"

echo "Content of response:"
cat "$RESPONSE_FILE"

echo "Script execution finished."
