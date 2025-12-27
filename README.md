<div align="center">

<br>

# 🐝 HIVEMIND

### Multi-Agent AI Orchestration System

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Agents](https://img.shields.io/badge/AI_Agents-24-00D26A.svg?style=for-the-badge)](#-the-hive)
[![Teams](https://img.shields.io/badge/Teams-4-7C3AED.svg?style=for-the-badge)](#-the-hive)

<br>

**One command. 24 AI agents. Infinite possibilities.**

<br>

[Quick Start](#-quick-start) • [The Hive](#-the-hive) • [Commands](#-commands) • [Examples](#-live-example) • [Install](#-installation)

<br>

---

<br>

</div>

## 🧠 What is HIVEMIND?

<div align="center">

**HIVEMIND** coordinates 24 specialized AI agents across 4 teams to accomplish complex technical tasks.

Instead of one AI doing everything, HIVEMIND routes your request to the right specialists—architects, security experts, infrastructure engineers, and QA professionals—who work together to deliver production-grade results.

<br>

```
                         YOUR REQUEST
                              │
                              ▼
                    ┌─────────────────┐
                    │   HEAD_CODEX    │
                    │  ─────────────  │
                    │   Orchestrator  │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
     ┌───────────┐    ┌───────────┐    ┌───────────┐
     │    DEV    │    │    SEC    │    │    INF    │
     │ 6 Agents  │    │ 6 Agents  │    │ 6 Agents  │
     └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    QA TEAM    │
                    │   6 Agents    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ QUALITY GATES │
                    │ G1→G2→G3→G4→G5│
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    REPORT     │
                    └───────────────┘
```

</div>

<br>

---

<br>

## ⚡ Quick Start

<div align="center">

```bash
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND
./install.sh
hivemind
```

**That's it. You're in.**

</div>

<br>

---

<br>

## 🐝 The Hive

<div align="center">

### 💻 Development Team — `DEV`

*Build it right.*

</div>

| Agent | Role | Specialty |
|:------|:-----|:----------|
| `DEV-001` | **Architect** | System design, patterns, APIs, microservices |
| `DEV-002` | **Backend Developer** | APIs, servers, databases, Python, Node.js |
| `DEV-003` | **Frontend Developer** | UI/UX, React, Vue, Angular, TypeScript |
| `DEV-004` | **Code Reviewer** | Code quality, pull requests, best practices |
| `DEV-005` | **Technical Writer** | Documentation, guides, API docs |
| `DEV-006` | **DevOps Liaison** | CI/CD, pipelines, GitHub Actions |

<br>

<div align="center">

### 🔐 Security Team — `SEC`

*Break it before they do.*

</div>

| Agent | Role | Specialty |
|:------|:-----|:----------|
| `SEC-001` | **Security Architect** | Threat modeling, security design, risk |
| `SEC-002` | **Penetration Tester** | Vulnerability assessment, OWASP, exploits |
| `SEC-003` | **Malware Analyst** | Reverse engineering, threat analysis, IOCs |
| `SEC-004` | **Wireless Security** | WiFi, Bluetooth, RF, IoT security |
| `SEC-005` | **Compliance Auditor** | SOC2, GDPR, PCI-DSS, NIST |
| `SEC-006` | **Incident Responder** | Breach response, forensics, containment |

<br>

<div align="center">

### ☁️ Infrastructure Team — `INF`

*Run it at scale.*

</div>

| Agent | Role | Specialty |
|:------|:-----|:----------|
| `INF-001` | **Infrastructure Architect** | Cloud design, AWS, GCP, Azure |
| `INF-002` | **Systems Administrator** | Linux, Windows, configuration |
| `INF-003` | **Network Engineer** | Firewalls, DNS, routing, VPCs |
| `INF-004` | **Database Administrator** | PostgreSQL, MySQL, MongoDB |
| `INF-005` | **Site Reliability Engineer** | Kubernetes, monitoring, SLOs |
| `INF-006` | **Automation Engineer** | Terraform, Ansible, IaC |

<br>

<div align="center">

### ✅ Quality Assurance Team — `QA`

*Prove it works.*

</div>

| Agent | Role | Specialty |
|:------|:-----|:----------|
| `QA-001` | **QA Architect** | Test strategy, coverage, quality planning |
| `QA-002` | **Test Automation** | Selenium, Cypress, pytest, frameworks |
| `QA-003` | **Performance Tester** | Load testing, JMeter, k6, benchmarks |
| `QA-004` | **Security Tester** | DAST, SAST, vulnerability scanning |
| `QA-005` | **Manual QA** | Exploratory testing, UAT, regression |
| `QA-006` | **Test Data Manager** | Fixtures, test environments, seeding |

<br>

---

<br>

## 🎮 Commands

<div align="center">

| Command | Description |
|:--------|:------------|
| `/hivemind [task]` | Full multi-agent orchestration |
| `/dev [task]` | Route to Development team |
| `/sec [task]` | Route to Security team |
| `/infra [task]` | Route to Infrastructure team |
| `/qa [task]` | Route to QA team |
| `/architect [task]` | Direct to DEV-001 |
| `/pentest [task]` | Direct to SEC-002 |
| `/sre [task]` | Direct to INF-005 |
| `/reviewer [task]` | Direct to DEV-004 |
| `/status` | System status |
| `/recall [query]` | Query memory |

</div>

<br>

---

<br>

## 🎬 Live Example

<div align="center">

**Input:**

```
Build a REST API with JWT authentication and deploy to Kubernetes
```

**Agent Execution:**

```
[DEV-001] Designing architecture
[SEC-001] Threat modeling auth
[DEV-002] Building endpoints
[DEV-004] Reviewing code
[SEC-002] Testing security
[QA-002] Writing tests
[QA-003] Load testing
[INF-001] K8s architecture
[INF-005] Configuring deploy
[INF-006] Writing Helm charts
```

**Quality Gates:**

```
[GATE] G1-DESIGN .... PASSED
[GATE] G2-SECURITY .. PASSED
[GATE] G3-CODE ...... PASSED
[GATE] G4-TEST ...... PASSED
[GATE] G5-DEPLOY .... READY
```

**Execution Report:**

```
╔════════════════════════════════════════════════╗
║          HIVEMIND EXECUTION REPORT             ║
╠════════════════════════════════════════════════╣
║  Task: REST API + JWT + K8s Deploy             ║
║  Status: COMPLETE                              ║
╠════════════════════════════════════════════════╣
║  AGENTS: 11 engaged                            ║
║  ────────────────────────────────              ║
║  DEV-001 Architect .......... Complete         ║
║  SEC-001 Security Arch ...... Complete         ║
║  DEV-002 Backend Dev ........ Complete         ║
║  DEV-004 Code Reviewer ...... Complete         ║
║  SEC-002 Pentester .......... Complete         ║
║  QA-002  Test Automation .... Complete         ║
║  QA-003  Performance ........ Complete         ║
║  INF-001 Infra Architect .... Complete         ║
║  INF-005 SRE ................ Complete         ║
║  INF-006 Automation ......... Complete         ║
╠════════════════════════════════════════════════╣
║  DELIVERABLES:                                 ║
║  • REST API with CRUD endpoints                ║
║  • JWT auth + refresh tokens                   ║
║  • RBAC implementation                         ║
║  • Test suite (94 tests, 100% pass)            ║
║  • Security report (0 critical)                ║
║  • K8s manifests + Helm chart                  ║
║  • CI/CD pipeline                              ║
╠════════════════════════════════════════════════╣
║  Load tested at 8,000 req/sec                  ║
║  Auto-scaling configured                       ║
╚════════════════════════════════════════════════╝
```

</div>

<br>

---

<br>

## 🚦 Quality Gates

<div align="center">

Every task passes through validation before completion:

```
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│   G1   │ → │   G2   │ → │   G3   │ → │   G4   │ → │   G5   │
│ DESIGN │   │SECURITY│   │  CODE  │   │  TEST  │   │ DEPLOY │
└────────┘   └────────┘   └────────┘   └────────┘   └────────┘
     │            │            │            │            │
     ▼            ▼            ▼            ▼            ▼
  Arch OK     No vulns     Review OK   Tests pass   Ready
```

</div>

<br>

---

<br>

## 🔀 Execution Patterns

<div align="center">

### Parallel Execution

*Independent tasks run simultaneously*

```
  DEV-001      SEC-001      INF-001      QA-001
     │            │            │            │
     ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Designing│ │Modeling │ │Planning │ │Strategy │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     └───────────┴───────────┴───────────┘
                      │
                      ▼
                 [ COMBINE ]
```

### Sequential Execution

*Dependent tasks chain together*

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ DEV-002 │ → │ DEV-004 │ → │  QA-002 │ → │ INF-005 │
│ Building│   │Reviewing│   │ Testing │   │Deploying│
└─────────┘   └─────────┘   └─────────┘   └─────────┘
```

</div>

<br>

---

<br>

## 📦 Installation

<div align="center">

### Prerequisites

| Requirement | Version |
|:------------|:--------|
| Python | 3.11+ |
| Node.js | 18+ |
| Codex CLI | `npm install -g @openai/codex` |
| Claude CLI | `npm install -g @anthropic-ai/claude-code` |

### Commands

```bash
# Install
./install.sh

# Run
hivemind

# Uninstall
./uninstall.sh
```

</div>

<br>

---

<br>

## ⚙️ Configuration

<div align="center">

### Environment Variables

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export HIVEMIND_THEME="cyberpunk-matrix"
```

### Config Files

```
config/
├── hivemind.yaml    # Main config
├── agents.json      # Agent definitions
├── routing.json     # Task routing
└── engines.yaml     # AI engines
```

</div>

<br>

---

<br>

## ⌨️ Keyboard Shortcuts

<div align="center">

| Key | Action |
|:----|:-------|
| `Enter` | Send message |
| `C` | Full chat mode |
| `M` | Main view |
| `Q` | Quit |
| `Ctrl+O` | Status log |
| `Ctrl+C` | Cancel task |
| `Ctrl+Enter` | Send (chat) |
| `Ctrl+L` | Clear history |
| `Esc` | Back |

</div>

<br>

---

<br>

## 📁 Project Structure

<div align="center">

```
HIVEMIND/
├── agents/        # Agent definitions (24 specs)
├── comms/         # Inter-agent protocols
├── config/        # System configuration
├── core/          # Orchestrator logic
├── memory/        # Persistent memory
├── protocols/     # Quality gates
├── runtime/       # Execution controllers
├── teams/         # Team configurations
├── templates/     # Output templates
├── tests/         # Test suite
├── tui/           # Terminal UI
├── workflows/     # Process playbooks
├── hivemind       # Main executable
└── CLAUDE.md      # System prompt
```

</div>

<br>

---

<br>

## 🧠 Memory System

<div align="center">

HIVEMIND remembers across sessions.

```
memory/
├── short-term/    # Session (clears on exit)
├── long-term/     # Permanent storage
│   ├── learnings
│   ├── preferences
│   ├── decisions
│   └── project
└── episodic/      # Events & milestones
```

### Triggers

| You say... | HIVEMIND stores... |
|:-----------|:-------------------|
| "Remember that..." | → learnings |
| "We decided..." | → decisions |
| "I prefer..." | → preferences |
| "Our stack is..." | → project |

</div>

<br>

---

<br>

<div align="center">

## 📄 License

MIT License — see [LICENSE](LICENSE)

<br>

---

<br>

### 🐝 HIVEMIND

**Orchestrate Silently. Report Completely.**

<br>

[⬆ Back to Top](#-hivemind)

</div>
