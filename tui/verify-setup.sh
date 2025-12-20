#!/bin/bash
# HIVEMIND TUI Setup Verification Script

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  HIVEMIND TUI Setup Verification      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Track status
ERRORS=0
WARNINGS=0
CHECKS=0

check() {
    CHECKS=$((CHECKS + 1))
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        ERRORS=$((ERRORS + 1))
    fi
}

warn() {
    WARNINGS=$((WARNINGS + 1))
    echo -e "${YELLOW}⚠${NC} $1"
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check directory structure
echo "Checking directory structure..."

[ -f "pyproject.toml" ]
check "pyproject.toml exists"

[ -f "README.md" ]
check "README.md exists"

[ -f "INSTALL.md" ]
check "INSTALL.md exists"

[ -f "QUICKSTART.md" ]
check "QUICKSTART.md exists"

[ -f "run-tui.sh" ]
check "run-tui.sh exists"

[ -x "run-tui.sh" ]
check "run-tui.sh is executable"

[ -d "src/hivemind_tui" ]
check "src/hivemind_tui directory exists"

[ -f "src/hivemind_tui/__init__.py" ]
check "Package __init__.py exists"

[ -f "src/hivemind_tui/app.py" ]
check "Main app.py exists"

[ -f "src/hivemind_tui/styles.css" ]
check "styles.css exists"

echo ""
echo "Checking screens..."

[ -d "src/hivemind_tui/screens" ]
check "screens directory exists"

[ -f "src/hivemind_tui/screens/__init__.py" ]
check "screens/__init__.py exists"

[ -f "src/hivemind_tui/screens/main.py" ]
check "main.py screen exists"

[ -f "src/hivemind_tui/screens/chat.py" ]
check "chat.py screen exists"

echo ""
echo "Checking widgets..."

[ -d "src/hivemind_tui/widgets" ]
check "widgets directory exists"

[ -f "src/hivemind_tui/widgets/__init__.py" ]
check "widgets/__init__.py exists"

[ -f "src/hivemind_tui/widgets/agent_list.py" ]
check "agent_list.py widget exists"

[ -f "src/hivemind_tui/widgets/message_view.py" ]
check "message_view.py widget exists"

[ -f "src/hivemind_tui/widgets/input_box.py" ]
check "input_box.py widget exists"

[ -f "src/hivemind_tui/widgets/status_bar.py" ]
check "status_bar.py widget exists"

echo ""
echo "Checking Python syntax..."

# Check Python syntax for all files
for file in src/hivemind_tui/*.py src/hivemind_tui/**/*.py; do
    if [ -f "$file" ]; then
        python3 -m py_compile "$file" 2>/dev/null
        if [ $? -eq 0 ]; then
            check "$(basename $file) syntax OK"
        else
            warn "$(basename $file) has syntax errors"
        fi
    fi
done

echo ""
echo "Checking dependencies..."

# Check if Python 3.11+ is available
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
    check "Python version ($PYTHON_VERSION) >= 3.11"
else
    warn "Python version ($PYTHON_VERSION) < 3.11 (may have issues)"
fi

# Check if pip is available
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    check "pip is available"
else
    warn "pip not found"
fi

echo ""
echo "File statistics..."

# Count lines of code
PYTHON_FILES=$(find src -name "*.py" | wc -l)
TOTAL_LINES=$(find src -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}')

info "Python files: $PYTHON_FILES"
info "Total lines of code: $TOTAL_LINES"

# Count documentation
DOC_FILES=$(find . -maxdepth 1 -name "*.md" | wc -l)
info "Documentation files: $DOC_FILES"

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo "Summary:"
echo -e "  ${GREEN}Checks passed: $CHECKS${NC}"
if [ $ERRORS -gt 0 ]; then
    echo -e "  ${RED}Errors: $ERRORS${NC}"
fi
if [ $WARNINGS -gt 0 ]; then
    echo -e "  ${YELLOW}Warnings: $WARNINGS${NC}"
fi
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Setup verification complete! Ready to install.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Run: pip install -e ."
    echo "  2. Run: ./run-tui.sh"
    echo "  or"
    echo "  2. Run: hivemind-tui"
    exit 0
else
    echo -e "${RED}✗ Setup verification found errors. Please fix before installing.${NC}"
    exit 1
fi
