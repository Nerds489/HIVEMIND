#!/usr/bin/env bash
#===============================================================================
# HIVEMIND v3.0 Installation Script
# TUI-Only Mode - DO NOT RUN WITH SUDO
#===============================================================================

set -euo pipefail

# Prevent running as root
if [[ $EUID -eq 0 ]]; then
    echo "ERROR: Do not run this script with sudo!"
    echo "Run as your normal user: ./install.sh"
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
echo "║                    HIVEMIND v3.0 INSTALLER                    ║"
echo "║                      TUI-Only Mode                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Determine installation directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HIVEMIND_HOME="${HIVEMIND_HOME:-$HOME/.local/share/hivemind}"
USER_BIN="${HOME}/.local/bin"

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        if [[ $(echo "$PYTHON_VERSION >= 3.11" | bc -l 2>/dev/null || echo 0) -eq 1 ]] || \
           [[ "$PYTHON_VERSION" > "3.10" ]]; then
            log_info "Python $PYTHON_VERSION found"
            return 0
        fi
    fi
    log_error "Python 3.11+ required. Install with: sudo dnf install python3.11"
    return 1
}

check_codex() {
    if command -v codex &> /dev/null; then
        log_info "Codex CLI found: $(which codex)"
        return 0
    fi
    log_warn "Codex CLI not found. Install with: npm install -g @openai/codex"
    return 1
}

check_claude() {
    if command -v claude &> /dev/null; then
        log_info "Claude CLI found: $(which claude)"
        return 0
    fi
    log_warn "Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"
    return 1
}

install_to_home() {
    log_info "Installing HIVEMIND to $HIVEMIND_HOME..."

    # Create directories
    mkdir -p "$HIVEMIND_HOME"
    mkdir -p "$USER_BIN"
    mkdir -p "$HIVEMIND_HOME/memory/sessions"
    mkdir -p "$HIVEMIND_HOME/memory/dialogue"
    mkdir -p "$HIVEMIND_HOME/memory/global"
    mkdir -p "$HIVEMIND_HOME/workspace"
    mkdir -p "$HIVEMIND_HOME/logs"

    # Copy files (excluding .git and __pycache__)
    rsync -av --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
          --exclude='bin/' --exclude='backend/' --exclude='.claude/commands/' \
          "$SCRIPT_DIR/" "$HIVEMIND_HOME/"

    # Create launcher script
    cat > "$USER_BIN/hivemind" << 'LAUNCHER'
#!/usr/bin/env bash
#===============================================================================
# HIVEMIND Launcher - Runs from any directory
#===============================================================================

HIVEMIND_HOME="${HIVEMIND_HOME:-$HOME/.local/share/hivemind}"

if [[ ! -d "$HIVEMIND_HOME" ]]; then
    echo "Error: HIVEMIND not installed at $HIVEMIND_HOME"
    echo "Run the installer first."
    exit 1
fi

# Store launch directory for context
export HIVEMIND_LAUNCH_DIR="$(pwd)"

# Change to TUI directory and run
cd "$HIVEMIND_HOME/tui"

# Install dependencies if needed
if [[ ! -d ".venv" ]]; then
    echo "Setting up Python environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q -e .
else
    source .venv/bin/activate
fi

# Run TUI
exec python -m hivemind_tui "$@"
LAUNCHER

    chmod +x "$USER_BIN/hivemind"
    log_info "Created launcher: $USER_BIN/hivemind"
}

setup_path() {
    local shell_rc=""

    if [[ -n "${BASH_VERSION:-}" ]]; then
        shell_rc="$HOME/.bashrc"
    elif [[ -n "${ZSH_VERSION:-}" ]]; then
        shell_rc="$HOME/.zshrc"
    fi

    if [[ -n "$shell_rc" ]] && [[ -f "$shell_rc" ]]; then
        if ! grep -q 'HIVEMIND PATH' "$shell_rc"; then
            cat >> "$shell_rc" << 'PATHBLOCK'

# >>> HIVEMIND PATH >>>
if [[ -d "$HOME/.local/bin" ]] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    export PATH="$HOME/.local/bin:$PATH"
fi
# <<< HIVEMIND PATH <<<
PATHBLOCK
            log_info "Added PATH to $shell_rc"
        fi
    fi
}

install_tui_deps() {
    log_info "Installing TUI dependencies..."

    cd "$HIVEMIND_HOME/tui"

    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
    fi

    source .venv/bin/activate
    pip install -q -e .

    log_info "TUI dependencies installed"
}

# Main installation
echo ""
log_info "Checking prerequisites..."
check_python || exit 1

echo ""
log_info "Checking AI engines..."
check_codex || true
check_claude || true

echo ""
install_to_home

echo ""
setup_path

echo ""
install_tui_deps

echo ""
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              HIVEMIND INSTALLATION COMPLETE!                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "To start HIVEMIND:"
echo ""
echo "  1. Open a new terminal (or run: source ~/.bashrc)"
echo "  2. Run: hivemind"
echo ""
echo "HIVEMIND works from any directory!"
echo ""
echo "First run will prompt for authentication."
echo ""
