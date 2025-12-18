#!/bin/bash
#
# HIVEMIND Installation

set -euo pipefail

HIVEMIND_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing HIVEMIND..."

check_dep() {
    if ! command -v "$1" &> /dev/null; then
        echo "Warning: $1 not found. Install it for $2 support."
        return 1
    fi
    return 0
}

echo "Checking engines..."
check_dep "codex" "Codex CLI" || true
check_dep "claude" "Claude Code CLI" || true

chmod +x "$HIVEMIND_ROOT/hivemind"
chmod +x "$HIVEMIND_ROOT/engines/"*.sh
chmod +x "$HIVEMIND_ROOT/bin/"*
chmod +x "$HIVEMIND_ROOT/core/"*.sh

mkdir -p "$HIVEMIND_ROOT/memory/global"
mkdir -p "$HIVEMIND_ROOT/memory/sessions"
mkdir -p "$HIVEMIND_ROOT/memory/agents"
mkdir -p "$HIVEMIND_ROOT/memory/long-term"
mkdir -p "$HIVEMIND_ROOT/memory/episodic"
mkdir -p "$HIVEMIND_ROOT/workspace"
mkdir -p "$HIVEMIND_ROOT/logs"

# Initialize memory (non-destructive)
[[ -f "$HIVEMIND_ROOT/memory/global/context.json" ]] || echo '{}' > "$HIVEMIND_ROOT/memory/global/context.json"
[[ -f "$HIVEMIND_ROOT/memory/global/learnings.json" ]] || echo '{"entries":[]}' > "$HIVEMIND_ROOT/memory/global/learnings.json"
[[ -f "$HIVEMIND_ROOT/memory/global/preferences.json" ]] || echo '{"entries":[]}' > "$HIVEMIND_ROOT/memory/global/preferences.json"

# Initialize memory files with proper structure (non-destructive)
[[ -f "$HIVEMIND_ROOT/memory/long-term/learnings.json" ]] || echo '{"version":"1.0","entries":[]}' > "$HIVEMIND_ROOT/memory/long-term/learnings.json"
[[ -f "$HIVEMIND_ROOT/memory/long-term/preferences.json" ]] || echo '{"version":"1.0","user_preferences":{"communication_style":null,"detail_level":"standard","code_style":{"language":null,"indentation":"spaces","indent_size":2},"rules":[]}}' > "$HIVEMIND_ROOT/memory/long-term/preferences.json"
[[ -f "$HIVEMIND_ROOT/memory/long-term/decisions.json" ]] || echo '{"version":"1.0","decisions":[]}' > "$HIVEMIND_ROOT/memory/long-term/decisions.json"
[[ -f "$HIVEMIND_ROOT/memory/long-term/project.json" ]] || echo '{"version":"1.0","project":{"name":null,"description":null,"tech_stack":[],"tools":[],"conventions":[],"architecture":null}}' > "$HIVEMIND_ROOT/memory/long-term/project.json"
[[ -f "$HIVEMIND_ROOT/memory/episodic/events.json" ]] || echo '{"version":"1.0","events":[]}' > "$HIVEMIND_ROOT/memory/episodic/events.json"

# Optional symlink to PATH (best-effort)
if [[ -d "/usr/local/bin" ]]; then
    if command -v sudo &> /dev/null; then
        sudo ln -sf "$HIVEMIND_ROOT/hivemind" /usr/local/bin/hivemind || true
        if [[ -L "/usr/local/bin/hivemind" ]]; then
            echo "Installed: /usr/local/bin/hivemind"
        fi
    else
        echo "Note: sudo not available; skipping /usr/local/bin symlink."
        echo "Run from repo root with: ./hivemind"
    fi
fi

# Create hm alias
if [[ -d "/usr/local/bin" ]]; then
    if command -v sudo &> /dev/null; then
        sudo ln -sf "$HIVEMIND_ROOT/bin/hm" /usr/local/bin/hm || true
    else
        ln -sf "$HIVEMIND_ROOT/bin/hm" /usr/local/bin/hm 2>/dev/null || true
    fi
fi

echo ""
echo "═══════════════════════════════════════════"
echo "        HIVEMIND INSTALLATION COMPLETE     "
echo "═══════════════════════════════════════════"
echo ""
echo "Usage:"
echo "  ./hivemind                  # Interactive mode"
echo "  ./hivemind \"task\"           # Direct task"
echo "  ./hivemind --config         # Show configuration"
echo "  ./hivemind --preset full-codex  # Switch engines"
echo ""
echo "Default configuration:"
echo "  HIVEMIND engine: codex"
echo "  Agent engine:    claude-code"
echo ""
echo "Run './hivemind' to start."
