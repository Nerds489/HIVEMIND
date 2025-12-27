<div align="center">

```
██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗
██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝
```

### Multi-Agent AI Orchestration System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Agents](https://img.shields.io/badge/agents-24-green.svg)](#agent-teams)

**24 specialized AI agents. 4 teams. 1 unified interface.**

[Quick Start](#quick-start) • [How It Works](#how-it-works) • [Commands](#commands) • [Agents](#agent-teams) • [Install](#installation)

</div>

---

## What is HIVEMIND?

HIVEMIND orchestrates 24 specialized AI agents across Development, Security, Infrastructure, and QA teams to accomplish complex technical tasks. You give it a task—it routes to the right agents, executes in parallel where possible, validates through quality gates, and delivers a consolidated report.

```
USER REQUEST
     │
     ▼
┌─────────────────────────────────────────┐
│         HEAD_CODEX (Orchestrator)       │
│  • Parse intent  • Route to agents      │
│  • Coordinate    • Generate report      │
└─────────────────────────────────────────┘
     │
     ├──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│   DEV   │  │   SEC   │  │   INF   │  │   QA    │
│ 6 agents│  │ 6 agents│  │ 6 agents│  │ 6 agents│
└─────────┘  └─────────┘  └─────────┘  └─────────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                         │
                         ▼
               ┌─────────────────┐
               │  QUALITY GATES  │
               │  G1→G2→G3→G4→G5 │
               └─────────────────┘
                         │
                         ▼
               ┌─────────────────┐
               │ EXECUTION REPORT│
               └─────────────────┘
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND

# Install
./install.sh

# Run
hivemind
```

---

## How It Works

### Agent Output Format

Every agent reports status in **2-4 words maximum**:

```
[DEV-001] Designing architecture
[SEC-002] Scanning endpoints
[QA-003] Running load tests
[INF-005] Deploying containers
```

### Parallel Execution

Independent tasks run simultaneously:

```
┌─────────┬─────────┬─────────┐
│ DEV-001 │ SEC-001 │ QA-001  │
│Designing│Modeling │Planning │
└─────────┴─────────┴─────────┘
```

### Sequential Handoffs

Dependent tasks chain together:

```
DEV-002 ──→ DEV-004 ──→ QA-002 ──→ INF-005
Building    Reviewing   Testing    Deploying
```

### Quality Gates

Work passes through validation gates:

| Gate | Name | Purpose |
|------|------|---------|
| G1 | Design | Architecture approved |
| G2 | Security | No critical vulnerabilities |
| G3 | Code | Code review passed |
| G4 | Test | All tests passing |
| G5 | Deploy | Deployment ready |

---

## Commands

| Command | Description |
|---------|-------------|
| `/hivemind [task]` | Full multi-agent orchestration |
| `/dev [task]` | Development team only |
| `/sec [task]` | Security team only |
| `/infra [task]` | Infrastructure team only |
| `/qa [task]` | QA team only |
| `/architect [task]` | Route to DEV-001 |
| `/pentest [task]` | Route to SEC-002 |
| `/sre [task]` | Route to INF-005 |
| `/reviewer [task]` | Route to DEV-004 |
| `/status` | System status |
| `/recall [query]` | Memory recall |
| `/debug [task]` | Verbose routing |
| `/note [msg]` | Live input during execution |

---

## Agent Teams

### DEV — Development Team

| ID | Role | Focus |
|----|------|-------|
| DEV-001 | Architect | System design, patterns, APIs, microservices |
| DEV-002 | Backend Developer | APIs, servers, databases, Python, Node |
| DEV-003 | Frontend Developer | UI/UX, React, Vue, Angular, CSS |
| DEV-004 | Code Reviewer | Code quality, PRs, best practices |
| DEV-005 | Technical Writer | Documentation, guides, API docs |
| DEV-006 | DevOps Liaison | CI/CD, pipelines, deployment automation |

### SEC — Security Team

| ID | Role | Focus |
|----|------|-------|
| SEC-001 | Security Architect | Threat modeling, security design, risk |
| SEC-002 | Penetration Tester | Vulnerability assessment, OWASP, exploits |
| SEC-003 | Malware Analyst | Reverse engineering, threat analysis, IOCs |
| SEC-004 | Wireless Security | WiFi, Bluetooth, RF, IoT security |
| SEC-005 | Compliance Auditor | SOC2, GDPR, PCI, NIST, regulatory |
| SEC-006 | Incident Responder | Breach response, forensics, containment |

### INF — Infrastructure Team

| ID | Role | Focus |
|----|------|-------|
| INF-001 | Infrastructure Architect | Cloud design, AWS, GCP, Azure |
| INF-002 | Systems Administrator | Linux, Windows, server configuration |
| INF-003 | Network Engineer | Firewalls, DNS, routing, VPCs |
| INF-004 | Database Administrator | PostgreSQL, MySQL, MongoDB, optimization |
| INF-005 | Site Reliability Engineer | Kubernetes, monitoring, reliability |
| INF-006 | Automation Engineer | Terraform, Ansible, IaC, scripting |

### QA — Quality Assurance Team

| ID | Role | Focus |
|----|------|-------|
| QA-001 | QA Architect | Test strategy, coverage, quality planning |
| QA-002 | Test Automation | Selenium, Cypress, pytest, frameworks |
| QA-003 | Performance Tester | Load testing, JMeter, k6, benchmarks |
| QA-004 | Security Tester | DAST, SAST, vulnerability scanning |
| QA-005 | Manual QA | Exploratory testing, UAT, regression |
| QA-006 | Test Data Manager | Fixtures, test environments, data seeding |

---

## Example Execution

**Task**: `Build a REST API with authentication and deploy to Kubernetes`

```
[DEV-001] Designing API architecture
[SEC-001] Threat modeling auth
[DEV-002] Building REST endpoints
[DEV-002] Implementing JWT auth
[DEV-004] Reviewing implementation
[SEC-002] Testing auth security
[QA-001] Creating test strategy
[QA-002] Writing API tests
[QA-003] Load testing endpoints
[INF-001] Designing K8s architecture
[INF-005] Configuring deployment
[INF-006] Writing Helm charts

[GATE] G1-DESIGN: PASSED
[GATE] G2-SECURITY: PASSED
[GATE] G3-CODE: PASSED
[GATE] G4-TEST: PASSED
[GATE] G5-DEPLOY: READY

╔══════════════════════════════════════════════════════════════╗
║                    HIVEMIND EXECUTION REPORT                  ║
╠══════════════════════════════════════════════════════════════╣
║ Task: REST API with JWT Auth + Kubernetes Deployment          ║
║ Status: COMPLETE                                              ║
╠══════════════════════════════════════════════════════════════╣
║ AGENTS ENGAGED: 11                                            ║
║ • DEV-001 Architect ............ Complete                     ║
║ • SEC-001 Security Architect ... Complete                     ║
║ • DEV-002 Backend Developer .... Complete                     ║
║ • DEV-004 Code Reviewer ........ Complete                     ║
║ • SEC-002 Penetration Tester ... Complete                     ║
║ • QA-001 QA Architect .......... Complete                     ║
║ • QA-002 Test Automation ....... Complete                     ║
║ • QA-003 Performance Tester .... Complete                     ║
║ • INF-001 Infrastructure Arch .. Complete                     ║
║ • INF-005 SRE .................. Complete                     ║
║ • INF-006 Automation Engineer .. Complete                     ║
╠══════════════════════════════════════════════════════════════╣
║ DELIVERABLES:                                                 ║
║ • REST API with CRUD endpoints                                ║
║ • JWT authentication with refresh tokens                      ║
║ • API test suite (94 tests, 100% pass)                        ║
║ • Security assessment (0 critical findings)                   ║
║ • Kubernetes manifests + Helm chart                           ║
║ • CI/CD pipeline configuration                                ║
╠══════════════════════════════════════════════════════════════╣
║ SUMMARY:                                                      ║
║ Production-ready REST API with JWT auth deployed to K8s.      ║
║ Security validated. Load tested at 8,000 req/sec.             ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Installation

### Prerequisites

| Component | Version |
|-----------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| Codex CLI | `npm install -g @openai/codex` |
| Claude CLI | `npm install -g @anthropic-ai/claude-code` |

### Install

```bash
./install.sh
```

### Uninstall

```bash
./uninstall.sh
```

---

## Configuration

### Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Optional (browser auth works)
export ANTHROPIC_API_KEY="sk-ant-..."    # Optional (browser auth works)
export HIVEMIND_THEME="cyberpunk-matrix" # Theme override
```

### Config File

`config/hivemind.yaml` controls agent timeouts, output preferences, and TUI settings.

---

## Keyboard Shortcuts

### Main Screen

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `C` | Full chat screen |
| `M` | Main view |
| `Q` | Quit |
| `Ctrl+O` | Status log |
| `Ctrl+C` | Cancel task |

### Chat Screen

| Key | Action |
|-----|--------|
| `Ctrl+Enter` | Send message |
| `Ctrl+L` | Clear history |
| `Ctrl+C` | Cancel task |
| `Esc` | Back |

---

## Memory System

HIVEMIND maintains contextual memory:

```
memory/
├── short-term/     # Session-scoped
├── long-term/      # Persistent learnings, preferences, decisions
└── episodic/       # Events and milestones
```

| Trigger | Storage |
|---------|---------|
| "Remember that..." | `long-term/learnings.json` |
| "We decided..." | `long-term/decisions.json` |
| "I prefer..." | `long-term/preferences.json` |
| "Our stack is..." | `long-term/project.json` |

---

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

**HIVEMIND** — Orchestrate Silently. Report Completely.

[Back to Top](#)

</div>
