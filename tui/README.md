# HIVEMIND TUI

```text
 _   _ ___ ____  ________  __ ___ _   _ ____
| | | |_ _|  _ \| ____\ \/ /|_ _| \ | |  _ \
| |_| || || | | |  _|  \  /  | ||  \| | | | |
|  _  || || |_| | |___ /  \  | || |\  | |_| |
|_| |_|___|____/|_____/_/\_\|___|_| \_|____/
```

A Textual-based terminal UI for the HIVEMIND multi-agent system.

## Highlights

- Quick chat bar on the main screen
- Full chat mode with history
- Codex + Claude consensus planning
- 24 specialist agents across 4 teams
- Status log popup (Ctrl+O)
- Live input injection during planning/review (/note)
- Cyberpunk/matrix theme

---

## Install

```bash
cd /var/home/mintys/HIVEMIND/tui
pip install -e .
```

---

## Run

```bash
# Launcher (recommended)
./run-tui.sh

# Python module
python -m hivemind_tui

# Installed command
hivemind-tui
```

---

## Commands

```
/hivemind [task]   Full multi-agent orchestration
/dev [task]        Development team
/sec [task]        Security team
/infra [task]      Infrastructure team
/qa [task]         QA team
/architect [task]  DEV-001 Architect
/pentest [task]    SEC-002 Pentester
/sre [task]        INF-005 SRE
/reviewer [task]   DEV-004 Code Reviewer
/status            System status
/recall [query]    Session memory recall
/debug [task]      Routing details
/note [message]    Live input during planning/review
```

Aliases for /note: /live, /feedback

---

## Live Input While Running

If you need to steer the plan or review while a task is running:

```
/note focus on auth flow correctness
```

Notes sent while idle are queued for the next task.

---

## Keyboard Shortcuts

### Main Screen

| Key | Action |
|-----|--------|
| Enter | Send message (quick input) |
| C | Open full chat screen |
| M | Return to main view |
| Q | Quit |
| D | Toggle dark mode |
| ? | Help |
| Ctrl+O | Status log popup |
| Ctrl+C | Cancel current task |
| Esc | Focus input |

### Full Chat Screen

| Key | Action |
|-----|--------|
| Ctrl+Enter | Send message |
| Ctrl+L | Clear chat history |
| Ctrl+C | Cancel current task |
| Esc | Back to main |

---

## Requirements

- Python 3.11+
- Codex CLI installed (`codex` in PATH)
- Claude CLI installed (`claude` in PATH)
- textual >= 0.40.0
- rich >= 13.0.0
- python-dotenv >= 1.0.0

---

## Theme

Set the theme from the environment:

```bash
export HIVEMIND_THEME="cyberpunk-matrix"
```

---

## Troubleshooting

### Codex trusted directory error

HIVEMIND skips the Codex trusted-directory check globally. If you still see it, update the `codex` CLI.

### CLI not found

```bash
which codex
which claude
```

---

## Architecture

```
src/hivemind_tui/
├── app.py                # Main Textual application
├── styles.css            # Global CSS styles
├── screens/
│   ├── auth_screen.py    # Auth screen
│   ├── main.py           # Main screen
│   ├── chat.py           # Full chat
│   └── status_log.py     # Status log popup
├── widgets/
│   ├── agent_list.py     # Agent list by team
│   ├── message_view.py   # Message history
│   ├── input_box.py      # Multi-line input with history
│   ├── status_bar.py     # System status
│   └── status_log.py     # Status log widget
└── engine/
    ├── auth.py           # CLI authentication checks
    ├── codex_head.py     # Codex orchestration
    ├── claude_agent.py   # Claude agent execution
    ├── dialogue.py       # Codex + Claude consensus
    └── memory.py         # Session memory
```

---

## License

MIT License - See LICENSE.
