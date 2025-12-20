# HIVEMIND TUI

A Textual-based Terminal User Interface for the HIVEMIND multi-agent system.

## Features

- **Three-Panel Layout**: Agents, Chat, and Status panels for complete system overview
- **24 AI Agents**: Organized across 6 specialized teams (Strategy, Engineering, Research, Documentation, Security, Communication)
- **Interactive Chat**: Real-time messaging with markdown support and streaming responses
- **Agent Management**: Monitor agent status, current tasks, and team organization
- **Keyboard-Driven**: Efficient navigation with comprehensive keyboard shortcuts
- **Rich Formatting**: Syntax highlighting, markdown rendering, and beautiful UI components

## Installation

Install in development mode:

```bash
cd /var/home/mintys/HIVEMIND/tui
pip install -e .
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

### Starting the TUI

Run the application:

```bash
hivemind-tui
```

With custom API endpoint:

```bash
hivemind-tui --api-url http://localhost:8000 --ws-url ws://localhost:8000
```

### Keyboard Shortcuts

- `q` - Quit application
- `?` - Show help
- `d` - Toggle dark/light mode
- `c` - Switch to Chat view
- `m` - Switch to Main view
- `Ctrl+R` - Refresh screen
- `Ctrl+Enter` - Send message (in chat)
- `Ctrl+L` - Clear messages (in chat)
- `Esc` - Go back/close screen

## Architecture

```
src/hivemind_tui/
├── __init__.py           # Package initialization
├── app.py                # Main Textual application
├── styles.css            # Global CSS styles
├── screens/              # Screen definitions
│   ├── __init__.py
│   ├── main.py          # Main three-panel view
│   └── chat.py          # Interactive chat screen
└── widgets/              # Reusable widgets
    ├── __init__.py
    ├── agent_list.py    # Agent list with team grouping
    ├── message_view.py  # Message history display
    ├── input_box.py     # Multi-line input with history
    └── status_bar.py    # System status display
```

## The 24 Agents

### Strategy Team (4 agents)
- Strategist Alpha - Lead Strategy
- Planner Beta - Planning
- Analyst Gamma - Analysis
- Coordinator Delta - Coordination

### Engineering Team (4 agents)
- Architect Prime - System Architecture
- Developer Apex - Implementation
- DevOps Sigma - Operations
- QA Validator - Quality Assurance

### Research Team (4 agents)
- Researcher Omega - Lead Research
- Data Scientist - Data Analysis
- ML Specialist - Machine Learning
- Knowledge Curator - Knowledge Management

### Documentation Team (4 agents)
- Doc Master - Lead Documentation
- Technical Writer - Technical Writing
- API Documenter - API Documentation
- Tutorial Creator - Tutorial Creation

### Security Team (4 agents)
- Security Chief - Lead Security
- Penetration Tester - Security Testing
- Code Auditor - Code Security
- Compliance Officer - Compliance

### Communication Team (4 agents)
- Comm Director - Lead Communication
- UX Specialist - User Experience
- Support Agent - User Support
- Community Manager - Community

## Configuration

Set environment variables in `.env`:

```bash
HIVEMIND_API_URL=http://localhost:8000
HIVEMIND_WS_URL=ws://localhost:8000
```

## Development

### Running in Development Mode

Enable CSS hot-reloading:

```bash
hivemind-tui --watch-css
```

### Code Style

Format code with Black:

```bash
black src/
```

Lint with Ruff:

```bash
ruff check src/
```

Type check with MyPy:

```bash
mypy src/
```

## Requirements

- Python 3.11+
- textual >= 0.40.0
- rich >= 13.0.0
- httpx >= 0.24.0
- websockets >= 12.0

## License

MIT License - See LICENSE file for details
