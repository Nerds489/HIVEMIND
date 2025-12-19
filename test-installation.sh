#!/bin/bash
#
# HIVEMIND Installation Test
# Run this after setup.sh to verify everything works
#

set -euo pipefail

HIVEMIND_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HIVEMIND_ROOT"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    local name="$1"
    local result="$2"

    if [ "$result" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $name"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}✗${NC} $name"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "                 HIVEMIND Installation Test"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Test 1: Core files exist
echo "Testing core files..."
test -f hivemind; check "hivemind exists" $?
test -f setup.sh; check "setup.sh exists" $?
test -f config/engines.yaml; check "config/engines.yaml exists" $?

# Test 2: Scripts are executable
echo ""
echo "Testing permissions..."
test -x hivemind; check "hivemind is executable" $?
test -x setup.sh; check "setup.sh is executable" $?

# Test 3: Codex CLI installed
echo ""
echo "Testing Codex CLI..."
if command -v codex &> /dev/null; then
    check "Codex CLI installed" 0
    codex --version > /dev/null 2>&1; check "Codex CLI responds" $?
else
    check "Codex CLI installed" 1
fi

# Test 4: Claude CLI installed
echo ""
echo "Testing Claude CLI..."
if command -v claude &> /dev/null; then
    check "Claude CLI installed" 0
    claude --version > /dev/null 2>&1; check "Claude CLI responds" $?
else
    check "Claude CLI installed" 1
fi

# Test 5: HIVEMIND config works
echo ""
echo "Testing HIVEMIND..."
./hivemind --config > /dev/null 2>&1; check "hivemind --config works" $?

# Test 6: Engine configuration
echo ""
echo "Testing engine configuration..."
grep -q "hivemind: codex" config/engines.yaml; check "Codex set as HIVEMIND engine" $?
grep -q "agents: claude" config/engines.yaml; check "Claude set as agent engine" $?

# Test 7: Agent definitions
echo ""
echo "Testing agent definitions..."
test -f agents/base-prompt.md; check "base-prompt.md exists" $?
test -d agents/dev; check "agents/dev/ exists" $?
test -d agents/security; check "agents/security/ exists" $?
test -d agents/infrastructure; check "agents/infrastructure/ exists" $?
test -d agents/qa; check "agents/qa/ exists" $?

# Test 8: Memory structure
echo ""
echo "Testing memory structure..."
test -d memory/global; check "memory/global/ exists" $?
test -d memory/long-term; check "memory/long-term/ exists" $?
test -f memory/global/context.json; check "memory/global/context.json exists" $?

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo -e "Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}"
echo "═══════════════════════════════════════════════════════════════"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}All tests passed! HIVEMIND is ready to use.${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Run ./setup.sh to fix issues.${NC}"
    exit 1
fi
