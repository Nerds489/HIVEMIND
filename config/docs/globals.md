# HIVEMIND Global Configuration

## Overview

This document defines global constants, standards, and conventions used across all HIVEMIND agents and workflows.

---

## Priority Levels

| Level | Name | Response SLA | Resolution SLA | Use Case |
|-------|------|--------------|----------------|----------|
| **P0** | Critical | 15 minutes | 4 hours | Production down, active security breach, data loss |
| **P1** | High | 1 hour | 24 hours | Major functionality broken, security vulnerability |
| **P2** | Medium | 4 hours | 72 hours | Significant issue with workaround available |
| **P3** | Low | 24 hours | 1 week | Minor issue, minimal business impact |
| **P4** | Info | Best effort | Best effort | Enhancement requests, documentation |

### Priority Escalation Rules

```yaml
escalation_rules:
  P0:
    - 15 min: Escalate to team lead
    - 30 min: Escalate to cross-team
    - 1 hour: Escalate to COORDINATOR
    - 2 hours: Escalate to human

  P1:
    - 1 hour: Escalate to team lead
    - 4 hours: Escalate to cross-team
    - 8 hours: Escalate to COORDINATOR

  P2:
    - 4 hours: Escalate to team lead
    - 24 hours: Escalate to cross-team

  P3:
    - 24 hours: Escalate to team lead

  P4:
    - No automatic escalation
```

---

## Security Classifications

| Level | Name | Description | Handling Requirements |
|-------|------|-------------|----------------------|
| **L1** | Restricted | Highest sensitivity - active exploits, credentials, PII | Encrypted storage, MFA access, full audit, need-to-know only |
| **L2** | Confidential | Sensitive business data, security findings | Encrypted storage, access logging, limited distribution |
| **L3** | Internal | Company-internal information | Standard access controls, no external sharing |
| **L4** | Public | Non-sensitive, shareable externally | No restrictions |

### Classification Guidelines

```yaml
classification_examples:
  restricted:
    - Active exploit code
    - Production credentials
    - Customer PII
    - Security incident details (during active incident)
    - Penetration test findings (detailed)

  confidential:
    - Architecture documents
    - Security assessment reports
    - Internal APIs documentation
    - Employee information
    - Business metrics

  internal:
    - Development documentation
    - Meeting notes
    - Project plans
    - General policies

  public:
    - Public API documentation
    - Marketing materials
    - Open source code
    - Public announcements
```

---

## Agent Identification

### Agent ID Format

```
[TEAM_PREFIX]-[NUMBER]
```

| Team | Prefix | Range |
|------|--------|-------|
| Development | DEV | 001-006 |
| Security | SEC | 001-006 |
| Infrastructure | INF | 001-006 |
| Quality Assurance | QA | 001-006 |

### Agent Registry

| ID | Name | Team | Role |
|----|------|------|------|
| DEV-001 | Architect | Development | System design and architecture |
| DEV-002 | Backend Developer | Development | Server-side implementation |
| DEV-003 | Frontend Developer | Development | Client-side implementation |
| DEV-004 | Code Reviewer | Development | Code quality assurance |
| DEV-005 | Technical Writer | Development | Documentation |
| DEV-006 | DevOps Liaison | Development | CI/CD and deployment |
| SEC-001 | Security Architect | Security | Security design and strategy |
| SEC-002 | Penetration Tester | Security | Offensive security testing |
| SEC-003 | Malware Analyst | Security | Malware analysis and reverse engineering |
| SEC-004 | Wireless Security Expert | Security | RF and wireless security |
| SEC-005 | Compliance Auditor | Security | Regulatory compliance |
| SEC-006 | Incident Responder | Security | Security incident handling |
| INF-001 | Infrastructure Architect | Infrastructure | Infrastructure design |
| INF-002 | Systems Administrator | Infrastructure | System management |
| INF-003 | Network Engineer | Infrastructure | Network infrastructure |
| INF-004 | Database Administrator | Infrastructure | Database management |
| INF-005 | Site Reliability Engineer | Infrastructure | Reliability and operations |
| INF-006 | Automation Engineer | Infrastructure | Infrastructure automation |
| QA-001 | QA Architect | QA | Test strategy and process |
| QA-002 | Test Automation Engineer | QA | Automated testing |
| QA-003 | Performance Tester | QA | Performance testing |
| QA-004 | Security Tester | QA | Security testing |
| QA-005 | Manual QA Tester | QA | Manual and exploratory testing |
| QA-006 | Test Data Manager | QA | Test data management |

---

## Naming Conventions

### Task IDs
```
TASK-[TEAM]-[YYYYMMDD]-[SEQ]
Example: TASK-DEV-20240115-001
```

### Handoff IDs
```
HO-[SOURCE]-[DEST]-[YYYYMMDD]-[HHMMSS]
Example: HO-DEV002-DEV004-20240115-143000
```

### Artifact IDs
```
ART-[YYYYMMDD]-[SEQ]
Example: ART-20240115-001
```

### Finding IDs
```
FIND-[YEAR]-[ASSESSMENT_SEQ]-[FINDING_SEQ]
Example: FIND-2024-001-007
```

### Incident IDs
```
INC-[YYYYMMDD]-[SEQ]
Example: INC-20240115-001
```

### Change Request IDs
```
CR-[YYYYMMDD]-[SEQ]
Example: CR-20240115-001
```

---

## Time Standards

### Timezone
- All timestamps in **ISO8601 format**
- All times in **UTC** unless explicitly specified
- Format: `YYYY-MM-DDTHH:MM:SSZ`

### Business Hours
- Standard: Monday-Friday, 09:00-18:00 UTC
- On-call: 24/7

### Deadline Interpretation
- Unless specified, deadlines are **end of business day**
- "By Friday" = Friday 18:00 UTC
- Explicit times override defaults

### SLA Clock
- SLA clock starts on **acknowledgment**, not receipt
- Acknowledgment required within **15 minutes** of receipt (P0/P1) or **1 hour** (P2+)

---

## Output Quality Standards

### Code Standards
- Must pass all linting rules
- Must have tests (coverage ≥80%)
- Must include documentation (docstrings, comments)
- Must follow language-specific conventions
- No hardcoded secrets or credentials
- No debug code or console.log statements

### Documentation Standards
- Clear, concise language
- Proper formatting (headers, lists, tables)
- No spelling/grammar errors
- Complete (no TODO or TBD placeholders)
- Up-to-date with current state

### Report Standards
- Executive summary first
- Findings sorted by severity
- Actionable recommendations
- Evidence included or referenced
- Use standard templates

### Deliverable Completeness
- All outputs must be complete
- No placeholders in final deliverables
- All references must be valid
- All dependencies documented

---

## Communication Standards

### Message Response Times

| Message Type | Priority | Max Response Time |
|--------------|----------|-------------------|
| REQUEST | P0 | 15 minutes |
| REQUEST | P1 | 1 hour |
| REQUEST | P2+ | 4 hours |
| ALERT | Critical | Immediate |
| ALERT | High | 15 minutes |
| ALERT | Medium | 1 hour |
| QUERY | Any | 1 hour |
| STATUS | Any | Best effort |

### Acknowledgment Protocol
1. Acknowledge receipt within SLA
2. Provide estimated completion time
3. Update on progress at defined intervals
4. Notify on completion or blocker

---

## Artifact Paths

### Standard Directory Structure
```
/artifacts/
├── [team]/
│   └── [date YYYY-MM-DD]/
│       └── [task_id]/
│           ├── code/
│           ├── docs/
│           ├── reports/
│           └── evidence/
```

### Example Paths
```
/artifacts/development/2024-01-15/TASK-DEV-20240115-001/code/
/artifacts/security/2024-01-15/TASK-SEC-20240115-001/reports/
/artifacts/qa/2024-01-15/TASK-QA-20240115-001/evidence/
```

---

## Severity Definitions

### Bug Severity

| Severity | Criteria | Response |
|----------|----------|----------|
| Critical | System unusable, data loss, security breach | P0 - Immediate |
| High | Major feature broken, significant impact | P1 - Same day |
| Medium | Feature impaired, workaround available | P2 - 3 days |
| Low | Minor issue, cosmetic | P3 - Next sprint |

### Security Finding Severity

| Severity | CVSS Range | Examples |
|----------|------------|----------|
| Critical | 9.0-10.0 | RCE, Auth bypass, SQLi with data access |
| High | 7.0-8.9 | Privilege escalation, significant data exposure |
| Medium | 4.0-6.9 | XSS, CSRF, information disclosure |
| Low | 0.1-3.9 | Minor info leak, missing headers |
| Info | 0.0 | Best practices, hardening recommendations |

---

## Gate Requirements

### Code Merge Gate
- ✓ Build passes
- ✓ All tests pass
- ✓ Coverage ≥80%
- ✓ Linting clean
- ✓ SAST scan clean (no critical/high)
- ✓ Dependency scan clean (no critical/high)
- ✓ Secrets scan clean
- ✓ Code review approved

### Production Deployment Gate
- ✓ Code Merge Gate passed
- ✓ All environments tested
- ✓ Performance baselines met
- ✓ Security review approved
- ✓ Change request approved
- ✓ Rollback plan documented
- ✓ On-call team notified

---

## Version Numbers

### Semantic Versioning
```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible new features
- **PATCH**: Backward-compatible bug fixes

### Pre-release Tags
```
1.0.0-alpha.1
1.0.0-beta.2
1.0.0-rc.1
```

---

## Retention Policies

| Data Type | Retention Period | Archive | Delete |
|-----------|------------------|---------|--------|
| Audit logs | 7 years | After 1 year | After 7 years |
| Security findings | 3 years | After 1 year | After 3 years |
| Incident reports | 7 years | After 1 year | Never |
| Code reviews | 2 years | After 6 months | After 2 years |
| Test results | 1 year | After 3 months | After 1 year |
| Build artifacts | 90 days | N/A | After 90 days |
