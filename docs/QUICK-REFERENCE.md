# HIVEMIND Quick Reference Card

```
██╗  ██╗██╗██╗   ██╗███████╗███╗   ███╗██╗███╗   ██╗██████╗
██║  ██║██║██║   ██║██╔════╝████╗ ████║██║████╗  ██║██╔══██╗
███████║██║██║   ██║█████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║
██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║
██║  ██║██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝
          24 Agents • 4 Teams • 1 Unified Intelligence
```

---

## Activation

| Command | Effect |
|---------|--------|
| Say "HIVEMIND" | Activates multi-agent system |
| "stop HIVEMIND" | Deactivates, returns to normal |

---

## Slash Commands

### System Commands
| Command | Purpose |
|---------|---------|
| `/hivemind [task]` | Full system for any task |
| `/status` | Show system status |
| `/recall [query]` | Search memory |
| `/debug [component]` | Troubleshoot issues |

### Team Commands
| Command | Team |
|---------|------|
| `/dev [task]` | Development (6 agents) |
| `/sec [task]` | Security (6 agents) |
| `/infra [task]` | Infrastructure (6 agents) |
| `/qa [task]` | Quality Assurance (6 agents) |

### Agent Commands
| Command | Agent |
|---------|-------|
| `/architect` | DEV-001 System Architect |
| `/reviewer` | DEV-004 Code Reviewer |
| `/pentest` | SEC-002 Penetration Tester |
| `/sre` | INF-005 Site Reliability Engineer |

### Workflow Commands
| Command | Workflow |
|---------|----------|
| `/sdlc [project]` | Full development lifecycle |
| `/incident [desc]` | Incident response protocol |

---

## Teams & Agents

### Development Team (DEV)
| ID | Role | Expertise |
|----|------|-----------|
| DEV-001 | Architect | System design, patterns |
| DEV-002 | Backend | APIs, databases, Python |
| DEV-003 | Frontend | React, TypeScript, CSS |
| DEV-004 | Reviewer | Code quality, PR reviews |
| DEV-005 | Writer | Documentation, guides |
| DEV-006 | DevOps | CI/CD, Docker, K8s |

### Security Team (SEC)
| ID | Role | Expertise |
|----|------|-----------|
| SEC-001 | Architect | Security architecture |
| SEC-002 | Pentester | Vulnerability testing |
| SEC-003 | Malware | Reverse engineering |
| SEC-004 | Wireless | WiFi/RF security |
| SEC-005 | Compliance | SOC2, ISO, GDPR |
| SEC-006 | Incident | IR, forensics |

### Infrastructure Team (INF)
| ID | Role | Expertise |
|----|------|-----------|
| INF-001 | Architect | Cloud, infrastructure |
| INF-002 | SysAdmin | Linux, Windows servers |
| INF-003 | Network | Routing, firewalls |
| INF-004 | DBA | PostgreSQL, MySQL |
| INF-005 | SRE | Reliability, monitoring |
| INF-006 | Automation | Terraform, Ansible |

### QA Team (QA)
| ID | Role | Expertise |
|----|------|-----------|
| QA-001 | Architect | Test strategy |
| QA-002 | Automation | Playwright, pytest |
| QA-003 | Performance | k6, load testing |
| QA-004 | Security | SAST, DAST, scanning |
| QA-005 | Manual | Exploratory, UAT |
| QA-006 | Data | Test data, masking |

---

## Memory Commands

```
"Remember that we use TypeScript"       → Creates factual memory
"The fix for the auth bug was..."       → Creates procedural memory
"We chose PostgreSQL because..."        → Creates semantic memory
```

---

## File Locations

```
HIVEMIND/
├── hivemind              # Main CLI
├── CLAUDE.md             # Auto-loaded prompt
├── config/
│   ├── agents.json       # Agent registry
│   ├── routing.json      # Task routing
│   └── settings.json     # System settings
├── memory/
│   ├── global/           # Shared memory
│   ├── teams/            # Team knowledge
│   └── agents/           # Per-agent memory
└── .claude/commands/     # Slash commands
```

---

## Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| "HIVEMIND not responding" | Say "HIVEMIND" to activate |
| Engine not detected | Run `./health-check.sh` |
| Memory not persisting | Check memory/ permissions |
| Wrong agent routing | Update config/routing.json |

---

## Tips

1. **Be specific** - "Design a REST API for user auth" routes better than "help with API"
2. **Use team commands** - `/sec` for security tasks, `/dev` for coding
3. **Check status** - `/status` shows active agents and system health
4. **Query memory** - `/recall` finds previous decisions and learnings

---

*HIVEMIND v1.0.0 | 24 Agents | 4 Teams | Unified Intelligence*
