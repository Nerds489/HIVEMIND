#!/bin/bash
#
# HIVEMIND Launcher
# Sources environment and starts HIVEMIND
#

HIVEMIND_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HIVEMIND_ROOT

# Source environment file if exists
if [[ -f "$HIVEMIND_ROOT/.env" ]]; then
    set -a
    source "$HIVEMIND_ROOT/.env"
    set +a
fi

# Ensure PATH includes npm global and local bin
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"

# Launch HIVEMIND
exec "$HIVEMIND_ROOT/hivemind" "$@"
