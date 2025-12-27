#!/usr/bin/env bash
#===============================================================================
# HIVEMIND v3.0 Uninstall Script
#===============================================================================

set -euo pipefail

# Prevent running as root
if [[ $EUID -eq 0 ]]; then
    echo "ERROR: Do not run this script with sudo!"
    echo "Run as your normal user: ./uninstall.sh"
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                   HIVEMIND v3.0 UNINSTALLER                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Paths
HIVEMIND_HOME="${HIVEMIND_HOME:-$HOME/.local/share/hivemind}"
USER_BIN="${HOME}/.local/bin"
CONFIG_DIR="${HOME}/.config/hivemind"

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

remove_path_block() {
    local shell_rc="$1"
    if [[ -f "$shell_rc" ]] && grep -q 'HIVEMIND PATH' "$shell_rc"; then
        awk '
            /# >>> HIVEMIND PATH >>>/ {skip=1; next}
            /# <<< HIVEMIND PATH <<</ {skip=0; next}
            !skip {print}
        ' "$shell_rc" > "${shell_rc}.tmp"
        mv "${shell_rc}.tmp" "$shell_rc"
        log_info "Removed PATH block from $shell_rc"
    fi
}

echo ""
log_info "Removing launcher..."
if [[ -f "$USER_BIN/hivemind" ]]; then
    rm -f "$USER_BIN/hivemind"
    log_info "Removed $USER_BIN/hivemind"
else
    log_warn "Launcher not found at $USER_BIN/hivemind"
fi

echo ""
log_info "Removing installation directory..."
if [[ -d "$HIVEMIND_HOME" ]]; then
    rm -rf "$HIVEMIND_HOME"
    log_info "Removed $HIVEMIND_HOME"
else
    log_warn "Install directory not found at $HIVEMIND_HOME"
fi

echo ""
log_info "Removing config directory..."
if [[ -d "$CONFIG_DIR" ]]; then
    rm -rf "$CONFIG_DIR"
    log_info "Removed $CONFIG_DIR"
else
    log_warn "Config directory not found at $CONFIG_DIR"
fi

echo ""
log_info "Cleaning PATH entries..."
remove_path_block "$HOME/.bashrc"
remove_path_block "$HOME/.zshrc"

echo ""
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              HIVEMIND UNINSTALL COMPLETE                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "If you opened a new terminal for PATH changes, close and reopen it."
echo ""
