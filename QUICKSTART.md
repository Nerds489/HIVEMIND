# HIVEMIND Quick Start Guide

Start here:
- `BOOTSTRAP.md` (single entry point + load sequence)
- `CLAUDE.md` (canonical operating rules)

## 30-Second Start

```bash
# Navigate to HIVEMIND directory
cd /path/to/HIVEMIND

# Claude Code will auto-load CLAUDE.md and become HIVEMIND
```

## Basic Invocation Patterns

### Single Agent Tasks

```
"Design a REST API for user management"
→ Routes to DEV-001 (Architect)

"Review this pull request for security issues"
→ Routes to DEV-004 (Code Reviewer) + QA-004 (Security Tester)

"Run a penetration test on the login endpoint"
→ Routes to SEC-002 (Penetration Tester)

"Set up monitoring for the new microservice"
→ Routes to INF-005 (Site Reliability Engineer)

"Create automated tests for the checkout flow"
→ Routes to QA-002 (Test Automation Engineer)
```

### Team Tasks

```
"I need the development team to build a new feature"
→ Activates Development Team coordination

"Security team, assess our cloud infrastructure"
→ Activates Security Team coordination

"Infrastructure team, prepare for production deployment"
→ Activates Infrastructure Team coordination

"QA team, run full regression testing"
→ Activates QA Team coordination
```

### Workflow Tasks

```
"Full SDLC for implementing OAuth authentication"
→ Activates full-sdlc.md workflow

"Security assessment of the payment API"
→ Activates security-assessment.md workflow

"We have a production incident - database is down"
→ Activates incident-response.md workflow

"Code review pipeline for PR #1234"
→ Activates code-review.md workflow

"Deploy version 2.0 to production"
→ Activates infrastructure-deploy.md workflow

"Compliance audit for SOC2 certification"
→ Activates compliance-audit.md workflow
```

---

## Agent Quick Reference

| ID | Agent | Keywords |
|----|-------|----------|
| **Development Team** |||
| DEV-001 | Architect | design, architecture, system, blueprint |
| DEV-002 | Backend Developer | api, backend, server, database, python, node |
| DEV-003 | Frontend Developer | ui, frontend, react, vue, css, component |
| DEV-004 | Code Reviewer | review, pr, quality, standards |
| DEV-005 | Technical Writer | docs, documentation, readme, guide |
| DEV-006 | DevOps Liaison | ci/cd, pipeline, deploy, build |
| **Security Team** |||
| SEC-001 | Security Architect | threat model, security design, defense |
| SEC-002 | Penetration Tester | pentest, hack, exploit, vulnerability |
| SEC-003 | Malware Analyst | malware, reverse engineer, binary |
| SEC-004 | Wireless Security | wifi, bluetooth, wireless, rf |
| SEC-005 | Compliance Auditor | compliance, audit, gdpr, soc2, pci |
| SEC-006 | Incident Responder | incident, breach, forensics, emergency |
| **Infrastructure Team** |||
| INF-001 | Infrastructure Architect | cloud, aws, azure, infrastructure |
| INF-002 | Systems Administrator | linux, server, sysadmin, configuration |
| INF-003 | Network Engineer | network, firewall, dns, routing |
| INF-004 | Database Administrator | database, sql, optimization, backup |
| INF-005 | Site Reliability Engineer | sre, monitoring, slo, reliability |
| INF-006 | Automation Engineer | terraform, ansible, automation, iac |
| **QA Team** |||
| QA-001 | QA Architect | test strategy, quality, coverage |
| QA-002 | Test Automation Engineer | selenium, playwright, automated test |
| QA-003 | Performance Tester | load test, performance, benchmark |
| QA-004 | Security Tester | sast, dast, security scan |
| QA-005 | Manual QA Tester | exploratory, manual test, uat |
| QA-006 | Test Data Manager | test data, fixtures, environment |

---

## Common Scenarios

### Scenario 1: New Feature Development
```
User: "Build a user notification system with email and push notifications"

HIVEMIND response:
1. Routes to DEV-001 (Architect) for system design
2. Hands off to DEV-002 (Backend) for API implementation
3. Parallel: DEV-003 (Frontend) for UI components
4. DEV-004 (Code Reviewer) reviews all code
5. QA-002 (Test Automation) creates tests
6. SEC-002 (Penetration Tester) validates security
7. DEV-006 (DevOps) deploys to staging
8. QA-005 (Manual QA) performs UAT
9. INF-005 (SRE) deploys to production
```

### Scenario 2: Security Incident
```
User: "We detected suspicious activity - possible data breach"

HIVEMIND response:
1. IMMEDIATELY routes to SEC-006 (Incident Responder)
2. Parallel activation: INF-005 (SRE) for system isolation
3. SEC-003 (Malware Analyst) examines suspicious files
4. SEC-002 (Penetration Tester) identifies attack vector
5. INF-002 (SysAdmin) implements containment
6. SEC-005 (Compliance) assesses regulatory impact
7. Full incident report generated
```

### Scenario 3: Production Deployment
```
User: "Deploy v3.0 to production this weekend"

HIVEMIND response:
1. QA-001 (QA Architect) verifies all tests pass
2. SEC-001 (Security Architect) approves security posture
3. INF-001 (Infrastructure Architect) reviews deployment plan
4. INF-005 (SRE) prepares monitoring
5. DEV-006 (DevOps) executes deployment
6. INF-002 (SysAdmin) validates system health
7. QA-005 (Manual QA) performs smoke tests
```

---

## Output Formats

All HIVEMIND outputs follow standards:

| Output Type | Format | Template |
|-------------|--------|----------|
| Security Report | Markdown | `/templates/security-report.md` |
| Architecture Decision | Markdown | `/templates/architecture-decision-record.md` |
| Incident Report | Markdown | `/templates/incident-report.md` |
| Code Review | Markdown | `/templates/code-review-findings.md` |
| Test Results | Markdown | `/templates/test-results.md` |
| Deployment Checklist | Markdown | `/templates/deployment-checklist.md` |

---

## Escalation Levels

| Level | Scope | Timeout |
|-------|-------|---------|
| 1 | Peer consultation | 5 min |
| 2 | Team lead escalation | 15 min |
| 3 | Cross-team coordination | 30 min |
| 4 | COORDINATOR intervention | 1 hour |
| 5 | Human escalation | As needed |

---

## Priority Levels

| Priority | SLA | Use Case |
|----------|-----|----------|
| P0 | 15 min | Production down, active breach |
| P1 | 1 hour | Major functionality broken |
| P2 | 4 hours | Significant issue, workaround exists |
| P3 | 24 hours | Minor issue |
| P4 | Best effort | Enhancement, documentation |

---

## Tips for Best Results

1. **Be specific** - "Review auth code for SQL injection" > "Review code"
2. **Mention urgency** - Include priority if time-sensitive
3. **Provide context** - Reference files, PRs, or systems involved
4. **Name the workflow** - "Run full SDLC" triggers the complete pipeline
5. **Multi-agent tasks** - HIVEMIND auto-coordinates, just describe the goal

---

## File Locations

```
HIVEMIND/
├── CLAUDE.md           ← Auto-loaded by Claude Code
├── HIVEMIND.md         ← Full system documentation
├── QUICKSTART.md       ← This file
├── agents/             ← 24 agent definitions
├── orchestration/      ← Coordinator and routing
├── protocols/          ← Communication rules
├── workflows/          ← Multi-agent pipelines
├── teams/              ← Team configurations
├── templates/          ← Output templates
└── config/             ← System settings
```

---

*HIVEMIND - Route intelligently. Execute completely.*
