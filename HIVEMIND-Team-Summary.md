# HIVEMIND

**24 Agents | 4 Teams | 1 Collective Intelligence**

```
                              HIVEMIND
                                 |
         ---------------------------------------------
         |            |              |               |
    DEVELOPMENT   SECURITY      INFRASTRUCTURE      QA
      6 agents    6 agents        6 agents       6 agents
```

---

## DEVELOPMENT & ARCHITECTURE

**Leader:** Architect
**Mission:** Transforms requirements into working software.

| Agent | Role |
|-------|------|
| Architect | System design, technical blueprints |
| Backend Developer | APIs, databases, server logic |
| Frontend Developer | UI/UX, client-side code |
| Code Reviewer | Quality gates, code standards |
| Technical Writer | Documentation, guides |
| DevOps Liaison | CI/CD, deployments |

---

## SECURITY & OFFENSIVE OPERATIONS

**Leader:** Security Architect
**Mission:** Thinks like attackers, defends like pros.

| Agent | Role |
|-------|------|
| Security Architect | Defense strategy, threat modeling |
| Penetration Tester | Ethical hacking, exploits |
| Malware Analyst | Reverse engineering, IOCs |
| Wireless Security Expert | WiFi/RF security |
| Compliance Auditor | NIST, SOC2, GDPR, PCI |
| Incident Responder | Forensics, crisis management |

---

## INFRASTRUCTURE & OPERATIONS

**Leader:** Infrastructure Architect
**Mission:** Keeps the lights on, automates everything.

| Agent | Role |
|-------|------|
| Infrastructure Architect | Cloud design, capacity planning |
| Systems Administrator | Server hardening, patching |
| Network Engineer | Firewalls, routing, DNS |
| Database Administrator | Data storage, query optimization |
| Site Reliability Engineer | Monitoring, SLOs, on-call |
| Automation Engineer | Terraform, Ansible, scripting |

---

## QUALITY ASSURANCE & VALIDATION

**Leader:** QA Architect
**Mission:** Catches problems before users do.

| Agent | Role |
|-------|------|
| QA Architect | Test strategy, coverage |
| Test Automation Engineer | Selenium, Playwright, pytest |
| Performance Tester | Load testing, bottlenecks |
| Security Tester | SAST, DAST, DevSecOps |
| Manual QA Tester | Exploratory testing, edge cases |
| Test Data Manager | Test data, environments |

---

## Usage

```
# Summon the collective
Task -> subagent_type: "hivemind"

# Individual agents
Task -> subagent_type: "architect"
Task -> subagent_type: "penetration-tester"
Task -> subagent_type: "database-administrator"
```
