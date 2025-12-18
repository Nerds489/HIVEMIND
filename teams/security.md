# Security & Offensive Operations Team

## Team Overview

**Mission:** Think like attackers, defend like pros. Identify vulnerabilities, validate defenses, and ensure systems can withstand real-world threats.

**Leader:** Security Architect

**Size:** 6 Agents

## Internal Registry (IDs)

This mapping is for internal routing/documentation only. Never include these IDs in user-visible output.

| Internal ID | Role | Specialty |
|-------------|------|-----------|
| SEC-001 | Security Architect | Threat modeling, strategy |
| SEC-002 | Penetration Tester | Offensive security |
| SEC-003 | Malware Analyst | Threat intelligence |
| SEC-004 | Wireless Security Expert | RF, IoT security |
| SEC-005 | Compliance Auditor | Regulatory compliance |
| SEC-006 | Incident Responder | Incident management |

## Provides (Summary)

- Threat models
- Security requirements
- Vulnerability assessments
- Compliance guidance
- Incident response

## Interfaces (Summary)

- Development: security reviews, requirements
- Infrastructure: hardening, access controls
- QA: security test cases

## Team Structure

```
                    ┌─────────────────────┐
                    │ SECURITY ARCHITECT  │
                    │   (Team Leader)     │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  Penetration  │     │    Malware    │     │   Wireless    │
│    Tester     │     │    Analyst    │     │   Security    │
└───────────────┘     └───────────────┘     └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                                 │
              ▼                                 ▼
     ┌───────────────┐                ┌───────────────┐
     │  Compliance   │                │   Incident    │
     │    Auditor    │                │   Responder   │
     └───────────────┘                └───────────────┘
```

## Agent Roster

| Agent | Role | Primary Responsibility |
|-------|------|------------------------|
| **Security Architect** | Team Leader | Defense strategy, threat modeling, security design |
| **Penetration Tester** | Offensive Security | Ethical hacking, vulnerability discovery, exploits |
| **Malware Analyst** | Threat Intelligence | Reverse engineering, IOCs, threat analysis |
| **Wireless Security Expert** | RF Specialist | WiFi/Bluetooth security, RF monitoring |
| **Compliance Auditor** | Standards | NIST, SOC2, GDPR, PCI compliance |
| **Incident Responder** | Crisis Management | Forensics, containment, recovery |

## Team Capabilities

### Defensive Security
- Security architecture design
- Threat modeling (STRIDE, PASTA)
- Security requirements definition
- Control implementation guidance
- Security review and approval

### Offensive Security
- Penetration testing
- Vulnerability assessment
- Red team exercises
- Social engineering tests
- Wireless security testing

### Threat Intelligence
- Malware analysis
- IOC extraction
- Threat hunting
- Detection rule creation
- Attack pattern analysis

### Compliance & Governance
- Framework compliance (NIST, ISO, SOC2)
- Audit support
- Policy development
- Risk assessment
- Evidence collection

### Incident Response
- Security incident handling
- Digital forensics
- Containment procedures
- Recovery operations
- Post-incident analysis

## Interaction Patterns

### Security Assessment Flow
```
Security Request
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ SECURITY ARCHITECT                                            │
│ • Defines security requirements                               │
│ • Creates threat models                                       │
│ • Assigns security tasks                                      │
└─────────────────────────┬────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ PENETRATION    │ │ WIRELESS       │ │ COMPLIANCE     │
│ TESTER         │ │ SECURITY       │ │ AUDITOR        │
│ • Tests systems│ │ • Tests RF     │ │ • Audits       │
│ • Finds vulns  │ │ • Scans WiFi   │ │ • Documents    │
└───────┬────────┘ └───────┬────────┘ └───────┬────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │ MALWARE ANALYST        │
              │ • Analyzes threats     │
              │ • Creates IOCs         │
              │ • Detection rules      │
              └───────────┬────────────┘
                          │
                          ▼ (If incident)
              ┌────────────────────────┐
              │ INCIDENT RESPONDER     │
              │ • Manages incidents    │
              │ • Forensics            │
              │ • Recovery             │
              └────────────────────────┘
```

### Cross-Team Interactions

| External Team | Key Interactions |
|---------------|------------------|
| **Development** | Secure design review, vulnerability remediation |
| **Infrastructure** | Network security, infrastructure hardening |
| **QA** | Security testing automation, DevSecOps |

## Communication Protocols

### Security Alert
```
ALERT: Security Issue Detected
SEVERITY: [Critical/High/Medium/Low]
TYPE: [Vulnerability/Incident/Compliance Gap]
AFFECTED: [Systems/Applications]
DETAILS: [Description]
RECOMMENDED_ACTION: [What to do]
DEADLINE: [When to act]
```

### Penetration Test Report Handoff
```
REPORT: Penetration Test Complete
TARGET: [System/Application]
DURATION: [Test period]
FINDINGS:
  - Critical: [count]
  - High: [count]
  - Medium: [count]
  - Low: [count]
REPORT_LOCATION: [Link]
REMEDIATION_PRIORITY: [Top 3 items]
```

### Incident Declaration
```
INCIDENT DECLARED
ID: INC-[YYYY]-[NNN]
SEVERITY: [P1/P2/P3/P4]
TYPE: [Malware/Intrusion/Data Breach/etc.]
STATUS: [Investigating/Containing/Eradicating/Recovering]
COMMANDER: Incident Responder
AFFECTED: [Systems/Users]
NEXT_UPDATE: [Time]
```

## Security Gates

### Design Review Gate
- [ ] Threat model complete
- [ ] Security requirements defined
- [ ] Authentication design approved
- [ ] Authorization design approved
- [ ] Data protection verified
- [ ] Logging requirements met

### Pre-Production Gate
- [ ] Penetration test passed
- [ ] Vulnerability scan clean
- [ ] Dependency scan clean
- [ ] Security configuration reviewed
- [ ] Compliance requirements met
- [ ] Incident response plan ready

## Escalation Path

```
Security Event
      │
      ▼
Initial Assessment
      │
      ├── False Positive ──► Document & Close
      │
      ▼ (Confirmed Issue)
Security Architect Notified
      │
      ├── Low Severity ──► Standard Remediation
      │
      ▼ (High Severity)
Incident Response Activated
      │
      ├── Contained ──► Recovery & PIR
      │
      ▼ (Major Incident)
Executive Notification
```

## Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Mean Time to Detect (MTTD) | < 1 hour | Time from attack to detection |
| Mean Time to Respond (MTTR) | < 4 hours | Time from detection to containment |
| Vulnerability Remediation | 30 days (Critical: 7 days) | Time to fix |
| Pentest Coverage | 100% | Critical systems tested annually |
| Compliance Score | > 95% | Controls passing / Total |

## Invocation

```bash
# Summon the Security Team
Task -> subagent_type: "security-team"

# Individual agents
Task -> subagent_type: "security-architect"
Task -> subagent_type: "penetration-tester"
Task -> subagent_type: "malware-analyst"
Task -> subagent_type: "wireless-security-expert"
Task -> subagent_type: "compliance-auditor"
Task -> subagent_type: "incident-responder"
```
