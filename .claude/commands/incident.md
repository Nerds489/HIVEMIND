# Incident Response Command

Activates the **Incident Response Workflow** with SEC-006 (Incident Responder) as primary and INF-005 (SRE) as support.

## Immediate Actions

When invoked, this command:
1. Activates incident response mode
2. Loads SEC-006 and INF-005 agents
3. Initiates incident documentation
4. Begins triage and assessment

## Incident Severity Classification

| Level | Criteria | Response |
|-------|----------|----------|
| **SEV1** | Complete outage, active breach, data loss | All hands, immediate |
| **SEV2** | Major degradation, exploited vulnerability | Incident team, < 15 min |
| **SEV3** | Partial issue, confirmed security issue | On-call, < 1 hour |
| **SEV4** | Minor issue, low impact | Next business day |

## Response Phases

```
DETECT → TRIAGE → CONTAIN → INVESTIGATE → ERADICATE → RECOVER
```

1. **Detect:** Identify and confirm the incident
2. **Triage:** Assess severity and impact
3. **Contain:** Stop the spread, isolate affected systems
4. **Investigate:** Determine root cause
5. **Eradicate:** Remove the threat
6. **Recover:** Restore services, verify remediation

## Agents Involved

- **SEC-006** (Lead): Incident handling, forensics
- **INF-005** (Support): System recovery, monitoring
- **SEC-002** (Consult): Vulnerability analysis
- **INF-002** (Consult): System restoration

## Documentation Requirements

Every incident must document:
- Timeline of events
- Affected systems
- Actions taken
- Root cause analysis
- Lessons learned

## Load Full Workflow

For complete workflow details:
`/workflows/incident-response.md`

---

**Incident Description:** $ARGUMENTS
