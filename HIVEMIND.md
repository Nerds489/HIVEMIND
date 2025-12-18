# HIVEMIND Multi-Agent Orchestration System

Start here:
- `BOOTSTRAP.md` (single entry point + load sequence)
- `CLAUDE.md` (canonical operating rules)

```
██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗
██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝

         24 Agents • 4 Teams • 1 Unified System
```

## Overview

HIVEMIND is a multi-agent orchestration system designed to coordinate 24 specialized AI agents across 4 functional teams. Each agent has distinct expertise, responsibilities, and collaboration patterns that work together to deliver comprehensive software development, security, infrastructure, and quality assurance capabilities.

---

## Quick Start

### Invoke the Full System
```
/hivemind [your request]
```

### Invoke Specific Teams
```
/dev [development request]      # Development Team
/sec [security request]         # Security Team
/infra [infrastructure request] # Infrastructure Team
/qa [quality request]           # QA Team
```

### Invoke Specific Agents
```
/architect [design request]     # DEV-001 Architect
/pentest [security request]     # SEC-002 Penetration Tester
/sre [reliability request]      # INF-005 SRE
/reviewer [review request]      # DEV-004 Code Reviewer
```

### Invoke Workflows
```
/sdlc [project]                 # Full SDLC Pipeline
/incident [description]         # Incident Response
```

---

## System Architecture

```
                           ┌─────────────────┐
                           │   COORDINATOR   │
                           │   (Orchestrator)│
                           └────────┬────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   DEVELOPMENT   │      │    SECURITY     │      │ INFRASTRUCTURE  │
│      TEAM       │◄────►│      TEAM       │◄────►│      TEAM       │
│    (6 agents)   │      │    (6 agents)   │      │    (6 agents)   │
└────────┬────────┘      └────────┬────────┘      └────────┬────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                                  ▼
                       ┌─────────────────┐
                       │    QA TEAM      │
                       │   (6 agents)    │
                       └─────────────────┘
```

---

## Teams & Agents

### Development & Architecture Team
| ID | Role | Primary Focus |
|----|------|---------------|
| DEV-001 | Architect | System design, architecture decisions |
| DEV-002 | Backend Developer | Server-side code, APIs, databases |
| DEV-003 | Frontend Developer | UI/UX, client-side applications |
| DEV-004 | Code Reviewer | Code quality, review, best practices |
| DEV-005 | Technical Writer | Documentation, API docs, guides |
| DEV-006 | DevOps Liaison | CI/CD, pipelines, developer experience |

### Security & Offensive Operations Team
| ID | Role | Primary Focus |
|----|------|---------------|
| SEC-001 | Security Architect | Security design, threat modeling |
| SEC-002 | Penetration Tester | Offensive security, vulnerability testing |
| SEC-003 | Malware Analyst | Malware analysis, reverse engineering |
| SEC-004 | Wireless Security Expert | WiFi, Bluetooth, RF security |
| SEC-005 | Compliance Auditor | Regulatory compliance, audits |
| SEC-006 | Incident Responder | Security incidents, forensics |

### Infrastructure & Operations Team
| ID | Role | Primary Focus |
|----|------|---------------|
| INF-001 | Infrastructure Architect | Cloud architecture, infrastructure design |
| INF-002 | Systems Administrator | System management, configuration |
| INF-003 | Network Engineer | Networking, firewalls, connectivity |
| INF-004 | Database Administrator | Database management, optimization |
| INF-005 | Site Reliability Engineer | Reliability, monitoring, on-call |
| INF-006 | Automation Engineer | Infrastructure automation, IaC |

### Quality Assurance & Validation Team
| ID | Role | Primary Focus |
|----|------|---------------|
| QA-001 | QA Architect | Test strategy, quality processes |
| QA-002 | Test Automation Engineer | Automated testing, frameworks |
| QA-003 | Performance Tester | Load testing, performance analysis |
| QA-004 | Security Tester | Security testing, SAST/DAST |
| QA-005 | Manual QA Tester | Exploratory testing, UAT |
| QA-006 | Test Data Manager | Test data, environments |

---

## Workflows

### Full SDLC Pipeline
Complete software development lifecycle from design to deployment.
```
DESIGN → IMPLEMENT → REVIEW → TEST → DEPLOY → VALIDATE
```
Use: `/sdlc [project/feature]`

### Security Assessment
Comprehensive security testing from scoping to remediation.
```
SCOPE → RECON → TEST → REPORT → VERIFY
```
Use: `/sec security assessment for [target]`

### Code Review Pipeline
Structured code review with automated and manual checks.
```
SUBMIT → AUTOMATED CHECKS → PEER REVIEW → SECURITY → APPROVE → MERGE
```
Use: `/reviewer [PR/code]`

### Incident Response
Security and reliability incident handling.
```
DETECT → TRIAGE → CONTAIN → INVESTIGATE → ERADICATE → RECOVER
```
Use: `/incident [description]`

---

## Protocols

### Communication Protocol
Agents communicate using structured messages:
- **REQUEST:** Task assignments
- **RESPONSE:** Task completions
- **ALERT:** Urgent notifications
- **STATUS:** Progress updates
- **QUERY:** Information requests

### Escalation Protocol
Five-level escalation hierarchy:
1. **Self-resolution** — Agent handles independently
2. **Peer consultation** — Ask same-team agent
3. **Team lead** — Escalate within team
4. **Cross-team** — Coordinate with other teams
5. **Human escalation** — Request human intervention

### Handoff Protocol
Work transfer between agents includes:
- Context summary
- Artifacts and deliverables
- Open questions
- Success criteria
- Next steps

### Security Gates
Mandatory checkpoints:
- Code Merge Gate
- Production Deployment Gate
- Security Assessment Publication Gate
- Infrastructure Change Gate
- Incident Declaration Gate

---

## Directory Structure

```
HIVEMIND/
├── HIVEMIND.md                 # This file - system overview
├── agents/                     # Agent definitions
│   ├── development/            # DEV-001 through DEV-006
│   ├── security/               # SEC-001 through SEC-006
│   ├── infrastructure/         # INF-001 through INF-006
│   └── qa/                     # QA-001 through QA-006
├── teams/                      # Team configurations
│   ├── development.md
│   ├── security.md
│   ├── infrastructure.md
│   └── qa.md
├── protocols/                  # Collaboration protocols
│   ├── messages.md             # Message formats
│   ├── escalation.md           # Escalation procedures
│   ├── handoffs.md             # Work handoff procedures
│   └── security-gates.md       # Quality/security gates
├── workflows/                  # Workflow definitions
│   ├── full-sdlc.md            # Full SDLC pipeline
│   ├── security-assessment.md  # Security assessment
│   ├── code-review.md          # Code review pipeline
│   └── incident-response.md    # Incident response
├── orchestration/              # Orchestration logic
│   └── COORDINATOR.md          # Master coordinator
├── config/                     # Configuration files
│   ├── agents.json             # Agent registry
│   ├── routing.json            # Task routing rules
│   └── settings.json           # System settings
└── .claude/
    └── commands/               # Slash commands
        ├── hivemind.md         # Main orchestrator command
        ├── dev.md              # Development team
        ├── sec.md              # Security team
        ├── infra.md            # Infrastructure team
        ├── qa.md               # QA team
        ├── architect.md        # DEV-001
        ├── pentest.md          # SEC-002
        ├── sre.md              # INF-005
        ├── reviewer.md         # DEV-004
        ├── incident.md         # Incident response
        └── sdlc.md             # Full SDLC
```

---

## Usage Examples

### Example 1: Architecture Review
```
/architect Design a microservices architecture for an e-commerce platform
```

### Example 2: Security Assessment
```
/sec Perform a security assessment of our REST API
```

### Example 3: Full Feature Development
```
/sdlc Implement user authentication with OAuth 2.0
```

### Example 4: Incident Response
```
/incident Production database is showing high latency and connection errors
```

### Example 5: Code Review
```
/reviewer Review PR #1234 for security and performance
```

### Example 6: Infrastructure Design
```
/infra Design a Kubernetes deployment for our microservices
```

---

## Configuration

### Agent Registry
See `/config/agents.json` for complete agent metadata.

### Routing Rules
See `/config/routing.json` for task routing configuration.

### System Settings
See `/config/settings.json` for system-wide settings.

---

## Extending HIVEMIND

### Adding New Agents
1. Create agent definition in `/agents/{team}/{agent}.md`
2. Add to team configuration in `/teams/{team}.md`
3. Register in `/config/agents.json`
4. Update routing rules in `/config/routing.json`
5. Optionally create slash command in `/.claude/commands/`

### Adding New Workflows
1. Create workflow definition in `/workflows/{workflow}.md`
2. Define phases, agents, and gates
3. Create slash command if needed
4. Update COORDINATOR with routing

### Modifying Protocols
1. Update protocol file in `/protocols/`
2. Ensure all affected agents are updated
3. Test communication flows

---

## Support

For issues or enhancements:
1. Review relevant agent definitions
2. Check workflow documentation
3. Consult protocol specifications
4. Escalate to COORDINATOR for complex issues

---

*HIVEMIND — Unified Intelligence Through Coordinated Expertise*
