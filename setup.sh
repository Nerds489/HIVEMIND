#!/bin/bash
#
# ██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗ 
# ██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
# ███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
# ██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
# ██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
# ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ 
#
# HIVEMIND Complete Setup Script
# Installs everything, configures everything, authenticates everything
#
# Usage: ./setup.sh [--unattended] [--codex-key KEY] [--claude-key KEY]
#

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

HIVEMIND_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HIVEMIND_ROOT

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# State tracking
NODEJS_INSTALLED=false
NPM_INSTALLED=false
CODEX_INSTALLED=false
CLAUDE_INSTALLED=false
CODEX_AUTHENTICATED=false
CLAUDE_AUTHENTICATED=false

# CLI arguments
UNATTENDED=false
CODEX_API_KEY=""
CLAUDE_API_KEY=""
SKIP_AUTH=false

# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT PARSING
# ═══════════════════════════════════════════════════════════════════════════════

while [[ $# -gt 0 ]]; do
    case "$1" in
        --unattended|-y)
            UNATTENDED=true
            shift
            ;;
        --codex-key)
            CODEX_API_KEY="$2"
            shift 2
            ;;
        --claude-key)
            CLAUDE_API_KEY="$2"
            shift 2
            ;;
        --skip-auth)
            SKIP_AUTH=true
            shift
            ;;
        --help|-h)
            cat << 'EOF'
HIVEMIND Complete Setup Script

Usage: ./setup.sh [OPTIONS]

Options:
  --unattended, -y     Run without prompts (use with --codex-key and --claude-key)
  --codex-key KEY      OpenAI API key for Codex authentication
  --claude-key KEY     Anthropic API key for Claude authentication
  --skip-auth          Skip authentication (configure later)
  --help, -h           Show this help message

Examples:
  ./setup.sh                                    # Interactive setup
  ./setup.sh --codex-key sk-xxx --claude-key sk-ant-xxx  # With API keys
  ./setup.sh --unattended --skip-auth           # Install only, auth later

EOF
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}" >&2
            exit 1
            ;;
    esac
done

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

log_step() {
    echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${BLUE}▶ $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✔${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✖${NC} $1"
}

log_dim() {
    echo -e "${DIM}  $1${NC}"
}

prompt_yes_no() {
    local prompt="$1"
    local default="${2:-y}"
    
    if [[ "$UNATTENDED" == "true" ]]; then
        [[ "$default" == "y" ]] && return 0 || return 1
    fi
    
    local yn_hint="[Y/n]"
    [[ "$default" == "n" ]] && yn_hint="[y/N]"
    
    while true; do
        read -rp "$(echo -e "${PURPLE}?${NC} $prompt $yn_hint: ")" yn
        yn="${yn:-$default}"
        case "${yn,,}" in
            y|yes) return 0 ;;
            n|no) return 1 ;;
            *) echo "Please answer yes or no." ;;
        esac
    done
}

prompt_choice() {
    local prompt="$1"
    shift
    local options=("$@")
    
    echo -e "\n${PURPLE}?${NC} $prompt"
    for i in "${!options[@]}"; do
        echo -e "  ${BOLD}$((i+1)))${NC} ${options[$i]}"
    done
    
    while true; do
        read -rp "$(echo -e "${PURPLE}>${NC} Selection [1-${#options[@]}]: ")" choice
        if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#options[@]} )); then
            return $((choice - 1))
        fi
        echo "Invalid selection. Please enter a number between 1 and ${#options[@]}."
    done
}

prompt_secret() {
    local prompt="$1"
    local var_name="$2"
    
    read -rsp "$(echo -e "${PURPLE}?${NC} $prompt: ")" secret
    echo
    eval "$var_name=\"\$secret\""
}

command_exists() {
    command -v "$1" &> /dev/null
}

find_executable() {
    local name="$1"
    
    # Check PATH first
    local from_path
    from_path="$(command -v "$name" 2>/dev/null || true)"
    if [[ -n "$from_path" ]]; then
        echo "$from_path"
        return 0
    fi
    
    # Common locations
    local candidates=(
        "$HOME/.local/bin/$name"
        "$HOME/.npm-global/bin/$name"
        "$HOME/.cargo/bin/$name"
        "$HOME/.bun/bin/$name"
        "$HOME/.volta/bin/$name"
        "$HOME/.asdf/shims/$name"
        "/usr/local/bin/$name"
        "/usr/bin/$name"
    )
    
    # NVM locations
    if [[ -d "$HOME/.nvm/versions/node" ]]; then
        local best
        best="$(ls -1d "$HOME/.nvm/versions/node"/v*/bin/"$name" 2>/dev/null | sort -V | tail -n 1 || true)"
        [[ -n "$best" ]] && candidates+=("$best")
    fi
    
    # fnm locations
    if [[ -d "$HOME/.local/share/fnm/node-versions" ]]; then
        local best
        best="$(ls -1d "$HOME/.local/share/fnm/node-versions"/v*/installation/bin/"$name" 2>/dev/null | sort -V | tail -n 1 || true)"
        [[ -n "$best" ]] && candidates+=("$best")
    fi
    
    for p in "${candidates[@]}"; do
        if [[ -x "$p" ]]; then
            echo "$p"
            return 0
        fi
    done
    
    return 1
}

get_os() {
    case "$(uname -s)" in
        Linux*)  echo "linux" ;;
        Darwin*) echo "macos" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)       echo "unknown" ;;
    esac
}

get_arch() {
    case "$(uname -m)" in
        x86_64|amd64) echo "x64" ;;
        aarch64|arm64) echo "arm64" ;;
        armv7l) echo "arm" ;;
        *) echo "unknown" ;;
    esac
}

ensure_path_entry() {
    local dir="$1"
    
    if [[ ":$PATH:" != *":$dir:"* ]]; then
        export PATH="$dir:$PATH"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════════════════════

show_banner() {
    clear 2>/dev/null || true
    echo -e "${CYAN}"
    cat << 'EOF'
    ██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗ 
    ██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
    ███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
    ██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
    ██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
    ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ 
EOF
    echo -e "${NC}"
    echo -e "${BOLD}        Neural Multi-Agent Orchestration System${NC}"
    echo -e "${DIM}              Complete Setup & Configuration${NC}"
    echo ""
    echo -e "${YELLOW}    This installer will:${NC}"
    echo -e "    ${GREEN}✔${NC} Install Node.js (if needed)"
    echo -e "    ${GREEN}✔${NC} Install Codex CLI (OpenAI)"
    echo -e "    ${GREEN}✔${NC} Install Claude Code CLI (Anthropic)"
    echo -e "    ${GREEN}✔${NC} Configure PATH and environment"
    echo -e "    ${GREEN}✔${NC} Authenticate both engines"
    echo -e "    ${GREEN}✔${NC} Set up HIVEMIND directories"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: DETECT SYSTEM STATE
# ═══════════════════════════════════════════════════════════════════════════════

detect_system() {
    log_step "Detecting System State"
    
    local os=$(get_os)
    local arch=$(get_arch)
    log_info "Operating System: ${BOLD}$os${NC} (${arch})"
    
    # Check Node.js
    if command_exists node; then
        local node_version=$(node --version 2>/dev/null || echo "unknown")
        log_success "Node.js: ${GREEN}$node_version${NC}"
        NODEJS_INSTALLED=true
    else
        log_warning "Node.js: ${YELLOW}Not installed${NC}"
    fi
    
    # Check npm
    if command_exists npm; then
        local npm_version=$(npm --version 2>/dev/null || echo "unknown")
        log_success "npm: ${GREEN}v$npm_version${NC}"
        NPM_INSTALLED=true
    else
        log_warning "npm: ${YELLOW}Not installed${NC}"
    fi
    
    # Check Codex
    local codex_path
    codex_path="$(find_executable codex 2>/dev/null || true)"
    if [[ -n "$codex_path" ]]; then
        log_success "Codex CLI: ${GREEN}$codex_path${NC}"
        CODEX_INSTALLED=true
        
        # Check auth status
        if "$codex_path" login status &>/dev/null || [[ -n "${OPENAI_API_KEY:-}" ]]; then
            log_success "Codex Auth: ${GREEN}Authenticated${NC}"
            CODEX_AUTHENTICATED=true
        else
            log_warning "Codex Auth: ${YELLOW}Not authenticated${NC}"
        fi
    else
        log_warning "Codex CLI: ${YELLOW}Not installed${NC}"
    fi
    
    # Check Claude
    local claude_path
    claude_path="$(find_executable claude 2>/dev/null || true)"
    if [[ -n "$claude_path" ]]; then
        log_success "Claude CLI: ${GREEN}$claude_path${NC}"
        CLAUDE_INSTALLED=true
        
        # Check auth status
        if [[ -n "${ANTHROPIC_API_KEY:-}" ]] || [[ -n "${CLAUDE_API_KEY:-}" ]] || [[ -f "$HOME/.claude/.credentials.json" ]]; then
            log_success "Claude Auth: ${GREEN}Authenticated${NC}"
            CLAUDE_AUTHENTICATED=true
        else
            log_warning "Claude Auth: ${YELLOW}Not authenticated${NC}"
        fi
    else
        log_warning "Claude CLI: ${YELLOW}Not installed${NC}"
    fi
    
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: INSTALL NODE.JS (IF NEEDED)
# ═══════════════════════════════════════════════════════════════════════════════

install_nodejs() {
    if [[ "$NODEJS_INSTALLED" == "true" ]] && [[ "$NPM_INSTALLED" == "true" ]]; then
        return 0
    fi
    
    log_step "Installing Node.js"
    
    local os=$(get_os)
    
    case "$os" in
        linux)
            log_info "Detected Linux - Installing via NodeSource or package manager..."
            
            if command_exists apt-get; then
                # Debian/Ubuntu
                log_info "Using apt package manager"
                
                if prompt_yes_no "Install Node.js 20.x LTS via NodeSource?"; then
                    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
                    sudo apt-get install -y nodejs
                else
                    sudo apt-get update
                    sudo apt-get install -y nodejs npm
                fi
                
            elif command_exists dnf; then
                # Fedora/RHEL
                log_info "Using dnf package manager"
                sudo dnf install -y nodejs npm
                
            elif command_exists pacman; then
                # Arch Linux
                log_info "Using pacman package manager"
                sudo pacman -S --noconfirm nodejs npm
                
            elif command_exists zypper; then
                # openSUSE
                log_info "Using zypper package manager"
                sudo zypper install -y nodejs npm
                
            else
                log_warning "Unknown package manager. Installing via fnm..."
                install_nodejs_fnm
            fi
            ;;
            
        macos)
            log_info "Detected macOS"
            
            if command_exists brew; then
                log_info "Installing via Homebrew..."
                brew install node
            else
                log_warning "Homebrew not found. Installing via fnm..."
                install_nodejs_fnm
            fi
            ;;
            
        *)
            log_error "Unsupported OS: $os"
            log_info "Please install Node.js manually: https://nodejs.org/"
            exit 1
            ;;
    esac
    
    # Verify installation
    if command_exists node && command_exists npm; then
        NODEJS_INSTALLED=true
        NPM_INSTALLED=true
        log_success "Node.js installed: $(node --version)"
        log_success "npm installed: v$(npm --version)"
    else
        log_error "Node.js installation failed"
        exit 1
    fi
}

install_nodejs_fnm() {
    log_info "Installing fnm (Fast Node Manager)..."
    
    curl -fsSL https://fnm.vercel.app/install | bash -s -- --skip-shell
    
    export FNM_DIR="$HOME/.local/share/fnm"
    export PATH="$FNM_DIR:$PATH"
    
    # Source fnm
    eval "$(~/.local/share/fnm/fnm env)"
    
    # Install Node.js LTS
    fnm install --lts
    fnm use lts-latest
    fnm default lts-latest
    
    NODEJS_INSTALLED=true
    NPM_INSTALLED=true
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: CONFIGURE NPM FOR USER-LOCAL INSTALLS
# ═══════════════════════════════════════════════════════════════════════════════

configure_npm() {
    log_step "Configuring npm for User-Local Installs"
    
    # Create user npm directory
    local npm_global="$HOME/.npm-global"
    mkdir -p "$npm_global"
    
    # Configure npm to use it
    npm config set prefix "$npm_global"
    
    # Add to PATH
    ensure_path_entry "$npm_global/bin"
    
    # Update shell config files
    local path_export="export PATH=\"\$HOME/.npm-global/bin:\$PATH\""
    local marker="# HIVEMIND npm PATH"
    
    for rcfile in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
        if [[ -f "$rcfile" ]] || [[ "$rcfile" == "$HOME/.bashrc" ]]; then
            if ! grep -Fq "$marker" "$rcfile" 2>/dev/null; then
                echo "" >> "$rcfile"
                echo "$marker" >> "$rcfile"
                echo "$path_export" >> "$rcfile"
                log_dim "Updated: $rcfile"
            fi
        fi
    done
    
    log_success "npm configured for user-local installs at: $npm_global"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: INSTALL CODEX CLI
# ═══════════════════════════════════════════════════════════════════════════════

install_codex() {
    if [[ "$CODEX_INSTALLED" == "true" ]]; then
        log_info "Codex CLI already installed"
        return 0
    fi
    
    log_step "Installing OpenAI Codex CLI"
    
    log_info "Installing @openai/codex globally..."
    npm install -g @openai/codex
    
    # Rehash and verify
    hash -r 2>/dev/null || true
    
    local codex_path
    codex_path="$(find_executable codex 2>/dev/null || true)"
    
    if [[ -n "$codex_path" ]]; then
        CODEX_INSTALLED=true
        log_success "Codex CLI installed: $codex_path"
    else
        log_error "Codex CLI installation failed"
        log_info "Try running: npm install -g @openai/codex"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: INSTALL CLAUDE CODE CLI
# ═══════════════════════════════════════════════════════════════════════════════

install_claude() {
    if [[ "$CLAUDE_INSTALLED" == "true" ]]; then
        log_info "Claude Code CLI already installed"
        return 0
    fi
    
    log_step "Installing Anthropic Claude Code CLI"
    
    log_info "Installing @anthropic-ai/claude-code globally..."
    npm install -g @anthropic-ai/claude-code
    
    # Rehash and verify
    hash -r 2>/dev/null || true
    
    local claude_path
    claude_path="$(find_executable claude 2>/dev/null || true)"
    
    if [[ -n "$claude_path" ]]; then
        CLAUDE_INSTALLED=true
        log_success "Claude Code CLI installed: $claude_path"
    else
        log_error "Claude Code CLI installation failed"
        log_info "Try running: npm install -g @anthropic-ai/claude-code"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: AUTHENTICATE CODEX
# ═══════════════════════════════════════════════════════════════════════════════

authenticate_codex() {
    if [[ "$SKIP_AUTH" == "true" ]]; then
        log_info "Skipping Codex authentication (--skip-auth)"
        return 0
    fi
    
    if [[ "$CODEX_AUTHENTICATED" == "true" ]]; then
        log_info "Codex already authenticated"
        return 0
    fi
    
    log_step "Authenticating Codex CLI (OpenAI)"
    
    local codex_cmd
    codex_cmd="$(find_executable codex)"
    
    # If API key provided via CLI
    if [[ -n "$CODEX_API_KEY" ]]; then
        log_info "Using provided API key..."
        echo "$CODEX_API_KEY" | "$codex_cmd" login --with-api-key
        CODEX_AUTHENTICATED=true
        save_api_key "OPENAI_API_KEY" "$CODEX_API_KEY"
        log_success "Codex authenticated via API key"
        return 0
    fi
    
    # Interactive authentication
    echo ""
    echo -e "${YELLOW}OpenAI Codex Authentication${NC}"
    echo -e "${DIM}Codex requires an OpenAI account (same as ChatGPT)${NC}"
    echo ""
    
    prompt_choice "Choose authentication method:" \
        "Browser Login (OAuth - recommended)" \
        "API Key (paste key)" \
        "Skip for now"
    local choice=$?
    
    case $choice in
        0)  # Browser OAuth
            log_info "Starting browser authentication..."
            log_info "A browser window will open. Log in with your OpenAI/ChatGPT account."
            echo ""
            "$codex_cmd" login --device-auth
            CODEX_AUTHENTICATED=true
            log_success "Codex authenticated via browser"
            ;;
            
        1)  # API Key
            echo ""
            log_info "Get your API key from: ${BOLD}https://platform.openai.com/api-keys${NC}"
            prompt_secret "Enter your OpenAI API key" CODEX_API_KEY
            
            if [[ -n "$CODEX_API_KEY" ]]; then
                echo "$CODEX_API_KEY" | "$codex_cmd" login --with-api-key
                CODEX_AUTHENTICATED=true
                save_api_key "OPENAI_API_KEY" "$CODEX_API_KEY"
                log_success "Codex authenticated via API key"
            else
                log_warning "No API key provided"
            fi
            ;;
            
        2)  # Skip
            log_warning "Skipping Codex authentication"
            log_info "Run './hivemind --setup' later to authenticate"
            ;;
    esac
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7: AUTHENTICATE CLAUDE
# ═══════════════════════════════════════════════════════════════════════════════

authenticate_claude() {
    if [[ "$SKIP_AUTH" == "true" ]]; then
        log_info "Skipping Claude authentication (--skip-auth)"
        return 0
    fi
    
    if [[ "$CLAUDE_AUTHENTICATED" == "true" ]]; then
        log_info "Claude already authenticated"
        return 0
    fi
    
    log_step "Authenticating Claude Code CLI (Anthropic)"
    
    local claude_cmd
    claude_cmd="$(find_executable claude)"
    
    # If API key provided via CLI
    if [[ -n "$CLAUDE_API_KEY" ]]; then
        log_info "Using provided API key..."
        save_api_key "ANTHROPIC_API_KEY" "$CLAUDE_API_KEY"
        CLAUDE_AUTHENTICATED=true
        log_success "Claude authenticated via API key"
        return 0
    fi
    
    # Interactive authentication
    echo ""
    echo -e "${YELLOW}Anthropic Claude Authentication${NC}"
    echo -e "${DIM}Claude requires an Anthropic account${NC}"
    echo ""
    
    prompt_choice "Choose authentication method:" \
        "Browser Token Setup (recommended)" \
        "API Key (paste key)" \
        "Skip for now"
    local choice=$?
    
    case $choice in
        0)  # Browser token
            log_info "Starting token setup..."
            "$claude_cmd" setup-token
            CLAUDE_AUTHENTICATED=true
            log_success "Claude authenticated via token"
            ;;
            
        1)  # API Key
            echo ""
            log_info "Get your API key from: ${BOLD}https://console.anthropic.com/settings/keys${NC}"
            prompt_secret "Enter your Anthropic API key" CLAUDE_API_KEY
            
            if [[ -n "$CLAUDE_API_KEY" ]]; then
                save_api_key "ANTHROPIC_API_KEY" "$CLAUDE_API_KEY"
                CLAUDE_AUTHENTICATED=true
                log_success "Claude authenticated via API key"
            else
                log_warning "No API key provided"
            fi
            ;;
            
        2)  # Skip
            log_warning "Skipping Claude authentication"
            log_info "Run './hivemind --setup' later to authenticate"
            ;;
    esac
}

save_api_key() {
    local key_name="$1"
    local key_value="$2"
    
    # Create HIVEMIND env file
    local env_file="$HIVEMIND_ROOT/.env"
    
    # Remove existing entry
    if [[ -f "$env_file" ]]; then
        grep -v "^$key_name=" "$env_file" > "$env_file.tmp" 2>/dev/null || true
        mv "$env_file.tmp" "$env_file"
    fi
    
    # Add new entry
    echo "$key_name=\"$key_value\"" >> "$env_file"
    chmod 600 "$env_file"
    
    # Also add to shell rc files for persistence
    local export_line="export $key_name=\"$key_value\""
    local marker="# HIVEMIND $key_name"
    
    for rcfile in "$HOME/.bashrc" "$HOME/.zshrc"; do
        if [[ -f "$rcfile" ]]; then
            # Remove old entry
            grep -v "$marker" "$rcfile" > "$rcfile.tmp" 2>/dev/null || true
            grep -v "^export $key_name=" "$rcfile.tmp" > "$rcfile" 2>/dev/null || true
            rm -f "$rcfile.tmp"
            
            # Add new entry
            echo "" >> "$rcfile"
            echo "$marker" >> "$rcfile"
            echo "$export_line" >> "$rcfile"
        fi
    done
    
    # Export for current session
    export "$key_name"="$key_value"
    
    log_dim "API key saved to: $env_file"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8: CONFIGURE HIVEMIND
# ═══════════════════════════════════════════════════════════════════════════════

configure_hivemind() {
    log_step "Configuring HIVEMIND"
    
    # Make scripts executable
    chmod +x "$HIVEMIND_ROOT/hivemind" 2>/dev/null || true
    chmod +x "$HIVEMIND_ROOT/install.sh" 2>/dev/null || true
    chmod +x "$HIVEMIND_ROOT/setup.sh" 2>/dev/null || true
    find "$HIVEMIND_ROOT/bin" -type f -exec chmod +x {} \; 2>/dev/null || true
    find "$HIVEMIND_ROOT/core" -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
    find "$HIVEMIND_ROOT/engines" -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
    
    log_success "Made scripts executable"
    
    # Create required directories
    local dirs=(
        "memory/global"
        "memory/sessions"
        "memory/agents"
        "memory/long-term"
        "memory/short-term"
        "memory/episodic"
        "memory/teams"
        "memory/projects"
        "workspace"
        "logs"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$HIVEMIND_ROOT/$dir"
    done
    
    log_success "Created directory structure"
    
    # Initialize memory files
    [[ -f "$HIVEMIND_ROOT/memory/global/context.json" ]] || echo '{}' > "$HIVEMIND_ROOT/memory/global/context.json"
    [[ -f "$HIVEMIND_ROOT/memory/global/learnings.json" ]] || echo '{"entries":[]}' > "$HIVEMIND_ROOT/memory/global/learnings.json"
    [[ -f "$HIVEMIND_ROOT/memory/global/preferences.json" ]] || echo '{"entries":[]}' > "$HIVEMIND_ROOT/memory/global/preferences.json"
    
    [[ -f "$HIVEMIND_ROOT/memory/long-term/learnings.json" ]] || echo '{"version":"1.0","entries":[]}' > "$HIVEMIND_ROOT/memory/long-term/learnings.json"
    [[ -f "$HIVEMIND_ROOT/memory/long-term/preferences.json" ]] || echo '{"version":"1.0","user_preferences":{"communication_style":null,"detail_level":"standard","code_style":{"language":null,"indentation":"spaces","indent_size":2},"rules":[]}}' > "$HIVEMIND_ROOT/memory/long-term/preferences.json"
    [[ -f "$HIVEMIND_ROOT/memory/long-term/decisions.json" ]] || echo '{"version":"1.0","decisions":[]}' > "$HIVEMIND_ROOT/memory/long-term/decisions.json"
    [[ -f "$HIVEMIND_ROOT/memory/long-term/project.json" ]] || echo '{"version":"1.0","project":{"name":null,"description":null,"tech_stack":[],"tools":[],"conventions":[],"architecture":null}}' > "$HIVEMIND_ROOT/memory/long-term/project.json"
    [[ -f "$HIVEMIND_ROOT/memory/episodic/events.json" ]] || echo '{"version":"1.0","events":[]}' > "$HIVEMIND_ROOT/memory/episodic/events.json"
    
    [[ -f "$HIVEMIND_ROOT/memory/short-term/context.json" ]] || echo '{}' > "$HIVEMIND_ROOT/memory/short-term/context.json"
    [[ -f "$HIVEMIND_ROOT/memory/short-term/working.json" ]] || echo '{}' > "$HIVEMIND_ROOT/memory/short-term/working.json"
    [[ -f "$HIVEMIND_ROOT/memory/short-term/project-context.json" ]] || echo '{}' > "$HIVEMIND_ROOT/memory/short-term/project-context.json"
    [[ -f "$HIVEMIND_ROOT/memory/short-term/decisions.json" ]] || echo '{}' > "$HIVEMIND_ROOT/memory/short-term/decisions.json"
    
    log_success "Initialized memory files"
    
    # Create symlinks in ~/.local/bin
    local user_bin="$HOME/.local/bin"
    mkdir -p "$user_bin"
    
    ln -sf "$HIVEMIND_ROOT/hivemind" "$user_bin/hivemind"
    ln -sf "$HIVEMIND_ROOT/bin/hm" "$user_bin/hm"
    
    log_success "Created symlinks in $user_bin"
    
    # Ensure ~/.local/bin is in PATH
    ensure_path_entry "$user_bin"
    
    local path_marker="# HIVEMIND local bin PATH"
    local path_export='if [[ -d "$HOME/.local/bin" ]] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then export PATH="$HOME/.local/bin:$PATH"; fi'
    
    for rcfile in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
        if [[ -f "$rcfile" ]] || [[ "$rcfile" == "$HOME/.bashrc" ]]; then
            if ! grep -Fq "$path_marker" "$rcfile" 2>/dev/null; then
                echo "" >> "$rcfile"
                echo "$path_marker" >> "$rcfile"
                echo "$path_export" >> "$rcfile"
            fi
        fi
    done
    
    log_success "Updated PATH in shell configs"
    
    # Verify engines.yaml configuration
    if [[ -f "$HIVEMIND_ROOT/config/engines.yaml" ]]; then
        log_success "Engine configuration exists: config/engines.yaml"
        log_dim "  HIVEMIND engine: codex"
        log_dim "  Agent engine: claude"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 9: CREATE LAUNCHER SCRIPT
# ═══════════════════════════════════════════════════════════════════════════════

create_launcher() {
    log_step "Creating Launcher Script"
    
    local launcher="$HIVEMIND_ROOT/start-hivemind.sh"
    
    cat > "$launcher" << 'LAUNCHER_EOF'
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
LAUNCHER_EOF
    
    chmod +x "$launcher"
    
    log_success "Created launcher: $launcher"
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 10: VERIFY INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

verify_installation() {
    log_step "Verifying Installation"
    
    local all_good=true
    
    # Check Codex
    local codex_path
    codex_path="$(find_executable codex 2>/dev/null || true)"
    if [[ -n "$codex_path" ]]; then
        log_success "Codex CLI: $codex_path"
    else
        log_error "Codex CLI: Not found"
        all_good=false
    fi
    
    # Check Claude
    local claude_path
    claude_path="$(find_executable claude 2>/dev/null || true)"
    if [[ -n "$claude_path" ]]; then
        log_success "Claude CLI: $claude_path"
    else
        log_error "Claude CLI: Not found"
        all_good=false
    fi
    
    # Check HIVEMIND command
    if [[ -x "$HOME/.local/bin/hivemind" ]]; then
        log_success "hivemind command: $HOME/.local/bin/hivemind"
    else
        log_warning "hivemind command: Not in PATH yet (restart shell)"
    fi
    
    # Check authentication
    echo ""
    log_info "Authentication Status:"
    
    if [[ -n "$codex_path" ]]; then
        if "$codex_path" login status &>/dev/null || [[ -n "${OPENAI_API_KEY:-}" ]]; then
            log_success "  Codex: Authenticated"
        else
            log_warning "  Codex: Not authenticated"
            all_good=false
        fi
    fi
    
    if [[ -n "${ANTHROPIC_API_KEY:-}" ]] || [[ -n "${CLAUDE_API_KEY:-}" ]] || [[ -f "$HOME/.claude/.credentials.json" ]]; then
        log_success "  Claude: Authenticated"
    else
        log_warning "  Claude: Not authenticated"
        all_good=false
    fi
    
    echo ""
    
    if [[ "$all_good" == "true" ]]; then
        return 0
    else
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 11: SHOW COMPLETION MESSAGE
# ═══════════════════════════════════════════════════════════════════════════════

show_completion() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}              HIVEMIND SETUP COMPLETE!${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if verify_installation; then
        echo -e "${GREEN}All components installed and configured successfully!${NC}"
    else
        echo -e "${YELLOW}Setup complete with some warnings. See above for details.${NC}"
    fi
    
    echo ""
    echo -e "${BOLD}Quick Start:${NC}"
    echo -e "  ${CYAN}source ~/.bashrc${NC}    # Reload shell (or restart terminal)"
    echo -e "  ${CYAN}hivemind${NC}            # Start interactive mode"
    echo -e "  ${CYAN}hm${NC}                  # Shorthand"
    echo ""
    echo -e "${BOLD}Or run directly:${NC}"
    echo -e "  ${CYAN}$HIVEMIND_ROOT/start-hivemind.sh${NC}"
    echo ""
    echo -e "${BOLD}Configuration:${NC}"
    echo -e "  ${CYAN}hivemind --config${NC}   # View current config"
    echo -e "  ${CYAN}hivemind --setup${NC}    # Re-run authentication"
    echo -e "  ${CYAN}hivemind --help${NC}     # Full help"
    echo ""
    echo -e "${BOLD}Architecture:${NC}"
    echo -e "  ${BLUE}Codex${NC} (OpenAI)  → HIVEMIND Orchestrator (brain)"
    echo -e "  ${PURPLE}Claude${NC} (Anthropic) → 24 Specialized Agents (workers)"
    echo ""
    echo -e "${DIM}Files:${NC}"
    echo -e "${DIM}  Config:  $HIVEMIND_ROOT/config/engines.yaml${NC}"
    echo -e "${DIM}  Env:     $HIVEMIND_ROOT/.env${NC}"
    echo -e "${DIM}  Logs:    $HIVEMIND_ROOT/logs/${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    show_banner
    
    if ! prompt_yes_no "Ready to set up HIVEMIND?"; then
        echo "Setup cancelled."
        exit 0
    fi
    
    detect_system
    
    # Install Node.js if needed
    if [[ "$NODEJS_INSTALLED" != "true" ]] || [[ "$NPM_INSTALLED" != "true" ]]; then
        if prompt_yes_no "Node.js is required. Install it now?"; then
            install_nodejs
        else
            log_error "Node.js is required. Please install it manually."
            exit 1
        fi
    fi
    
    configure_npm
    
    # Install CLIs
    if [[ "$CODEX_INSTALLED" != "true" ]]; then
        if prompt_yes_no "Install OpenAI Codex CLI?"; then
            install_codex
        fi
    fi
    
    if [[ "$CLAUDE_INSTALLED" != "true" ]]; then
        if prompt_yes_no "Install Anthropic Claude Code CLI?"; then
            install_claude
        fi
    fi
    
    # Authenticate
    authenticate_codex
    authenticate_claude
    
    # Configure HIVEMIND
    configure_hivemind
    create_launcher
    
    # Done!
    show_completion
}

# Run main
main "$@"
