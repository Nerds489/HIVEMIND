# Architecture Decision Record

---

## ADR-[NUMBER]: [TITLE]

**Date:** [YYYY-MM-DD]

**Status:** [PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED]

**Superseded by:** [ADR-XXX] *(if applicable)*

**Supersedes:** [ADR-XXX] *(if applicable)*

---

## Decision Makers

| Role | Agent/Person | Team |
|------|--------------|------|
| Author | [AGENT_ID] | [TEAM] |
| Reviewer | [AGENT_ID] | [TEAM] |
| Approver | [AGENT_ID] | [TEAM] |

---

## Context

### Problem Statement

[What is the issue that we're seeing that motivates this decision or change? What is the context in which this decision is being made?]

### Background

[Relevant technical or business background. Include links to related documents, tickets, or prior decisions.]

### Constraints

- [CONSTRAINT_1]
- [CONSTRAINT_2]
- [CONSTRAINT_3]

### Requirements

| Requirement | Priority | Source |
|-------------|----------|--------|
| [REQ_1] | Must Have | [SOURCE] |
| [REQ_2] | Should Have | [SOURCE] |
| [REQ_3] | Nice to Have | [SOURCE] |

---

## Decision

### Summary

[One paragraph clearly stating the decision that was made.]

### Details

[Detailed explanation of the decision, including technical specifics.]

```
[Diagram, code example, or configuration if applicable]
```

---

## Alternatives Considered

### Option A: [OPTION_NAME] *(Selected)*

**Description:** [Brief description]

**Pros:**
- [PRO_1]
- [PRO_2]

**Cons:**
- [CON_1]
- [CON_2]

**Effort:** [LOW | MEDIUM | HIGH]

**Risk:** [LOW | MEDIUM | HIGH]

---

### Option B: [OPTION_NAME]

**Description:** [Brief description]

**Pros:**
- [PRO_1]
- [PRO_2]

**Cons:**
- [CON_1]
- [CON_2]

**Effort:** [LOW | MEDIUM | HIGH]

**Risk:** [LOW | MEDIUM | HIGH]

**Rejection Reason:** [Why this option was not selected]

---

### Option C: [OPTION_NAME]

**Description:** [Brief description]

**Pros:**
- [PRO_1]
- [PRO_2]

**Cons:**
- [CON_1]
- [CON_2]

**Effort:** [LOW | MEDIUM | HIGH]

**Risk:** [LOW | MEDIUM | HIGH]

**Rejection Reason:** [Why this option was not selected]

---

## Consequences

### Positive

- [POSITIVE_1]
- [POSITIVE_2]
- [POSITIVE_3]

### Negative

- [NEGATIVE_1]
- [NEGATIVE_2]

### Neutral

- [NEUTRAL_1]

---

## Impact Analysis

### Affected Components

| Component | Impact Type | Description |
|-----------|-------------|-------------|
| [COMPONENT] | [New | Modified | Deprecated] | [DESCRIPTION] |

### Affected Teams/Agents

| Team/Agent | Impact | Action Required |
|------------|--------|-----------------|
| [TEAM/AGENT] | [HIGH | MEDIUM | LOW] | [ACTION] |

### Migration Requirements

[If this decision requires migration or transition, describe the approach]

1. [STEP_1]
2. [STEP_2]
3. [STEP_3]

---

## Security Implications

| Consideration | Impact | Mitigation |
|---------------|--------|------------|
| [CONSIDERATION_1] | [IMPACT] | [MITIGATION] |
| [CONSIDERATION_2] | [IMPACT] | [MITIGATION] |

**Security Review Required:** [YES | NO]

**Security Reviewer:** [AGENT_ID] *(if applicable)*

---

## Performance Implications

| Metric | Expected Impact | Acceptable? |
|--------|-----------------|-------------|
| [METRIC_1] | [IMPACT] | [YES | NO | NEEDS_TESTING] |
| [METRIC_2] | [IMPACT] | [YES | NO | NEEDS_TESTING] |

---

## Cost Implications

| Cost Type | Estimate | Recurring? |
|-----------|----------|------------|
| Development | [ESTIMATE] | No |
| Infrastructure | [ESTIMATE] | [YES | NO] |
| Licensing | [ESTIMATE] | [YES | NO] |
| Maintenance | [ESTIMATE] | Yes |

---

## Compliance Considerations

| Framework | Relevant? | Notes |
|-----------|-----------|-------|
| GDPR | [YES | NO | N/A] | [NOTES] |
| SOC2 | [YES | NO | N/A] | [NOTES] |
| PCI-DSS | [YES | NO | N/A] | [NOTES] |
| HIPAA | [YES | NO | N/A] | [NOTES] |

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [RISK_1] | [HIGH | MEDIUM | LOW] | [HIGH | MEDIUM | LOW] | [MITIGATION] |
| [RISK_2] | [HIGH | MEDIUM | LOW] | [HIGH | MEDIUM | LOW] | [MITIGATION] |

---

## Implementation Plan

### Phase 1: [PHASE_NAME]
**Duration:** [ESTIMATE]
**Owner:** [AGENT_ID]
- [ ] [TASK_1]
- [ ] [TASK_2]

### Phase 2: [PHASE_NAME]
**Duration:** [ESTIMATE]
**Owner:** [AGENT_ID]
- [ ] [TASK_1]
- [ ] [TASK_2]

### Rollback Plan

[Describe how to revert this decision if needed]

1. [STEP_1]
2. [STEP_2]

---

## Validation

### Success Criteria

- [ ] [CRITERION_1]
- [ ] [CRITERION_2]
- [ ] [CRITERION_3]

### Metrics to Monitor

| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| [METRIC] | [BASELINE] | [TARGET] | [METHOD] |

---

## Related Documents

- [DOCUMENT_1](link)
- [DOCUMENT_2](link)
- [Related ADR-XXX](link)

---

## Review History

| Date | Reviewer | Outcome | Notes |
|------|----------|---------|-------|
| [DATE] | [AGENT_ID] | [APPROVED | CHANGES REQUESTED | REJECTED] | [NOTES] |

---

## Approval

| Role | Agent | Date | Signature |
|------|-------|------|-----------|
| Technical Approval | [AGENT_ID] | [DATE] | ☑ |
| Security Approval | [AGENT_ID] | [DATE] | ☑ |
| Business Approval | [AGENT_ID] | [DATE] | ☑ |

---

*ADR generated by HIVEMIND Development Team*
