#!/usr/bin/env fish
set -l HOST_OBSIDIAN /home/bumip/Documents/Agent_Command_Center
set -l HOST_SANDBOX (pwd)/sandbox
set -l CTR_OBSIDIAN /app/obsidian_hub
set -l CTR_SANDBOX /app/sandbox

podman run --rm -it \
  --network=host \
  --userns=keep-id \
  -v "$HOST_OBSIDIAN:$CTR_OBSIDIAN:Z" \
  -v "$HOST_SANDBOX:$CTR_SANDBOX:Z" \
  personal-agent:latest
