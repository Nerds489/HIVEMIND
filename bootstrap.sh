#!/bin/bash
#
# HIVEMIND Quick Bootstrap
# Run this once to set everything up
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/yourusername/HIVEMIND/main/bootstrap.sh | bash
#   OR
#   ./bootstrap.sh
#

set -euo pipefail

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              HIVEMIND Quick Bootstrap                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Determine HIVEMIND root
if [[ -f "./setup.sh" ]]; then
    HIVEMIND_ROOT="$(pwd)"
elif [[ -f "$(dirname "$0")/setup.sh" ]]; then
    HIVEMIND_ROOT="$(cd "$(dirname "$0")" && pwd)"
else
    echo "Error: Cannot find HIVEMIND directory."
    echo "Please run this from the HIVEMIND directory."
    exit 1
fi

cd "$HIVEMIND_ROOT"

# Make setup script executable
chmod +x setup.sh

# Run full setup
exec ./setup.sh "$@"
