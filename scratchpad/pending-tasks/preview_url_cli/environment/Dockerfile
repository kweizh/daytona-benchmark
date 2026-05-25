FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep jq && \
    pip3 install --break-system-packages pytest-json-ctrf && \
    DAYTONA_ARCH=$(dpkg --print-architecture) && \
    case "$DAYTONA_ARCH" in \
        amd64) DAYTONA_ASSET=daytona-linux-amd64 ;; \
        arm64) DAYTONA_ASSET=daytona-linux-arm64 ;; \
        *) echo "Unsupported architecture: $DAYTONA_ARCH" >&2 && exit 1 ;; \
    esac && \
    curl -fsSL "https://github.com/daytonaio/daytona/releases/download/v0.180.0/${DAYTONA_ASSET}" -o /usr/local/bin/daytona && \
    chmod +x /usr/local/bin/daytona && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user
RUN mkdir -p /home/user/myproject

LABEL Author="generate-harbor-tasks"
LABEL Description="Daytona CLI task environment for generating signed preview URLs from a sandbox HTTP server."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

# Container contents:
#   - always required apt packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep
#   - extra apt packages: jq (for JSON parsing of Daytona CLI output)
#   - always required pip3 packages: pytest-json-ctrf
#   - Daytona CLI v0.180.0 binary installed at /usr/local/bin/daytona
#   - /home/user/myproject: working directory for the task
