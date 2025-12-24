#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# HIVEMIND Upgrade Installer
# ═══════════════════════════════════════════════════════════════════════════════
# Installs the upgrade package into an existing HIVEMIND installation
# Usage: ./install-upgrade.sh [HIVEMIND_PATH]
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

RED=$'\033[0;31m'
GRN=$'\033[0;32m'
CYN=$'\033[0;36m'
WHT=$'\033[1;37m'
RST=$'\033[0m'

echo -e "${CYN}"
cat << 'BANNER'
╔═══════════════════════════════════════════════════════════╗
║           HIVEMIND UPGRADE INSTALLER                      ║
║      Complete Agent Profiles + Extended Commands          ║
╚═══════════════════════════════════════════════════════════╝
BANNER
echo -e "${RST}"

# Get paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPGRADE_ROOT="${SCRIPT_DIR%/*}"

# Determine HIVEMIND location
if [[ -n "${1:-}" ]]; then
    HIVEMIND_ROOT="$1"
elif [[ -d "$HOME/HIVEMIND" ]]; then
    HIVEMIND_ROOT="$HOME/HIVEMIND"
elif [[ -d "$HOME/Desktop/HIVEMIND" ]]; then
    HIVEMIND_ROOT="$HOME/Desktop/HIVEMIND"
else
    echo -e "${RED}Error: HIVEMIND not found${RST}"
    echo "Usage: $0 [/path/to/HIVEMIND]"
    exit 1
fi

echo -e "Upgrade source: ${WHT}$UPGRADE_ROOT${RST}"
echo -e "Target HIVEMIND: ${WHT}$HIVEMIND_ROOT${RST}"
echo ""

# Verify HIVEMIND exists
if [[ ! -f "$HIVEMIND_ROOT/hivemind" ]]; then
    echo -e "${RED}Error: Not a valid HIVEMIND installation${RST}"
    echo "Missing: $HIVEMIND_ROOT/hivemind"
    exit 1
fi

# Confirm
echo -e "${CYN}This will install:${RST}"
echo "  • 20 agent memory profiles"
echo "  • 3 new slash commands"
echo "  • Health check script"
echo "  • Documentation updates"
echo ""
read -p "Continue? [y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""

# Install memory profiles
echo -e "${CYN}Installing agent memory profiles...${RST}"
for dir in "$UPGRADE_ROOT/memory/agents"/*; do
    if [[ -d "$dir" ]]; then
        agent_id=$(basename "$dir")
        target_dir="$HIVEMIND_ROOT/memory/agents/$agent_id"
        mkdir -p "$target_dir"
        cp "$dir/_memory.json" "$target_dir/" 2>/dev/null && \
            echo -e "  ${GRN}✓${RST} $agent_id" || \
            echo -e "  ${RED}✗${RST} $agent_id (failed)"
    fi
done

# Install commands
echo -e "${CYN}Installing slash commands...${RST}"
mkdir -p "$HIVEMIND_ROOT/.claude/commands"
for cmd in "$UPGRADE_ROOT/commands"/*.md; do
    if [[ -f "$cmd" ]]; then
        name=$(basename "$cmd")
        cp "$cmd" "$HIVEMIND_ROOT/.claude/commands/" && \
            echo -e "  ${GRN}✓${RST} $name" || \
            echo -e "  ${RED}✗${RST} $name (failed)"
    fi
done

# Install scripts
echo -e "${CYN}Installing scripts...${RST}"
mkdir -p "$HIVEMIND_ROOT/scripts"
for script in "$UPGRADE_ROOT/scripts"/*.sh; do
    if [[ -f "$script" ]]; then
        name=$(basename "$script")
        cp "$script" "$HIVEMIND_ROOT/scripts/"
        chmod +x "$HIVEMIND_ROOT/scripts/$name"
        echo -e "  ${GRN}✓${RST} $name"
    fi
done

# Install docs
echo -e "${CYN}Installing documentation...${RST}"
mkdir -p "$HIVEMIND_ROOT/docs"
for doc in "$UPGRADE_ROOT/docs"/*.md; do
    if [[ -f "$doc" ]]; then
        name=$(basename "$doc")
        cp "$doc" "$HIVEMIND_ROOT/docs/" && \
            echo -e "  ${GRN}✓${RST} $name"
    fi
done

# Install extras
echo -e "${CYN}Installing extras...${RST}"
for extra in "$UPGRADE_ROOT/extras"/*.md; do
    if [[ -f "$extra" ]]; then
        name=$(basename "$extra")
        cp "$extra" "$HIVEMIND_ROOT/docs/" && \
            echo -e "  ${GRN}✓${RST} $name"
    fi
done

echo ""
echo -e "${GRN}═══════════════════════════════════════════════════════════════${RST}"
echo -e "${GRN}           UPGRADE COMPLETE!${RST}"
echo -e "${GRN}═══════════════════════════════════════════════════════════════${RST}"
echo ""
echo -e "Run health check: ${WHT}$HIVEMIND_ROOT/scripts/health-check.sh${RST}"
echo ""
echo -e "New commands available:"
echo -e "  ${CYN}/status${RST}  - System status"
echo -e "  ${CYN}/recall${RST}  - Query memory"
echo -e "  ${CYN}/debug${RST}   - Troubleshooting"
echo ""
