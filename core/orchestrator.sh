#!/bin/bash
#
# Main orchestrator entrypoint (shell implementation)

set -euo pipefail

HIVEMIND_ROOT="${HIVEMIND_ROOT:-$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")" && pwd)}"

run_orchestrator() {
  local task="$1"
  "$HIVEMIND_ROOT/hivemind" "$task"
}

export -f run_orchestrator

