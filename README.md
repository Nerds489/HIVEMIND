<div align="center">

# HIVEMIND v3.0

### AI Assistant with Multi-Agent Orchestration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

<pre>
H   H III V   V EEEEE M   M III N   N DDDD
H   H  I  V   V E     MM MM  I  NN  N D   D
HHHHH  I  V   V EEEE  M M M  I  N N N D   D
H   H  I   V V  E     M   M  I  N  NN D   D
H   H III   V   EEEEE M   M III N   N DDDD
</pre>

<pre>
+--------------------------------------+
|               HIVEMIND               |
|  Unified Multi-Agent Orchestration   |
+--------------------------------------+
</pre>

Talk to Codex. Complex work brings Claude and 24 specialist agents.

[Quick Start](#quick-start) | [How It Works](#how-it-works) | [Usage](#usage) | [Install](#install) | [Shortcuts](#keyboard-shortcuts)

</div>

---

## What is HIVEMIND?

HIVEMIND is a unified AI assistant that escalates to coordinated multi-agent work when tasks get complex.

- Simple requests are answered directly by Codex.
- Complex requests trigger a Codex + Claude planning loop.
- Claude executes specialist agents and reports back.
- Codex and Claude both agree before you get the final response.

The orchestration is internal. You only talk to one AI.

---

## Features

- Codex + Claude consensus planning
- 24 agents across DEV, SEC, INF, QA
- Quality gates and verification before delivery
- Live status updates and a status log popup
- Live input injection during planning/review via /note
- Cancel any task with Ctrl+C
- Cyberpunk/matrix theme
- Global Codex trusted-directory skip enabled

---

## Quick Start

```bash
# Clone
git clone https://github.com/Nerds489/HIVEMIND.git
cd HIVEMIND

# Install (do not use sudo)
./install.sh

# Run from any directory
hivemind
```

First run opens the auth screen for Codex and Claude.

---

## How It Works

1) You send a message to Codex.
2) If it is complex, Codex consults Claude.
3) They iterate until they agree on the plan and agents.
4) Claude runs the agents.
5) Codex and Claude both verify the output.
6) Only then does Codex respond to you.

---

## Usage

### Commands

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

### Live Input During Planning/Review

If you want to steer the plan or the review while work is running:

```
/note prioritize security review before performance tuning
```

Notes sent while no task is running are queued for the next task.

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

## Agents

### Development Team (DEV-001 to DEV-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| DEV-001 | Architect | System design, patterns, APIs |
| DEV-002 | Backend Developer | APIs, servers, databases |
| DEV-003 | Frontend Developer | UI, UX, web apps |
| DEV-004 | Code Reviewer | Code quality, best practices |
| DEV-005 | Technical Writer | Docs, guides, API docs |
| DEV-006 | DevOps Liaison | CI/CD, deployment |

### Security Team (SEC-001 to SEC-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| SEC-001 | Security Architect | Threat modeling, security design |
| SEC-002 | Penetration Tester | Vulnerability assessment |
| SEC-003 | Malware Analyst | Threat analysis |
| SEC-004 | Wireless Security | WiFi, Bluetooth, IoT |
| SEC-005 | Compliance Auditor | SOC2, GDPR, PCI |
| SEC-006 | Incident Responder | Breach response |

### Infrastructure Team (INF-001 to INF-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| INF-001 | Infrastructure Architect | Cloud design |
| INF-002 | Systems Administrator | Linux/Windows |
| INF-003 | Network Engineer | DNS, routing, firewalls |
| INF-004 | Database Administrator | Postgres, MySQL, MongoDB |
| INF-005 | Site Reliability Engineer | Reliability, monitoring |
| INF-006 | Automation Engineer | Terraform, Ansible |

### QA Team (QA-001 to QA-006)

| ID | Agent | Expertise |
|----|-------|-----------|
| QA-001 | QA Architect | Test strategy |
| QA-002 | Test Automation | Automation frameworks |
| QA-003 | Performance Tester | Load testing |
| QA-004 | Security Tester | DAST, SAST |
| QA-005 | Manual QA | Exploratory testing |
| QA-006 | Test Data Manager | Fixtures, data |

---

## Install

### Prerequisites

| Component | Requirement |
|-----------|-------------|
| OS | Linux or macOS |
| Python | 3.11+ |
| Node.js | 18+ |
| Codex CLI | npm install -g @openai/codex |
| Claude CLI | npm install -g @anthropic-ai/claude-code |

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
# Optional - browser auth works without these
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Theme override
export HIVEMIND_THEME="cyberpunk-matrix"
```

### Config File

`config/hivemind.yaml` controls:
- Dialogue and verification settings
- Agent timeouts
- Output preferences
- TUI settings

---

## Troubleshooting

### Codex trusted directory error

HIVEMIND skips the Codex trusted-directory check globally. If you still see a trust error, confirm the `codex` CLI is updated.

### CLI not found

```bash
which codex
which claude
```

If missing, reinstall the CLIs.

---

## License

MIT License - see LICENSE.

---

<div align="center">

HIVEMIND v3.0 - Talk naturally. Work gets done.

[Back to Top](#hivemind-v30)

</div>
