# HIVEMIND

```
██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗
██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝
```

**Multi-Agent Orchestration System for Claude Code**

24 Agents | 4 Teams | Unified Intelligence

---

## Start Here

- `BOOTSTRAP.md` — single entry point + load sequence
- `INDEX.md` — complete file map
- `CLAUDE.md` — canonical operating rules

---

## What is HIVEMIND?

HIVEMIND is a prompt engineering framework that transforms Claude into a coordinated team of 24 specialized AI agents. Each agent has distinct expertise, communication protocols, and collaboration patterns.

**Use Cases:**
- Full-stack software development with architecture, coding, review, and testing
- Security assessments with penetration testing, threat modeling, and compliance
- Infrastructure design with cloud architecture, automation, and reliability
- Quality assurance with test strategy, automation, and performance testing

---

## Quick Setup

### 1. Navigate to HIVEMIND

```bash
cd /home/mintys/Desktop/HIVEMIND
```

### 2. Start Claude Code

```bash
claude
```

Claude automatically loads `CLAUDE.md` and becomes the HIVEMIND coordinator.

### 3. Start Using Agents

```bash
# Full system
"Design and implement a REST API for user management"

# Specific agent
"As DEV-001, design the architecture for a microservices platform"

# Specific team
"Security team, assess this codebase for vulnerabilities"

# Workflow
"Run full SDLC for implementing OAuth authentication"
```

---

## Directory Structure

```
HIVEMIND/
├── BOOTSTRAP.md                 # Single entry point (start here)
├── README.md                    # This file
├── CLAUDE.md                    # Auto-loaded by Claude Code (agent system)
├── HIVEMIND.md                  # Complete system documentation
├── QUICKSTART.md                # Quick reference guide
├── INDEX.md                     # Complete file map
├── CODEX.md                     # Codex entrypoint
├── CODEX-INSTRUCTIONS.md        # Codex activation + operating rules
│
├── agents/                      # 24 Agent Definitions
│   ├── development/             # DEV-001 to DEV-006
│   │   ├── architect.md
│   │   ├── backend-developer.md
│   │   ├── frontend-developer.md
│   │   ├── code-reviewer.md
│   │   ├── technical-writer.md
│   │   └── devops-liaison.md
│   ├── security/                # SEC-001 to SEC-006
│   │   ├── security-architect.md
│   │   ├── penetration-tester.md
│   │   ├── malware-analyst.md
│   │   ├── wireless-security-expert.md
│   │   ├── compliance-auditor.md
│   │   └── incident-responder.md
│   ├── infrastructure/          # INF-001 to INF-006
│   │   ├── infrastructure-architect.md
│   │   ├── systems-administrator.md
│   │   ├── network-engineer.md
│   │   ├── database-administrator.md
│   │   ├── site-reliability-engineer.md
│   │   └── automation-engineer.md
│   └── qa/                      # QA-001 to QA-006
│       ├── qa-architect.md
│       ├── test-automation-engineer.md
│       ├── performance-tester.md
│       ├── security-tester.md
│       ├── manual-qa-tester.md
│       └── test-data-manager.md
│   └── registry/                # ID-based registry entries
│       └── *.md
│
├── teams/                       # Team Configurations
│   ├── development.md
│   ├── security.md
│   ├── infrastructure.md
│   └── qa.md
│
├── workflows/                   # Multi-Agent Pipelines
│   ├── full-sdlc.md             # Design → Implement → Review → Test → Deploy
│   ├── security-assessment.md   # Scope → Recon → Test → Report
│   ├── code-review.md           # Submit → Check → Review → Approve
│   ├── incident-response.md     # Detect → Triage → Contain → Recover
│   ├── infrastructure-deploy.md # Plan → Stage → Deploy → Validate
│   └── compliance-audit.md      # Scope → Assess → Report → Remediate
│
├── protocols/                   # Communication Rules
│   ├── messages.md              # Structured message formats
│   ├── handoffs.md              # Work transfer between agents
│   ├── escalation.md            # When and how to escalate
│   ├── security-gates.md        # Quality/security checkpoints
│   └── QUALITY-GATES.md         # Pre-output validation gates
│
├── orchestration/               # Coordination Logic
│   ├── COORDINATOR.md           # Master orchestrator
│   ├── task-router.md           # Routes tasks to agents
│   └── context-manager.md       # Manages shared context
│
├── config/                      # Configuration Files
│   ├── README.md                # Config map
│   ├── agents.json              # Agent registry with metadata
│   ├── routing.json             # Task routing rules
│   ├── settings.json            # System settings
│   └── docs/
│       ├── globals.md           # Global variables
│       ├── output-standards.md  # Output format standards
│       └── tool-matrix.md       # Agent tool capabilities
│
├── memory/                      # Persistent Memory System
│   ├── MEMORY.md                # Memory system documentation
│   ├── MEMORY-PROTOCOL.md       # Memory operation protocols
│   ├── TRIGGERS.md              # Automatic memory triggers
│   ├── QUERY.md                 # Memory query interface
│   ├── ENGINE.md                # Active learning + memory engine reference
│   ├── learnings/               # Learning schema (active engine)
│   ├── short-term/              # Includes project-context.json
│   └── long-term/               # Includes user-profile.json
│   ├── schemas/                 # JSON schemas for memory types
│   ├── global/                  # System-wide memories
│   ├── teams/                   # Team-scoped memories
│   ├── agents/                  # Agent-specific memories
│   ├── projects/                # Project-isolated memories
│   ├── sessions/                # Session working memory
│   └── user/                    # User profile and preferences
│
├── templates/                   # Output Templates
│   ├── security-report.md
│   ├── architecture-decision-record.md
│   ├── incident-report.md
│   ├── code-review-findings.md
│   ├── test-results.md
│   └── deployment-checklist.md
│
├── .codex/
│   └── trigger.md               # Codex trigger documentation
└── .claude/
    └── commands/                # Slash Commands
        ├── hivemind.md          # /hivemind - Main orchestrator
        ├── dev.md               # /dev - Development team
        ├── sec.md               # /sec - Security team
        ├── infra.md             # /infra - Infrastructure team
        ├── qa.md                # /qa - QA team
        ├── architect.md         # /architect - DEV-001
        ├── pentest.md           # /pentest - SEC-002
        ├── sre.md               # /sre - INF-005
        ├── reviewer.md          # /reviewer - DEV-004
        ├── incident.md          # /incident - Incident response
        └── sdlc.md              # /sdlc - Full SDLC pipeline
```

---

## Agent Registry

### Development Team (DEV)

| ID | Agent | Expertise |
|:---|:------|:----------|
| DEV-001 | Architect | System design, API design, architecture patterns |
| DEV-002 | Backend Developer | APIs, server logic, databases, Python/Node/Go |
| DEV-003 | Frontend Developer | React, Vue, UI/UX, accessibility |
| DEV-004 | Code Reviewer | Code quality, security review, best practices |
| DEV-005 | Technical Writer | Documentation, API docs, guides |
| DEV-006 | DevOps Liaison | CI/CD, pipelines, deployment automation |

### Security Team (SEC)

| ID | Agent | Expertise |
|:---|:------|:----------|
| SEC-001 | Security Architect | Threat modeling, security design, defense strategy |
| SEC-002 | Penetration Tester | Ethical hacking, vulnerability assessment, OWASP |
| SEC-003 | Malware Analyst | Reverse engineering, binary analysis, IOCs |
| SEC-004 | Wireless Security Expert | WiFi, Bluetooth, RF security testing |
| SEC-005 | Compliance Auditor | SOC2, GDPR, PCI-DSS, HIPAA audits |
| SEC-006 | Incident Responder | Forensics, crisis management, containment |

### Infrastructure Team (INF)

| ID | Agent | Expertise |
|:---|:------|:----------|
| INF-001 | Infrastructure Architect | Cloud architecture, AWS/Azure/GCP, scaling |
| INF-002 | Systems Administrator | Linux/Windows, server hardening, configuration |
| INF-003 | Network Engineer | Firewalls, DNS, routing, VPN, network security |
| INF-004 | Database Administrator | PostgreSQL, MySQL, MongoDB, optimization |
| INF-005 | Site Reliability Engineer | Monitoring, SLOs, reliability, on-call |
| INF-006 | Automation Engineer | Terraform, Ansible, IaC, scripting |

### QA Team (QA)

| ID | Agent | Expertise |
|:---|:------|:----------|
| QA-001 | QA Architect | Test strategy, coverage analysis, quality process |
| QA-002 | Test Automation Engineer | Selenium, Playwright, pytest, test frameworks |
| QA-003 | Performance Tester | Load testing, stress testing, k6, JMeter |
| QA-004 | Security Tester | SAST, DAST, security scanning, DevSecOps |
| QA-005 | Manual QA Tester | Exploratory testing, UAT, bug hunting |
| QA-006 | Test Data Manager | Test data generation, fixtures, environments |

---

## Invocation Methods

### 1. Natural Language (Auto-Routes)

```
"Design a microservices architecture"          → DEV-001
"Find vulnerabilities in this code"            → SEC-002
"Set up Kubernetes monitoring"                 → INF-005
"Create automated tests for the API"           → QA-002
```

### 2. Direct Agent Invocation

```
"As DEV-001, design the database schema"
"As SEC-002, perform a security assessment"
"As INF-002, harden this server configuration"
"As QA-001, create a test strategy"
```

### 3. Team Invocation

```
"Development team, implement user authentication"
"Security team, assess the payment API"
"Infrastructure team, prepare for production deployment"
"QA team, run full regression testing"
```

### 4. Workflow Invocation

```
"Run full SDLC for implementing OAuth"
"Execute security assessment workflow"
"Start incident response for database outage"
"Run code review pipeline for PR #1234"
```

### 5. Slash Commands

```
/hivemind [task]     # Full system coordination
/architect [task]    # DEV-001 Architect
/pentest [task]      # SEC-002 Penetration Tester
/sre [task]          # INF-005 Site Reliability Engineer
/reviewer [task]     # DEV-004 Code Reviewer
/incident [desc]     # Incident Response workflow
/sdlc [project]      # Full SDLC workflow
```

---

## Configuration

### agents.json

Registry of all 24 agents with metadata, capabilities, and routing rules.

```json
{
  "agents": {
    "development": [
      {
        "id": "DEV-001",
        "name": "Architect",
        "role": "System Architect",
        "definition": "/agents/development/architect.md",
        "keywords": ["architecture", "design", "system", "api"],
        "capabilities": ["system_design", "api_design", "documentation"]
      }
    ]
  }
}
```

### routing.json

Task routing rules that map keywords to agents.

```json
{
  "routes": [
    {
      "keywords": ["design", "architecture", "blueprint"],
      "primary_agent": "DEV-001",
      "backup_agents": ["INF-001"]
    }
  ]
}
```

### settings.json

System-wide settings for escalation, quality gates, and integrations.

```json
{
  "defaults": {
    "escalation_timeout_minutes": 60
  },
  "quality_gates": {
    "code_coverage_threshold": 80,
    "security_scan_threshold": "no_critical_high"
  }
}
```

---

## Memory System

HIVEMIND includes a persistent memory system that remembers:

- **User preferences** - Coding style, tech stack, naming conventions
- **Project context** - Architecture decisions, codebase knowledge
- **Team learnings** - Bug patterns, solutions, best practices
- **Session state** - Current task, loaded memories, working context

Memory operations are automatic:

```
"Remember that we use snake_case for Python"     → Creates factual memory
"The fix for the auth bug was..."                → Creates procedural memory
"We decided to use PostgreSQL because..."        → Creates semantic memory
```

Query memory:

```
/recall deployment procedures
/memories
```

---

## Using HIVEMIND in Other Projects

To use HIVEMIND in another project (like VOIDWAVE):

### Method 1: Reference Path

```
"Use HIVEMIND from /home/mintys/Desktop/HIVEMIND for this task"
```

### Method 2: Copy CLAUDE.md

```bash
cp /home/mintys/Desktop/HIVEMIND/CLAUDE.md /path/to/your/project/
```

### Method 3: Symlink

```bash
ln -s /home/mintys/Desktop/HIVEMIND /path/to/your/project/HIVEMIND
```

### Method 4: Explicit Agent Invocation

Reference specific agents when working in any directory:

```
"Using HIVEMIND methodology, apply QA-001's test strategy approach"
"Following HIVEMIND's DEV-004 code review checklist, review this PR"
"As HIVEMIND SEC-002, assess this code for vulnerabilities"
```

---

## Files Reference

| File | Purpose |
|:-----|:--------|
| `CLAUDE.md` | Auto-loaded by Claude Code, contains full agent system |
| `HIVEMIND.md` | Complete system documentation |
| `QUICKSTART.md` | Quick reference and examples |
| `config/agents.json` | Agent registry |
| `config/routing.json` | Task routing rules |
| `config/settings.json` | System settings |
| `memory/MEMORY.md` | Memory system documentation |
| `orchestration/COORDINATOR.md` | Master coordinator logic |

---

## Extending HIVEMIND

### Add New Agent

1. Create agent definition: `agents/[team]/[agent].md`
2. Add to team config: `teams/[team].md`
3. Register in `config/agents.json`
4. Add routing rules: `config/routing.json`
5. (Optional) Create slash command: `.claude/commands/[agent].md`

### Add New Workflow

1. Create workflow: `workflows/[workflow].md`
2. Define phases, agents, gates
3. Create slash command if needed
4. Update COORDINATOR routing

---

## Priority & Escalation

| Priority | Response | Resolution | Triggers |
|:---------|:---------|:-----------|:---------|
| P0 | 15 min | 4 hours | "critical", "production down", "breach" |
| P1 | 1 hour | 24 hours | "urgent", "security vulnerability" |
| P2 | 4 hours | 72 hours | "important", "bug" |
| P3 | 24 hours | 1 week | "enhancement" |
| P4 | Best effort | Best effort | "docs", "nice to have" |

---

## Best Practices

1. **Be specific** - "Review auth code for SQL injection" > "Review code"
2. **Provide context** - Reference files, PRs, systems
3. **Name workflows** - "Run full SDLC" triggers complete pipeline
4. **Trust routing** - HIVEMIND auto-selects appropriate agents
5. **Use memory** - "Remember that..." persists preferences

---

*HIVEMIND — Unified Intelligence Through Coordinated Expertise*
