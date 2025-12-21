<div align="center">

# HIVEMIND

### Multi-Agent AI Orchestration System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**24 specialized AI agents. 4 expert teams. One unified intelligence.**

[Quick Start](#quick-start) |
[Features](#features) |
[Deployment](#deployment) |
[Documentation](#documentation)

</div>

---

## What is HIVEMIND?

HIVEMIND is a production-grade multi-agent orchestration system that coordinates 24 specialized AI agents to tackle complex technical tasks. It combines **OpenAI Codex** as the orchestration brain with **Claude Code** powering the specialized agents.

When you give HIVEMIND a task, it:

1. **Analyzes** your request to identify required expertise
2. **Routes** work to the appropriate specialist agents
3. **Synthesizes** outputs into a single, coherent response
4. **Learns** from interactions to improve future responses

All internal coordination is invisible - you interact with one unified AI that speaks with a single voice.

```
                          +-------------------+
                          |    YOUR TASK      |
                          +---------+---------+
                                    |
                                    v
+-------------------------------------------------------------------+
|                    HIVEMIND ORCHESTRATOR                          |
|              Analyzes | Routes | Synthesizes                      |
+-----------------------------+-------------------------------------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
   +-------------+     +-------------+     +-------------+
   | DEVELOPMENT |     |  SECURITY   |     |     QA      |
   |  6 agents   |     |  6 agents   |     |  6 agents   |
   +-------------+     +-------------+     +-------------+
          |                   |                   |
          +-------------------+-------------------+
                              |
                    +-------------------+
                    | INFRASTRUCTURE    |
                    |    6 agents       |
                    +-------------------+
```

---

## Quick Start

### Option 1: CLI Mode (Recommended for Development)

```bash
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND
./setup.sh
```

The installer handles:
- Node.js installation (if needed)
- Codex CLI (OpenAI) installation
- Claude Code CLI (Anthropic) installation
- Interactive authentication
- Path and directory configuration

Then run:

```bash
# Interactive mode
./hivemind

# Direct task
./hivemind "Design a REST API for user authentication"

# Shorthand
hm "Review this code for security vulnerabilities"
```

### Option 2: Docker Deployment (Production)

```bash
# Start all services
make up

# View logs
make logs

# Check health
make health
```

### Option 3: TUI (Terminal User Interface)

```bash
cd tui
pip install -e .
./run-tui.sh
```

The TUI provides:
- **Quick Chat Bar** - Chat input right at the top, just type and press Enter
- **Full Chat Mode** - Press `C` for dedicated chat screen
- **Live Claude Integration** - Connects directly to Claude Code CLI
- **Agent Overview** - See all 24 agents organized by team
- **Keyboard-Driven** - `Q` quit, `C` chat, `?` help, `D` dark mode

---

## Features

### 24 Specialized Agents

| Development Team | Security Team | Infrastructure Team | QA Team |
|------------------|---------------|---------------------|---------|
| Architect | Security Architect | Cloud Architect | QA Architect |
| Backend Developer | Penetration Tester | Systems Admin | Test Automation |
| Frontend Developer | Malware Analyst | Network Engineer | Performance Tester |
| Code Reviewer | Wireless Expert | DBA | Security Tester |
| Technical Writer | Compliance Auditor | SRE | Manual QA |
| DevOps Liaison | Incident Responder | Automation Engineer | Test Data Manager |

### Slash Commands

HIVEMIND integrates with Claude Code via slash commands:

| Command | Description |
|---------|-------------|
| `/hivemind` | Activate HIVEMIND orchestration |
| `/architect` | Invoke the Architect agent |
| `/dev` | Development team coordination |
| `/sec` | Security team coordination |
| `/infra` | Infrastructure team coordination |
| `/qa` | QA team coordination |
| `/pentest` | Security penetration testing |
| `/reviewer` | Code review agent |
| `/sre` | Site Reliability Engineering |
| `/incident` | Incident response workflow |
| `/sdlc` | Full SDLC pipeline |

### Intelligent Routing

Tasks are automatically routed based on context:

| You Say | HIVEMIND Routes To |
|---------|-------------------|
| "Design a microservices architecture" | Architect |
| "Review this PR for security issues" | Code Reviewer + Security Tester |
| "Set up Kubernetes monitoring" | SRE + Infrastructure |
| "Run a penetration test" | Penetration Tester |
| "Write API documentation" | Technical Writer |

### Persistent Memory

HIVEMIND remembers across sessions:

- **Long-term**: Project context, decisions, preferences, learnings
- **Short-term**: Session state, working data
- **Episodic**: Events, incidents, milestones

### Pre-Built Workflows

| Workflow | Description |
|----------|-------------|
| `full-sdlc` | Design → Build → Test → Deploy |
| `security-assessment` | Threat model → Pentest → Report |
| `incident-response` | Detect → Contain → Recover |
| `code-review` | Static analysis → Security scan → Quality check |
| `infrastructure-deploy` | Provision → Configure → Monitor |
| `compliance-audit` | Assess → Document → Remediate |

---

## Deployment

### Development Stack

```bash
# Start all services
make up

# Build and start
make up-build

# Stop services
make down
```

### Production Stack

The production deployment includes:

| Service | Purpose |
|---------|---------|
| **Backend** | FastAPI + WebSocket + gRPC orchestration |
| **PostgreSQL** | Persistent data storage |
| **Redis** | Caching and pub/sub messaging |
| **Qdrant** | Vector database for memory |
| **RabbitMQ** | Message queue for agent coordination |
| **Prometheus** | Metrics collection (optional) |
| **Grafana** | Dashboards (optional) |
| **Jaeger** | Distributed tracing (optional) |

```bash
# Configure production environment
cp .env.production .env
# Edit .env with your credentials

# Deploy
make deploy-prod

# Verify
make status
make health
```

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make up` | Start all services |
| `make down` | Stop all services |
| `make logs` | Tail logs from all services |
| `make logs-backend` | Tail backend logs only |
| `make shell` | Open shell in backend container |
| `make migrate` | Run database migrations |
| `make health` | Check service health |
| `make status` | Show service status |
| `make clean` | Clean up containers and volumes |

---

## Project Structure

```
HIVEMIND/
├── hivemind              # Main CLI executable
├── setup.sh              # One-command installer
├── install.sh            # Core installation script
├── Makefile              # Deployment commands
├── docker-compose.yml    # Full stack orchestration
│
├── backend/              # Python orchestration backend
│   ├── src/              # Source code
│   ├── migrations/       # Database migrations
│   ├── Dockerfile        # Container build
│   └── pyproject.toml    # Python dependencies
│
├── tui/                  # Terminal User Interface
│   ├── src/              # TUI source code
│   └── run-tui.sh        # TUI launcher
│
├── agents/               # Agent definitions
│   ├── dev/              # Development team
│   ├── security/         # Security team
│   ├── infrastructure/   # Infrastructure team
│   ├── qa/               # QA team
│   └── registry/         # Agent registry (DEV-001, etc.)
│
├── .claude/commands/     # Claude Code slash commands
│   ├── hivemind.md
│   ├── architect.md
│   ├── dev.md
│   ├── sec.md
│   └── ...
│
├── workflows/            # Pre-built automation pipelines
│   ├── full-sdlc.md
│   ├── security-assessment.md
│   ├── incident-response.md
│   └── ...
│
├── memory/               # Persistent memory storage
│   ├── short-term/       # Session-scoped
│   ├── long-term/        # Persistent
│   └── episodic/         # Event-based
│
├── config/               # Configuration files
│   ├── engines.yaml      # Engine presets
│   ├── hivemind.yaml     # System settings
│   └── routing.yaml      # Task routing rules
│
├── bin/                  # Utility scripts
│   ├── memory-ops        # Memory operations
│   ├── spawn-agent       # Agent spawning
│   ├── orchestrate       # Multi-agent orchestration
│   └── ...
│
├── runtime/              # Runtime components
├── protocols/            # Quality gates
├── comms/                # Communication bus
└── docs/                 # Documentation
```

---

## Configuration

### Engine Presets

```bash
./hivemind --preset recommended   # Codex orchestrator + Claude agents (default)
./hivemind --preset full-claude   # All Claude (maximum quality)
./hivemind --preset full-codex    # All Codex (OpenAI only)
```

### Environment Variables

```bash
# API keys (optional if using browser auth)
export OPENAI_API_KEY="sk-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"

# Backend configuration
export HIVEMIND_DATABASE_URL="postgresql://..."
export HIVEMIND_REDIS_URL="redis://..."
```

### View Configuration

```bash
./hivemind --config
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `./hivemind` | Start interactive mode |
| `./hivemind "task"` | Execute a direct task |
| `./hivemind --config` | Show current configuration |
| `./hivemind --status` | Show system status |
| `./hivemind --setup` | Run authentication wizard |
| `./hivemind --preset NAME` | Apply engine preset |
| `./hivemind --help` | Show all options |
| `hm` | Shorthand for `./hivemind` |

---

## Documentation

| Document | Description |
|----------|-------------|
| [Setup Guide](HIVEMIND-SETUP-GUIDE.md) | Complete installation and configuration |
| [Quick Start](QUICKSTART.md) | Usage examples and common patterns |
| [Deployment Guide](DEPLOYMENT.md) | Production deployment instructions |
| [Agent Reference](AGENTS.md) | Agent capabilities overview |
| [Workflows](workflows/) | Pre-built automation pipelines |
| [Changelog](CHANGELOG.md) | Version history and updates |
| [Contributing](CONTRIBUTING.md) | Contribution guidelines |

---

## Technology Stack

### CLI Layer
- **Node.js** 18+ for CLI runtime
- **Codex CLI** (OpenAI) for orchestration
- **Claude Code CLI** (Anthropic) for agents

### Backend Layer
- **Python 3.11+** runtime
- **FastAPI** REST API + WebSocket
- **gRPC** for high-performance IPC
- **ZeroMQ** & **Redis Pub/Sub** messaging

### Data Layer
- **PostgreSQL** persistent storage
- **Qdrant** vector database
- **Redis** caching

### Resilience
- **Tenacity** retry logic
- **pybreaker** circuit breakers
- **Dead Letter Queue** for failed messages

### Observability
- **structlog** structured logging
- **Prometheus** metrics
- **OpenTelemetry** tracing

---

## Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Linux or macOS (Windows via WSL) |
| **Node.js** | 18.0+ |
| **Python** | 3.11+ (for backend/TUI) |
| **Docker** | 20.10+ (for containerized deployment) |
| **Accounts** | OpenAI + Anthropic (free tiers available) |

---

## FAQ

<details>
<summary><b>What's the difference between Codex and Claude?</b></summary>

**Codex** (OpenAI) runs the HIVEMIND orchestrator - it receives tasks, decides what agents are needed, and synthesizes responses.

**Claude** (Anthropic) powers the 24 individual specialist agents.

This dual-engine approach gives you the best of both AI systems.
</details>

<details>
<summary><b>Do I need API keys?</b></summary>

Not necessarily. Both CLIs support browser-based authentication. API keys are optional but provide more persistent authentication.
</details>

<details>
<summary><b>Can I use only one AI provider?</b></summary>

Yes. Use `--preset full-codex` for OpenAI only, or `--preset full-claude` for Anthropic only.
</details>

<details>
<summary><b>How do I add custom agents?</b></summary>

Create a new `.md` file in the appropriate `agents/` subdirectory. Add a registry entry in `agents/registry/`. Update routing keywords in `config/routing.yaml`.
</details>

<details>
<summary><b>Is my data sent externally?</b></summary>

Yes, prompts are sent to OpenAI (Codex) and Anthropic (Claude) for processing. The memory system stores data locally only.
</details>

---

## Contributing

Contributions are welcome:

- **Report Bugs** - Open an issue with details
- **Suggest Features** - We'd love your ideas
- **Submit PRs** - Fork, branch, code, test, PR
- **Improve Docs** - Documentation improvements appreciated

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [OpenAI](https://openai.com) for Codex
- [Anthropic](https://anthropic.com) for Claude
- The open source community

---

<div align="center">

**HIVEMIND** - Route intelligently. Execute completely. Learn continuously.

[Back to Top](#hivemind)

</div>
