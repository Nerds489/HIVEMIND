#!/bin/bash
# HIVEMIND TUI Launcher Script

set -e

TUI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TUI_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   HIVEMIND TUI - Launcher Script      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}Using Python ${PYTHON_VERSION}${NC}"

# Check if package is installed
if ! python3 -c "import hivemind_tui" 2>/dev/null; then
    echo -e "${YELLOW}Installing HIVEMIND TUI in development mode...${NC}"
    pip install -e . --quiet
fi

# Load environment variables if .env exists
if [ -f .env ]; then
    echo -e "${GREEN}Loading environment from .env${NC}"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${YELLOW}No .env file found, using defaults${NC}"
fi

# Parse arguments
WATCH_CSS=false
API_URL="${HIVEMIND_API_URL:-http://localhost:8000}"
WS_URL="${HIVEMIND_WS_URL:-ws://localhost:8000}"

while [[ $# -gt 0 ]]; do
    case $1 in
        --watch-css)
            WATCH_CSS=true
            shift
            ;;
        --api-url)
            API_URL="$2"
            shift 2
            ;;
        --ws-url)
            WS_URL="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --watch-css         Enable CSS hot-reloading (dev mode)"
            echo "  --api-url URL       Set API base URL (default: http://localhost:8000)"
            echo "  --ws-url URL        Set WebSocket URL (default: ws://localhost:8000)"
            echo "  --help, -h          Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Build command
CMD="python3 -m hivemind_tui.app --api-url $API_URL --ws-url $WS_URL"
if [ "$WATCH_CSS" = true ]; then
    CMD="$CMD --watch-css"
fi

echo -e "${GREEN}API URL:${NC} $API_URL"
echo -e "${GREEN}WebSocket URL:${NC} $WS_URL"
echo ""
echo -e "${BLUE}Starting HIVEMIND TUI...${NC}"
echo ""

# Run the TUI
exec $CMD
