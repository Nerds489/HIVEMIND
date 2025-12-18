#!/bin/bash
#
# Routing helper (minimal)

set -euo pipefail

HIVEMIND_ROOT="${HIVEMIND_ROOT:-$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")" && pwd)}"

route_task() {
  local task="$1"
  # Placeholder: routing rules live in config/routing.yaml; orchestration is handled by the engine prompt.
  echo "$task" >/dev/null
}

export -f route_task

