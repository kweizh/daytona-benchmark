FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep jq && \
    pip3 install --break-system-packages pytest-json-ctrf && \
    ARCH="$(dpkg --print-architecture)" && \
    case "$ARCH" in \
        amd64) DAYTONA_ARCH=amd64 ;; \
        arm64) DAYTONA_ARCH=arm64 ;; \
        *) echo "Unsupported arch: $ARCH" >&2; exit 1 ;; \
    esac && \
    curl -fsSL -o /usr/local/bin/daytona \
        "https://github.com/daytonaio/daytona/releases/download/v0.180.0/daytona-linux-${DAYTONA_ARCH}" && \
    chmod +x /usr/local/bin/daytona && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user
RUN mkdir -p /home/user/myproject

LABEL Author="generate-harbor-tasks"
LABEL Description="Daytona CLI environment for exercising the sandbox lifecycle (login, create, info, delete) against Daytona SaaS."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

# Container contents:
#   - always required apt packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep
#   - additional apt packages: jq (for parsing JSON output from daytona info/list)
#   - always required pip3 packages: pytest-json-ctrf
#   - Daytona CLI v0.180.0 binary installed at /usr/local/bin/daytona (linux-amd64 release)
#   - /home/user/myproject: empty project directory used for log file output
