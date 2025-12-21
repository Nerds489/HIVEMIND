# HIVEMIND Quick Start Guide

Get up and running in minutes.

---

## Installation Options

### Option 1: CLI Only (Fastest)

```bash
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND
./setup.sh
```

This installs:
- Codex CLI (OpenAI)
- Claude Code CLI (Anthropic)
- `hm` command shortcut

### Option 2: Full Stack (Docker)

```bash
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND
make up
```

This starts:
- HIVEMIND Backend API (port 8000)
- PostgreSQL database
- Redis cache
- Qdrant vector DB
- RabbitMQ message queue

### Option 3: TUI (Terminal UI)

```bash
cd tui
pip install -e .
./run-tui.sh
```

The TUI features:
- **Quick Chat Bar** - Type and press Enter at the top of the screen
- **Full Chat Mode** - Press `C` for dedicated chat with history
- **Live Claude Integration** - Connects directly to Claude Code CLI
- **No Backend Required** - Works immediately after install

**Keyboard shortcuts:** `Enter` chat, `C` full chat, `Q` quit, `?` help, `D` dark mode

---

## Basic Usage

### CLI Mode

```bash
# Interactive mode
./hivemind

# Direct task
./hivemind "Design a REST API for user authentication"

# Shorthand
hm "Review this code for security vulnerabilities"
```

### Slash Commands (Claude Code)

In Claude Code, use these commands:

| Command | Description |
|---------|-------------|
| `/hivemind` | Activate HIVEMIND orchestration |
| `/architect` | System architecture and design |
| `/dev` | Development team tasks |
| `/sec` | Security team tasks |
| `/infra` | Infrastructure team tasks |
| `/qa` | QA and testing tasks |
| `/pentest` | Penetration testing |
| `/reviewer` | Code review |
| `/sre` | Site reliability engineering |
| `/incident` | Incident response |
| `/sdlc` | Full development lifecycle |

### Docker Commands

```bash
make up              # Start all services
make down            # Stop all services
make logs            # View logs
make logs-backend    # View backend logs only
make health          # Check service health
make shell           # Shell into backend container
make migrate         # Run database migrations
make test            # Run tests
```

---

## Task Examples

### Single Agent Tasks

```
"Design a REST API for user management"
→ Routes to Architect

"Review this pull request for security issues"
→ Routes to Code Reviewer + Security Tester

"Run a penetration test on the login endpoint"
→ Routes to Penetration Tester

"Set up monitoring for the new microservice"
→ Routes to SRE

"Create automated tests for the checkout flow"
→ Routes to Test Automation Engineer
```

### Team Tasks

```
"I need the development team to build a new feature"
→ Activates Development Team (6 agents)

"Security team, assess our cloud infrastructure"
→ Activates Security Team (6 agents)

"Infrastructure team, prepare for production deployment"
→ Activates Infrastructure Team (6 agents)

"QA team, run full regression testing"
→ Activates QA Team (6 agents)
```

### Workflow Tasks

```
"Full SDLC for implementing OAuth authentication"
→ Runs: Design → Build → Review → Test → Deploy

"Security assessment of the payment API"
→ Runs: Threat Model → Pentest → Report

"We have a production incident - database is down"
→ Runs: Detect → Contain → Recover → Report

"Code review pipeline for PR #1234"
→ Runs: Static Analysis → Security Scan → Quality Check

"Deploy version 2.0 to production"
→ Runs: Validate → Provision → Deploy → Monitor
```

---

## Agent Reference

### Development Team (DEV)

| ID | Role | Keywords |
|----|------|----------|
| DEV-001 | Architect | design, architecture, system, blueprint, patterns |
| DEV-002 | Backend Developer | api, backend, server, python, node, go |
| DEV-003 | Frontend Developer | ui, frontend, react, vue, css, component |
| DEV-004 | Code Reviewer | review, pr, quality, standards, best practices |
| DEV-005 | Technical Writer | docs, documentation, readme, guide, tutorial |
| DEV-006 | DevOps Liaison | ci/cd, pipeline, deploy, build, github actions |

### Security Team (SEC)

| ID | Role | Keywords |
|----|------|----------|
| SEC-001 | Security Architect | threat model, security design, zero trust |
| SEC-002 | Penetration Tester | pentest, hack, exploit, vulnerability, owasp |
| SEC-003 | Malware Analyst | malware, reverse engineer, binary, ioc |
| SEC-004 | Wireless Security | wifi, bluetooth, wireless, rf, iot |
| SEC-005 | Compliance Auditor | compliance, audit, gdpr, soc2, pci, hipaa |
| SEC-006 | Incident Responder | incident, breach, forensics, emergency |

### Infrastructure Team (INF)

| ID | Role | Keywords |
|----|------|----------|
| INF-001 | Infrastructure Architect | cloud, aws, azure, gcp, kubernetes |
| INF-002 | Systems Administrator | linux, server, sysadmin, hardening |
| INF-003 | Network Engineer | network, firewall, dns, routing, vpn |
| INF-004 | Database Administrator | database, sql, postgres, mongodb, optimization |
| INF-005 | Site Reliability Engineer | sre, monitoring, slo, reliability, uptime |
| INF-006 | Automation Engineer | terraform, ansible, automation, iac |

### QA Team (QA)

| ID | Role | Keywords |
|----|------|----------|
| QA-001 | QA Architect | test strategy, quality, coverage, process |
| QA-002 | Test Automation | selenium, playwright, pytest, jest, cypress |
| QA-003 | Performance Tester | load test, performance, benchmark, k6 |
| QA-004 | Security Tester | sast, dast, security scan, devsecops |
| QA-005 | Manual QA | exploratory, manual test, uat, usability |
| QA-006 | Test Data Manager | test data, fixtures, environment, mock |

---

## Configuration

### Engine Presets

```bash
./hivemind --preset recommended   # Codex orchestrator + Claude agents (default)
./hivemind --preset full-claude   # All Claude
./hivemind --preset full-codex    # All Codex
```

### Environment Variables

```bash
# API Keys (optional if using browser auth)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Backend (for Docker deployment)
export POSTGRES_PASSWORD="your-password"
export RABBITMQ_PASSWORD="your-password"
```

### View Current Config

```bash
./hivemind --config
./hivemind --status
```

---

## API Endpoints (Docker Mode)

When running with Docker (`make up`):

| Endpoint | Description |
|----------|-------------|
| `http://localhost:8000/` | API info |
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/health` | Health check |
| `http://localhost:8000/ready` | Readiness check |
| `ws://localhost:8000/ws` | WebSocket |
| `http://localhost:15672` | RabbitMQ UI |
| `http://localhost:6333` | Qdrant UI |

### With Monitoring Stack

```bash
make monitoring-up
```

| Endpoint | Description |
|----------|-------------|
| `http://localhost:3000` | Grafana (admin/admin) |
| `http://localhost:9090` | Prometheus |
| `http://localhost:16686` | Jaeger tracing |

---

## Memory System

HIVEMIND remembers across sessions:

### Auto-Store Triggers

| You Say | What Gets Stored |
|---------|------------------|
| "Remember that..." | Learning/fact |
| "We decided..." | Decision |
| "I prefer..." | Preference |
| "Always..." / "Never..." | Rule |
| "Our stack is..." | Tech stack |
| "We use..." | Tool |

### Memory Locations

```
memory/
├── short-term/     # Current session
├── long-term/      # Persistent storage
│   ├── learnings.json
│   ├── preferences.json
│   ├── decisions.json
│   └── project.json
├── episodic/       # Events & incidents
└── agents/         # Per-agent memory
```

### Memory Commands

```bash
# CLI memory operations
bin/memory-ops store "key" "value"
bin/memory-ops recall "query"
bin/memory-ops list
```

---

## Workflows

### Full SDLC Pipeline

```
Design → Implement → Review → Test → Deploy → Validate
```

Invoke: `"Run full SDLC for [feature]"` or `/sdlc`

### Security Assessment

```
Scope → Threat Model → Pentest → Report → Remediation
```

Invoke: `"Security assessment of [target]"` or `/sec`

### Incident Response

```
Detect → Contain → Eradicate → Recover → Report
```

Invoke: `"Incident response for [issue]"` or `/incident`

### Code Review Pipeline

```
Static Analysis → Security Scan → Quality Check → Findings Report
```

Invoke: `"Code review for [PR/file]"` or `/reviewer`

---

## Project Structure

```
HIVEMIND/
├── hivemind              # Main CLI
├── setup.sh              # Installer
├── Makefile              # Docker commands
├── docker-compose.yml    # Full stack
│
├── backend/              # Python API
│   ├── src/hivemind/     # Source code
│   ├── migrations/       # Database
│   └── Dockerfile
│
├── tui/                  # Terminal UI
│   └── src/hivemind_tui/
│
├── agents/               # 24 agent definitions
│   ├── dev/
│   ├── security/
│   ├── infrastructure/
│   ├── qa/
│   └── registry/         # Agent IDs
│
├── .claude/commands/     # Slash commands
│
├── workflows/            # Pipelines
│   ├── full-sdlc.md
│   ├── security-assessment.md
│   ├── incident-response.md
│   ├── code-review.md
│   ├── infrastructure-deploy.md
│   └── compliance-audit.md
│
├── memory/               # Persistent storage
├── config/               # Configuration
├── bin/                  # Utilities
└── templates/            # Output templates
```

---

## Troubleshooting

### CLI Issues

```bash
# Check installation
./hivemind --status

# Re-run setup
./setup.sh

# Check engine availability
which codex
which claude
```

### Docker Issues

```bash
# Check service status
make status
make health

# View logs
make logs

# Restart services
make restart

# Full reset
make down-volumes
make up-build
```

### TUI Issues

```bash
# Reinstall TUI dependencies
cd tui && pip install -e . --force-reinstall

# Check Python version (needs 3.11+)
python --version

# Run TUI manually
python -m hivemind_tui
```

### Common Fixes

| Problem | Solution |
|---------|----------|
| "codex not found" | Run `./setup.sh` or install manually |
| "claude not found" | Run `npm install -g @anthropic-ai/claude-code` |
| TUI "Claude CLI not found" | Ensure `claude` is in PATH |
| TUI won't start | Reinstall: `pip install -e . --force-reinstall` |
| Docker services unhealthy | `make down && make up-build` |
| Database connection failed | Check `POSTGRES_PASSWORD` in `.env` |
| API key errors | Set `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` |

---

## Tips

1. **Be specific** - "Review auth code for SQL injection" > "Review code"
2. **Use slash commands** - Faster than typing full prompts
3. **Check `/hivemind`** - Verify HIVEMIND is active
4. **Use Docker for production** - Full observability stack
5. **Memory persists** - HIVEMIND learns your preferences

---

## Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore [workflows/](workflows/) for automation pipelines
- Check [agents/](agents/) for detailed agent capabilities

---

*HIVEMIND - Route intelligently. Execute completely. Learn continuously.*
