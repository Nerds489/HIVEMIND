#!/bin/bash
#
# Spawner wrapper for agents

set -euo pipefail

HIVEMIND_ROOT="${HIVEMIND_ROOT:-$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")" && pwd)}"

spawn_agent() {
  local agent_type="$1"
  local task="$2"
  "$HIVEMIND_ROOT/bin/spawn-agent" "$agent_type" "$task"
}

export -f spawn_agent

