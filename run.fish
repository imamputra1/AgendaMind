#!/usr/bin/env fish

set -l SCRIPT_DIR (dirname (realpath (status --current-filename)))
set -l HOST_OBSIDIAN /home/bumip/Documents/Agent_Command_Center
set -l HOST_SANDBOX $SCRIPT_DIR/sandbox
set -l CTR_OBSIDIAN /app/obsidian_hub
set -l CTR_SANDBOX /app/sandbox

mkdir -p $HOST_SANDBOX

exec podman run --rm -it \
    --userns=keep-id \
    --network=host \
    -v "$HOST_OBSIDIAN:$CTR_OBSIDIAN:Z" \
    -v "$HOST_SANDBOX:$CTR_SANDBOX:Z" \
    personal-agent:latest $argv
