<div align="center">

# HIVEMIND v3.0

### AI Assistant with Multi-Agent Orchestration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Talk to Codex. Complex work gets Claude and 24 specialist agents.**

[Quick Start](#quick-start) |
[How It Works](#how-it-works) |
[Agents](#agents) |
[Installation](#installation)

</div>

---

## What is HIVEMIND?

HIVEMIND is an AI assistant that seamlessly escalates to multi-agent collaboration when needed.

**Simple questions?** Codex answers directly.

**Complex technical work?** Codex consults with Claude, they reach consensus, then specialist agents execute.

You always talk to one AI. The orchestration is invisible.

```
                    +-------------------+
                    |    YOU            |
                    +---------+---------+
                              |
                              v
              +-------------------------------+
              |           CODEX               |
              |    (Your AI Assistant)        |
              +---------------+---------------+
                              |
            Simple?           |           Complex?
           Answer ←───────────┴───────────→ Consult
           directly                         Claude
                                              |
                                              v
                              +-------------------------------+
                              |          CLAUDE               |
                              |    (Expert Consultant)        |
                              +---------------+---------------+
                                              |
                        +─────────────────────┼─────────────────────+
                        |                     |                     |
                        v                     v                     v
                 +-------------+       +-------------+       +-------------+
                 | DEVELOPMENT |       |  SECURITY   |       |     QA      |
                 |  6 agents   |       |  6 agents   |       |  6 agents   |
                 +-------------+       +-------------+       +-------------+
                        |                     |                     |
                        +─────────────────────┼─────────────────────+
                                              |
                                    +-------------------+
                                    | INFRASTRUCTURE    |
                                    |    6 agents       |
                                    +-------------------+
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND

# Install
./install.sh

# Run (from any directory)
hivemind
```

That's it. First run will prompt for Codex/Claude authentication.

---

## How It Works

### 1. You Talk to Codex

Codex is your primary AI assistant. It handles:
- Greetings and conversation
- Simple questions
- General explanations
- Quick lookups

### 2. Complex Work → Claude Consultation

When you ask for something substantial (build, design, implement, test, deploy, audit), Codex consults Claude:

1. **Codex proposes** an approach
2. **Claude evaluates** and suggests improvements
3. **Both iterate** until consensus
4. **Agents execute** the agreed plan
5. **Both verify** the output before delivery

### 3. Specialist Agents Execute

24 agents across 4 teams handle the actual work:

| Team | Agents |
|------|--------|
| Development | Architect, Backend, Frontend, Reviewer, Writer, DevOps |
| Security | SecArch, Pentester, Malware, Wireless, Compliance, Incident |
| Infrastructure | CloudArch, SysAdmin, Network, DBA, SRE, Automation |
| QA | QAArch, Automation, Performance, SecTest, Manual, TestData |

---

## Agents

### Development Team (DEV-001 to DEV-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| DEV-001 | Architect | System design, patterns, APIs, microservices |
| DEV-002 | Backend Developer | APIs, servers, databases, Python, Node, Java |
| DEV-003 | Frontend Developer | React, Vue, Angular, CSS, TypeScript |
| DEV-004 | Code Reviewer | Code quality, best practices, PR reviews |
| DEV-005 | Technical Writer | Documentation, guides, API docs |
| DEV-006 | DevOps Liaison | CI/CD, pipelines, deployment automation |

### Security Team (SEC-001 to SEC-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| SEC-001 | Security Architect | Threat modeling, security design |
| SEC-002 | Penetration Tester | Vulnerability assessment, exploits, OWASP |
| SEC-003 | Malware Analyst | Reverse engineering, threat analysis |
| SEC-004 | Wireless Security | WiFi, Bluetooth, RF, IoT security |
| SEC-005 | Compliance Auditor | NIST, SOC2, GDPR, PCI compliance |
| SEC-006 | Incident Responder | Breach response, forensics, recovery |

### Infrastructure Team (INF-001 to INF-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| INF-001 | Infrastructure Architect | AWS, GCP, Azure, cloud design |
| INF-002 | Systems Administrator | Linux, Windows, server management |
| INF-003 | Network Engineer | Firewalls, routing, DNS, VPCs |
| INF-004 | Database Administrator | PostgreSQL, MySQL, MongoDB, optimization |
| INF-005 | Site Reliability Engineer | Kubernetes, monitoring, reliability |
| INF-006 | Automation Engineer | Terraform, Ansible, IaC |

### QA Team (QA-001 to QA-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| QA-001 | QA Architect | Test strategy, coverage planning |
| QA-002 | Test Automation | Selenium, Cypress, pytest, frameworks |
| QA-003 | Performance Tester | Load testing, JMeter, k6, benchmarks |
| QA-004 | Security Tester | DAST, SAST, vulnerability scanning |
| QA-005 | Manual QA | Exploratory testing, UAT, regression |
| QA-006 | Test Data Manager | Fixtures, environments, test data |

---

## Installation

### Prerequisites

| Component | Requirement |
|-----------|-------------|
| **OS** | Linux or macOS |
| **Python** | 3.11+ |
| **Node.js** | 18+ (for Codex/Claude CLIs) |
| **Codex CLI** | `npm install -g @openai/codex` |
| **Claude CLI** | `npm install -g @anthropic-ai/claude-code` |

### Install HIVEMIND

```bash
# Clone the repo
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND

# Run installer
./install.sh
```

The installer:
- Creates `~/.local/share/hivemind/` installation
- Installs Python TUI dependencies
- Creates `hivemind` launcher in `~/.local/bin/`
- Sets up PATH if needed

### Run

```bash
# From any directory
hivemind

# Or with initial prompt
hivemind "Design a REST API for user management"
```

### Authentication

First run shows the auth screen:
- **Codex** - Browser OAuth or `OPENAI_API_KEY` env var
- **Claude** - Browser OAuth or `ANTHROPIC_API_KEY` env var

At minimum, Codex is required. Claude is optional but recommended.

---

## Usage Examples

### Simple Questions (Codex Direct)

```
> Hi
Hello! I'm Codex, your AI assistant. How can I help?

> What's a REST API?
A REST API is an architectural style for web services...

> Thanks!
You're welcome!
```

### Complex Work (Claude + Agents)

```
> Build a user authentication system with JWT

[Codex consults Claude...]
[Consensus reached]
[DEV-001 Architect] Designing auth architecture
[DEV-002 Backend] Implementing JWT endpoints
[SEC-001 Security] Reviewing auth security
[QA-002 Automation] Writing auth tests

Here's your complete authentication system:
[Full implementation with code, tests, and documentation]
```

### Work Requests That Trigger Agents

| You Say | Agents Involved |
|---------|-----------------|
| "Design a microservices architecture" | DEV-001 |
| "Build a REST API with auth" | DEV-001, DEV-002, SEC-001 |
| "Run a security audit" | SEC-001, SEC-002 |
| "Set up Kubernetes with monitoring" | INF-001, INF-005 |
| "Write tests for the payment module" | QA-001, QA-002 |
| "Deploy to production" | DEV-006, INF-005 |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `C` | Full chat screen |
| `M` | Main view |
| `Q` | Quit |
| `D` | Toggle dark mode |
| `?` | Help |
| `Ctrl+L` | Clear chat |
| `Esc` | Go back |

---

## Project Structure

```
HIVEMIND/
├── install.sh            # Installer
├── hivemind              # Dev launcher
├── config/
│   └── hivemind.yaml     # Configuration
├── tui/                  # TUI application
│   ├── src/hivemind_tui/
│   │   ├── app.py        # Main app
│   │   ├── engine/
│   │   │   ├── auth.py         # Authentication
│   │   │   ├── codex_head.py   # Codex (primary AI)
│   │   │   ├── claude_agent.py # Claude (consultant)
│   │   │   ├── dialogue.py     # Consensus system
│   │   │   └── coordinator.py  # Backward compat
│   │   ├── screens/
│   │   │   ├── auth_screen.py  # Auth screen
│   │   │   ├── main.py         # Main screen
│   │   │   └── chat.py         # Chat screen
│   │   └── widgets/
│   └── pyproject.toml
├── agents/
│   └── registry/         # Agent definitions
├── memory/               # Persistent storage
│   ├── short-term/
│   ├── long-term/
│   └── episodic/
└── workspace/            # Agent outputs
```

---

## Configuration

### Environment Variables

```bash
# Optional - browser auth works without these
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Config File

`config/hivemind.yaml` controls:
- Dialogue settings (max turns, verification)
- Agent timeouts
- Output preferences
- TUI theme

---

## Requirements

| Component | Version |
|-----------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| Codex CLI | Latest |
| Claude CLI | Latest |

---

## FAQ

<details>
<summary><b>What's the difference between Codex and Claude?</b></summary>

**Codex** is your primary AI assistant. You always talk to Codex.

**Claude** is the expert consultant. When you need complex work done, Codex consults with Claude to plan the approach, then Claude supervises the specialist agents.

You never talk directly to Claude - Codex presents everything to you.
</details>

<details>
<summary><b>Do I need both Codex and Claude?</b></summary>

**Codex is required** - it's your primary interface.

**Claude is optional** - but without it, complex multi-agent work won't be available. Simple questions will still work.
</details>

<details>
<summary><b>Do I need API keys?</b></summary>

No. Both Codex and Claude support browser-based authentication. API keys are optional but provide more persistent auth.
</details>

<details>
<summary><b>Is my data sent externally?</b></summary>

Yes. Prompts are sent to OpenAI (Codex) and Anthropic (Claude) for processing. Local memory stores conversation history and preferences only.
</details>

<details>
<summary><b>Can I add custom agents?</b></summary>

The 24 agents are defined in `engine/claude_agent.py`. You can modify the AGENTS dictionary to add or customize agents.
</details>

---

## License

MIT License - see [LICENSE](LICENSE).

---

<div align="center">

**HIVEMIND v3.0** - Talk naturally. Work gets done.

[Back to Top](#hivemind-v30)

</div>
