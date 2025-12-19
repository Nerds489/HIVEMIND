<div align="center">

# HIVEMIND

### Neural Multi-Agent Orchestration System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**HIVEMIND coordinates 24 specialized AI agents to tackle complex technical tasks.
One command. Multiple experts. Unified results.**

[Quick Start](#-quick-start) |
[Features](#-features) |
[Documentation](#-documentation) |
[Contributing](#-contributing)

</div>

---

## What is HIVEMIND?

HIVEMIND is a multi-agent orchestration system that combines **OpenAI Codex** as the central brain with **Claude Code** powering 24 specialized agents. When you give HIVEMIND a task, it automatically:

1. **Analyzes** your request to understand what expertise is needed
2. **Delegates** work to the appropriate specialist agents
3. **Synthesizes** their outputs into a single, coherent response
4. **Learns** from the interaction to improve future responses

All of this happens invisibly - you interact with one unified AI that has the combined knowledge of an entire technical team.

```
                              +-------------------+
                              |    YOUR TASK      |
                              +---------+---------+
                                        |
                                        v
+-----------------------------------------------------------------------+
|                      CODEX (HIVEMIND Brain)                           |
|                Orchestrates | Routes | Synthesizes                    |
+----------------------------------+------------------------------------+
                                   |
           +-----------------------+-----------------------+
           |                       |                       |
           v                       v                       v
    +-------------+         +-------------+         +-------------+
    | DEVELOPMENT |         |  SECURITY   |         |     QA      |
    |  6 agents   |         |  6 agents   |         |  6 agents   |
    +-------------+         +-------------+         +-------------+
           |                       |                       |
           +-----------------------+-----------------------+
                                   |
                         +-------------------+
                         | INFRASTRUCTURE    |
                         |    6 agents       |
                         +-------------------+
```

---

## Quick Start

### One-Command Install

```bash
git clone https://github.com/USERNAME/HIVEMIND.git
cd HIVEMIND
./setup.sh
```

The installer handles everything:

- Installs Node.js (if needed)
- Installs Codex CLI (OpenAI)
- Installs Claude Code CLI (Anthropic)
- Walks you through authentication
- Configures all paths and directories

### Start Using HIVEMIND

```bash
# Interactive mode
./hivemind

# Or direct task
./hivemind "Design a REST API for user authentication"

# Shorthand
hm "Review this code for security vulnerabilities"
```

---

## Features

### 24 Specialized Agents

| Development Team | Security Team | Infrastructure Team | QA Team |
|------------------|---------------|---------------------|---------|
| Architect | Security Architect | Cloud Architect | QA Architect |
| Backend Developer | Penetration Tester | Sysadmin | Test Automation |
| Frontend Developer | Malware Analyst | Network Engineer | Performance Tester |
| Code Reviewer | Wireless Expert | DBA | Security Tester |
| Technical Writer | Compliance Auditor | SRE | Manual QA |
| DevOps Liaison | Incident Responder | Automation Engineer | Test Data Manager |

### Intelligent Routing

HIVEMIND automatically routes tasks to the right agents based on context:

| You Say | HIVEMIND Routes To |
|---------|-------------------|
| "Design a microservices architecture" | Architect |
| "Review this PR for security issues" | Code Reviewer + Security Tester |
| "Set up Kubernetes monitoring" | SRE + Infrastructure Architect |
| "Run a penetration test" | Penetration Tester |
| "Write API documentation" | Technical Writer |

### Persistent Memory

HIVEMIND remembers across sessions:

- Project context and decisions
- Your preferences and coding style
- Learned patterns and solutions
- Team knowledge and best practices

### Pre-Built Workflows

Execute complex multi-agent pipelines:

- **Full SDLC** - Design -> Build -> Test -> Deploy
- **Security Assessment** - Threat model -> Pentest -> Report
- **Incident Response** - Detect -> Contain -> Recover
- **Code Review** - Static analysis -> Security scan -> Quality check

---

## Documentation

| Document | Description |
|----------|-------------|
| [Setup Guide](docs/SETUP-GUIDE.md) | Complete installation and configuration |
| [Quick Start](QUICKSTART.md) | Usage examples and common patterns |
| [Agent Reference](agents/) | Detailed agent capabilities |
| [Workflows](workflows/) | Pre-built automation pipelines |
| [Changelog](CHANGELOG.md) | Version history and updates |

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
# Optional: Set API keys instead of browser login
export OPENAI_API_KEY="sk-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### View Current Configuration

```bash
./hivemind --config
```

---

## Commands

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

## Project Structure

```
HIVEMIND/
├── hivemind              # Main executable
├── setup.sh              # One-command installer
├── config/
│   ├── engines.yaml      # Engine configuration
│   ├── hivemind.yaml     # System settings
│   └── routing.yaml      # Task routing rules
├── agents/
│   ├── dev/              # Development team agents
│   ├── security/         # Security team agents
│   ├── infrastructure/   # Infrastructure team agents
│   └── qa/               # QA team agents
├── workflows/            # Pre-built automation pipelines
├── memory/               # Persistent storage
├── bin/                  # Utility scripts
└── docs/                 # Documentation
```

---

## Contributing

Contributions are welcome! Here's how you can help:

- **Report Bugs** - Open an issue with details
- **Suggest Features** - We'd love to hear your ideas
- **Submit PRs** - Fork, branch, code, test, PR
- **Improve Docs** - Documentation improvements always appreciated

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Requirements

- **OS**: Linux or macOS (Windows via WSL)
- **Node.js**: 18.0 or higher
- **Accounts**: OpenAI + Anthropic (free tiers available)

---

## FAQ

<details>
<summary><b>What's the difference between Codex and Claude?</b></summary>

**Codex** (OpenAI) runs the HIVEMIND orchestrator - it receives your tasks, decides what agents are needed, and synthesizes the final response.

**Claude** (Anthropic) powers the 24 individual agents that do the specialized work.

This dual-engine approach gives you the best of both AI systems.
</details>

<details>
<summary><b>Do I need API keys?</b></summary>

Not necessarily! Both CLIs support browser-based authentication using your existing accounts. API keys are optional but provide more persistent authentication.
</details>

<details>
<summary><b>Is my data sent to external servers?</b></summary>

Yes, your prompts are sent to OpenAI (for Codex) and Anthropic (for Claude) for processing. No data is stored in this repository - the memory system only stores data locally on your machine.
</details>

<details>
<summary><b>Can I use only one AI provider?</b></summary>

Yes! Use `--preset full-codex` for OpenAI only, or `--preset full-claude` for Anthropic only.
</details>

<details>
<summary><b>How do I add custom agents?</b></summary>

Create a new `.md` file in the appropriate `agents/` subdirectory following the existing format. Then add the routing keywords in `config/routing.yaml`.
</details>

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

**HIVEMIND** - Route intelligently. Execute completely.

[Back to Top](#hivemind)

</div>
