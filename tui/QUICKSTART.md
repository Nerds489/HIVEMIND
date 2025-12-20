# HIVEMIND TUI Quick Start

Get up and running with HIVEMIND TUI in 60 seconds!

## Installation

```bash
cd /var/home/mintys/HIVEMIND/tui
pip install -e .
```

## Launch

```bash
./run-tui.sh
```

Or:

```bash
hivemind-tui
```

## Essential Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `?` | Show help |
| `c` | Switch to Chat view |
| `m` | Switch to Main view |
| `d` | Toggle dark/light mode |
| `Ctrl+R` | Refresh screen |
| `Esc` | Go back |

### In Chat View

| Key | Action |
|-----|--------|
| `Ctrl+Enter` | Send message |
| `Ctrl+L` | Clear messages |
| `Ctrl+Up` | Previous message from history |
| `Ctrl+Down` | Next message from history |

## Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit to set your endpoints:

```bash
HIVEMIND_API_URL=http://localhost:8000
HIVEMIND_WS_URL=ws://localhost:8000
```

## Layout Overview

### Main View (Default)

```
┌─────────────────────────────────────────────────────┐
│  HIVEMIND - Multi-Agent Command Center             │
├──────────┬────────────────────────┬─────────────────┤
│ AGENTS   │ MESSAGE HISTORY        │ SYSTEM STATUS   │
│          │                        │                 │
│ Strategy │ User: Hello            │ Connection: ✓   │
│ ● Agent1 │ Assistant: Hi there    │ Active: None    │
│ ● Agent2 │                        │ Tasks: 0/0      │
│          │                        │                 │
│ Engineer │                        │ Time: 14:25     │
│ ● Agent3 │                        │ API: localhost  │
│ ...      │                        │                 │
└──────────┴────────────────────────┴─────────────────┘
```

### Chat View

```
┌─────────────────────────────────────────────────────┐
│  HIVEMIND - Multi-Agent Command Center             │
├─────────────────────────────────────────────────────┤
│ CONVERSATION                                        │
│                                                     │
│ You • 14:25:30                                     │
│ Hello, HIVEMIND!                                   │
│                                                     │
│ HIVEMIND • 14:25:31                               │
│ Hello! How can I help you today?                   │
│                                                     │
├─────────────────────────────────────────────────────┤
│ YOUR MESSAGE (Ctrl+Enter to send)                  │
│ ┌─────────────────────────────────────────────┐   │
│ │ Type your message here...                   │   │
│ └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## The 24 Agents

Organized into 6 teams with 4 agents each:

- **Strategy** - Planning and coordination
- **Engineering** - Development and operations
- **Research** - Analysis and ML
- **Documentation** - Writing and tutorials
- **Security** - Testing and compliance
- **Communication** - UX and support

## Agent Status Indicators

- `●` Green - Idle (ready)
- `◐` Yellow - Busy (working)
- `✗` Red - Error (issue)

## Troubleshooting

### Can't import hivemind_tui
```bash
pip install -e . --force-reinstall
```

### Display issues
- Ensure terminal supports 256 colors
- Minimum terminal size: 80x24

### Connection failed
- Check backend is running
- Verify API URL in .env
- Check firewall settings

## Development Mode

Watch CSS for changes:

```bash
./run-tui.sh --watch-css
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [INSTALL.md](INSTALL.md) for installation help
- Explore the code in `src/hivemind_tui/`

## Support

- Documentation: Check the docs/ directory
- Issues: Review error messages in the TUI
- Logs: Check console output for debugging

---

**Ready to start!** Press `c` for chat mode and start interacting with HIVEMIND.
