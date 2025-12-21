# HIVEMIND TUI

A Textual-based Terminal User Interface for the HIVEMIND multi-agent system.

## Features

- **Quick Chat Bar** - Chat input at the top of the main screen, just type and press Enter
- **Full Chat Mode** - Dedicated chat screen with message history
- **Live Claude Integration** - Connects directly to Claude Code CLI (no backend required)
- **Three-Panel Layout** - Agents, Response, and Help panels
- **24 AI Agents** - Organized across 4 specialized teams
- **Keyboard-Driven** - Efficient navigation with comprehensive shortcuts
- **Rich Formatting** - Markdown rendering and syntax highlighting

## Installation

```bash
cd /var/home/mintys/HIVEMIND/tui
pip install -e .
```

## Usage

### Quick Start

```bash
# Using the launcher script (recommended)
./run-tui.sh

# Or directly via Python
python -m hivemind_tui

# Or via the installed command
hivemind-tui
```

### Main Screen

The main screen has three sections:

```
+------------------------------------------------------------------+
|  [Type here and press Enter to chat...]  [Send] [Full Chat]     |
+------------------------------------------------------------------+
|  AGENTS      |  RESPONSE              |  QUICK HELP             |
|              |                        |                         |
|  DEV Team    |  HIVEMIND ready...     |  Enter - Focus chat    |
|  - Architect |                        |  C - Full chat screen  |
|  - Backend   |  Your message here     |  Q - Quit              |
|  - Frontend  |                        |  D - Toggle dark mode  |
|  ...         |  Response appears...   |  ? - Help              |
|              |                        |                         |
|  SEC Team    |                        |  STATUS                 |
|  - Security  |                        |  Claude: Ready          |
|  ...         |                        |  Agents: 24             |
+------------------------------------------------------------------+
|  Q Quit | C Chat | ? Help | D Dark Mode                          |
+------------------------------------------------------------------+
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Focus chat input / Send message |
| `C` | Open full chat screen |
| `Q` | Quit application |
| `?` | Show help |
| `D` | Toggle dark/light mode |
| `M` | Return to main view |
| `Esc` | Go back |
| `Ctrl+R` | Refresh screen |

### Chat Screen Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+Enter` | Send message |
| `Ctrl+L` | Clear messages |
| `Ctrl+Up` | Previous message in history |
| `Ctrl+Down` | Next message in history |
| `Esc` | Return to main screen |

## How It Works

The TUI connects directly to Claude Code CLI:

1. You type a message in the chat input
2. TUI calls `claude --print "your message"`
3. Response streams back and displays in the message view
4. No backend server required - works out of the box

## Architecture

```
src/hivemind_tui/
├── app.py                # Main Textual application
├── styles.css            # Global CSS styles
├── screens/
│   ├── main.py          # Main screen with quick chat
│   └── chat.py          # Full chat screen
├── widgets/
│   ├── agent_list.py    # Agent list by team
│   ├── message_view.py  # Message history display
│   ├── input_box.py     # Multi-line input with history
│   └── status_bar.py    # System status display
├── engine/
│   ├── client.py        # HTTP API client
│   └── websocket.py     # WebSocket client
└── models/
    └── agents.py        # Agent data models
```

## The 24 Agents

### Development Team (6 agents)
- DEV-001: Architect
- DEV-002: Backend Developer
- DEV-003: Frontend Developer
- DEV-004: Code Reviewer
- DEV-005: Technical Writer
- DEV-006: DevOps Engineer

### Security Team (6 agents)
- SEC-001: Security Architect
- SEC-002: Penetration Tester
- SEC-003: Malware Analyst
- SEC-004: Wireless Security
- SEC-005: Compliance Auditor
- SEC-006: Incident Responder

### Infrastructure Team (6 agents)
- INF-001: Cloud Architect
- INF-002: Systems Admin
- INF-003: Network Engineer
- INF-004: Database Admin
- INF-005: SRE
- INF-006: Automation Engineer

### QA Team (6 agents)
- QA-001: QA Architect
- QA-002: Test Automation
- QA-003: Performance Tester
- QA-004: Security Tester
- QA-005: Manual QA
- QA-006: Test Data Manager

## Configuration

Environment variables (optional):

```bash
# For backend API mode (not required for CLI mode)
HIVEMIND_API_URL=http://localhost:8000
HIVEMIND_WS_URL=ws://localhost:8000
```

## Requirements

- Python 3.11+
- Claude Code CLI installed (`claude` command available)
- textual >= 0.40.0
- rich >= 13.0.0
- httpx >= 0.24.0
- websockets >= 12.0
- pydantic >= 2.0.0
- python-dotenv >= 1.0.0

## Development

### CSS Hot Reload

```bash
./run-tui.sh --watch-css
# or
hivemind-tui --watch-css
```

### Code Style

```bash
black src/
ruff check src/
mypy src/
```

## Troubleshooting

### "Claude Code CLI not found"

Make sure Claude Code is installed and in your PATH:

```bash
# Check if claude is available
which claude

# If not found, install it
npm install -g @anthropic-ai/claude-code

# Or add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### TUI won't start

```bash
# Reinstall dependencies
pip install -e . --force-reinstall

# Check Python version (needs 3.11+)
python --version
```

## License

MIT License - See LICENSE file for details
