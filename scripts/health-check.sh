#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# HIVEMIND Health Check & Diagnostic Script
# ═══════════════════════════════════════════════════════════════════════════════
# Verifies all components are properly configured and functional
# Run: ./health-check.sh [--fix] [--verbose]
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# Colors
RED=$'\033[0;31m'
GRN=$'\033[0;32m'
YLW=$'\033[0;33m'
CYN=$'\033[0;36m'
WHT=$'\033[1;37m'
DIM=$'\033[2m'
RST=$'\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

# Options
FIX_MODE=false
VERBOSE=false

for arg in "$@"; do
    case "$arg" in
        --fix) FIX_MODE=true ;;
        --verbose|-v) VERBOSE=true ;;
    esac
done

# Helpers
pass() { echo -e "  ${GRN}✓${RST} $1"; ((PASS++)); }
fail() { echo -e "  ${RED}✗${RST} $1"; ((FAIL++)); }
warn() { echo -e "  ${YLW}⚠${RST} $1"; ((WARN++)); }
info() { [[ "$VERBOSE" == "true" ]] && echo -e "  ${DIM}$1${RST}"; }
header() { echo -e "\n${CYN}━━━ $1 ━━━${RST}"; }

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HIVEMIND_ROOT="${SCRIPT_DIR%/*}"

echo -e "${WHT}"
cat << 'BANNER'
██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗
██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝
BANNER
echo -e "${RST}"
echo -e "${DIM}Health Check & Diagnostic Tool${RST}"
echo -e "${DIM}Root: $HIVEMIND_ROOT${RST}"

# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURE CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "DIRECTORY STRUCTURE"

required_dirs=(
    "agents/development"
    "agents/security"
    "agents/infrastructure"
    "agents/qa"
    "agents/registry"
    "config"
    "memory/global"
    "memory/agents"
    "memory/teams"
    "memory/schemas"
    "teams"
    "workflows"
    "orchestration"
    "protocols"
    ".claude/commands"
)

for dir in "${required_dirs[@]}"; do
    if [[ -d "$HIVEMIND_ROOT/$dir" ]]; then
        pass "$dir"
    else
        fail "$dir (missing)"
        if [[ "$FIX_MODE" == "true" ]]; then
            mkdir -p "$HIVEMIND_ROOT/$dir"
            info "Created $dir"
        fi
    fi
done

# ═══════════════════════════════════════════════════════════════════════════════
# AGENT CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "AGENTS (24 Required)"

agent_count=0
for team in development security infrastructure qa; do
    team_count=$(ls "$HIVEMIND_ROOT/agents/$team"/*.md 2>/dev/null | wc -l || echo 0)
    ((agent_count += team_count))
    info "$team: $team_count agents"
done

registry_count=$(ls "$HIVEMIND_ROOT/agents/registry"/*.md 2>/dev/null | wc -l || echo 0)

if [[ $registry_count -eq 24 ]]; then
    pass "Registry: 24/24 agents"
else
    fail "Registry: $registry_count/24 agents"
fi

# Check memory profiles
header "AGENT MEMORY PROFILES"

memory_profiles=0
for id in DEV-{001..006} SEC-{001..006} INF-{001..006} QA-{001..006}; do
    if [[ -f "$HIVEMIND_ROOT/memory/agents/$id/_memory.json" ]]; then
        ((memory_profiles++))
        info "$id: has memory profile"
    else
        warn "$id: missing _memory.json"
    fi
done

if [[ $memory_profiles -eq 24 ]]; then
    pass "Memory profiles: 24/24"
else
    warn "Memory profiles: $memory_profiles/24"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "CONFIGURATION"

config_files=(
    "config/agents.json"
    "config/routing.json"
    "config/settings.json"
)

for file in "${config_files[@]}"; do
    if [[ -f "$HIVEMIND_ROOT/$file" ]]; then
        if command -v jq &>/dev/null; then
            if jq empty "$HIVEMIND_ROOT/$file" 2>/dev/null; then
                pass "$file (valid JSON)"
            else
                fail "$file (invalid JSON)"
            fi
        else
            pass "$file (exists, jq not available for validation)"
        fi
    else
        fail "$file (missing)"
    fi
done

# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "AI ENGINES"

if command -v claude &>/dev/null; then
    pass "Claude Code CLI: installed"
    if [[ "$VERBOSE" == "true" ]]; then
        claude --version 2>/dev/null | head -1 | sed 's/^/    /'
    fi
else
    warn "Claude Code CLI: not found"
fi

if command -v codex &>/dev/null; then
    pass "Codex CLI: installed"
else
    warn "Codex CLI: not found"
fi

if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
    pass "ANTHROPIC_API_KEY: set"
else
    warn "ANTHROPIC_API_KEY: not set"
fi

if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    pass "OPENAI_API_KEY: set"
else
    info "OPENAI_API_KEY: not set (optional)"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CLI CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "HIVEMIND CLI"

if [[ -f "$HIVEMIND_ROOT/hivemind" ]]; then
    pass "hivemind executable exists"
    if [[ -x "$HIVEMIND_ROOT/hivemind" ]]; then
        pass "hivemind is executable"
    else
        fail "hivemind not executable"
        if [[ "$FIX_MODE" == "true" ]]; then
            chmod +x "$HIVEMIND_ROOT/hivemind"
            info "Fixed permissions"
        fi
    fi
else
    fail "hivemind executable missing"
fi

if [[ -f "$HIVEMIND_ROOT/CLAUDE.md" ]]; then
    pass "CLAUDE.md present"
else
    fail "CLAUDE.md missing (auto-load prompt)"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY SYSTEM CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "MEMORY SYSTEM"

schema_count=$(ls "$HIVEMIND_ROOT/memory/schemas"/*.json 2>/dev/null | wc -l || echo 0)
if [[ $schema_count -ge 10 ]]; then
    pass "Memory schemas: $schema_count files"
else
    warn "Memory schemas: only $schema_count files"
fi

if [[ -f "$HIVEMIND_ROOT/memory/MEMORY.md" ]]; then
    pass "Memory documentation present"
else
    warn "Memory documentation missing"
fi

# Check team knowledge
team_knowledge=0
for team in development security infrastructure qa; do
    if [[ -d "$HIVEMIND_ROOT/memory/teams/$team" ]]; then
        count=$(ls "$HIVEMIND_ROOT/memory/teams/$team"/*.json 2>/dev/null | wc -l || echo 0)
        ((team_knowledge += count))
    fi
done
pass "Team knowledge files: $team_knowledge"

# ═══════════════════════════════════════════════════════════════════════════════
# TUI CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "TUI (Optional)"

if [[ -d "$HIVEMIND_ROOT/tui" ]]; then
    pass "TUI directory exists"
    
    if [[ -f "$HIVEMIND_ROOT/tui/src/hivemind_tui/app.py" ]]; then
        pass "TUI app.py present"
    else
        warn "TUI app.py missing"
    fi
    
    if command -v python3 &>/dev/null; then
        if python3 -c "import textual" 2>/dev/null; then
            pass "Textual library available"
        else
            warn "Textual library not installed"
        fi
    fi
else
    info "TUI not installed (optional component)"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# BACKEND CHECK
# ═══════════════════════════════════════════════════════════════════════════════

header "BACKEND (Optional)"

if [[ -d "$HIVEMIND_ROOT/backend" ]]; then
    pass "Backend directory exists"
    
    if [[ -f "$HIVEMIND_ROOT/docker-compose.yml" ]]; then
        pass "docker-compose.yml present"
    fi
    
    if command -v docker &>/dev/null; then
        pass "Docker available"
        if docker compose version &>/dev/null || docker-compose version &>/dev/null; then
            pass "Docker Compose available"
        else
            warn "Docker Compose not available"
        fi
    else
        warn "Docker not installed"
    fi
else
    info "Backend not installed (optional component)"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYN}═══════════════════════════════════════════════════════════════════════════════${RST}"
echo -e "${WHT}SUMMARY${RST}"
echo -e "${CYN}═══════════════════════════════════════════════════════════════════════════════${RST}"
echo ""
echo -e "  ${GRN}Passed:${RST}   $PASS"
echo -e "  ${YLW}Warnings:${RST} $WARN"
echo -e "  ${RED}Failed:${RST}   $FAIL"
echo ""

if [[ $FAIL -eq 0 ]]; then
    echo -e "  ${GRN}★ HIVEMIND is healthy and ready!${RST}"
    exit 0
elif [[ $FAIL -lt 5 ]]; then
    echo -e "  ${YLW}⚠ Minor issues detected. Run with --fix to auto-repair.${RST}"
    exit 1
else
    echo -e "  ${RED}✗ Significant issues found. Review and fix manually.${RST}"
    exit 2
fi
