# Change Request

---

## Change Information

| Field | Value |
|-------|-------|
| **Change ID** | [CR-YYYYMMDD-XXX] |
| **Title** | [CHANGE_TITLE] |
| **Requestor** | [AGENT_ID / NAME] |
| **Date Submitted** | [DATE] |
| **Target Date** | [DATE] |
| **Status** | [Draft / Submitted / Approved / Rejected / Completed] |

---

## Change Classification

| Category | Selection |
|----------|-----------|
| **Change Type** | ☐ Standard ☐ Normal ☐ Emergency |
| **Risk Level** | ☐ Low ☐ Medium ☐ High ☐ Critical |
| **Impact Scope** | ☐ Single System ☐ Multiple Systems ☐ Organization-wide |
| **Environment** | ☐ Development ☐ Staging ☐ Production |

---

## Change Description

### Summary
[One paragraph summary of the change]

### Detailed Description
[Comprehensive description of what will be changed, including technical details]

### Business Justification
[Why is this change needed? What business value does it provide?]

### Related Items
| Item Type | Reference |
|-----------|-----------|
| Ticket/Issue | [TICKET_ID] |
| Project | [PROJECT_NAME] |
| Previous Changes | [CR-XXX] |
| Related Systems | [SYSTEM_NAMES] |

---

## Impact Assessment

### Systems Affected

| System | Impact Type | Description |
|--------|-------------|-------------|
| [SYSTEM_1] | [Direct / Indirect] | [DESCRIPTION] |
| [SYSTEM_2] | [Direct / Indirect] | [DESCRIPTION] |

### User Impact

| User Group | Impact | Description |
|------------|--------|-------------|
| [GROUP_1] | [High / Medium / Low / None] | [DESCRIPTION] |
| [GROUP_2] | [High / Medium / Low / None] | [DESCRIPTION] |

### Service Impact

| Metric | Expected Impact |
|--------|-----------------|
| Availability | [IMPACT_DESCRIPTION] |
| Performance | [IMPACT_DESCRIPTION] |
| Security | [IMPACT_DESCRIPTION] |

### Downtime Required
| Item | Value |
|------|-------|
| Downtime Required | ☐ Yes ☐ No |
| Duration | [DURATION] |
| Maintenance Window | [WINDOW] |

---

## Risk Assessment

### Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [RISK_1] | [High/Med/Low] | [High/Med/Low] | [MITIGATION] |
| [RISK_2] | [High/Med/Low] | [High/Med/Low] | [MITIGATION] |
| [RISK_3] | [High/Med/Low] | [High/Med/Low] | [MITIGATION] |

### Risk Score
| Factor | Score (1-5) |
|--------|-------------|
| Technical Complexity | [X] |
| User Impact | [X] |
| Reversibility | [X] |
| Testing Coverage | [X] |
| **Total Risk Score** | **[X/20]** |

---

## Implementation Plan

### Pre-Implementation Steps

| Step | Description | Owner | Est. Duration |
|------|-------------|-------|---------------|
| 1 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |
| 2 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |

### Implementation Steps

| Step | Description | Owner | Est. Duration |
|------|-------------|-------|---------------|
| 1 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |
| 2 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |
| 3 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |

### Post-Implementation Steps

| Step | Description | Owner | Est. Duration |
|------|-------------|-------|---------------|
| 1 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |
| 2 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |

### Total Implementation Time
| Phase | Duration |
|-------|----------|
| Pre-Implementation | [DURATION] |
| Implementation | [DURATION] |
| Post-Implementation | [DURATION] |
| **Total** | **[DURATION]** |

---

## Rollback Plan

### Rollback Triggers
Rollback will be initiated if:
- [ ] [TRIGGER_CONDITION_1]
- [ ] [TRIGGER_CONDITION_2]
- [ ] [TRIGGER_CONDITION_3]

### Rollback Steps

| Step | Description | Owner | Est. Duration |
|------|-------------|-------|---------------|
| 1 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |
| 2 | [STEP_DESCRIPTION] | [AGENT_ID] | [DURATION] |

### Rollback Time Estimate
| Item | Value |
|------|-------|
| Estimated Rollback Time | [DURATION] |
| Maximum Acceptable Rollback Time | [DURATION] |

---

## Testing Plan

### Pre-Implementation Testing

| Test Type | Description | Status |
|-----------|-------------|--------|
| [TEST_1] | [DESCRIPTION] | ☐ Pass ☐ Fail ☐ Pending |
| [TEST_2] | [DESCRIPTION] | ☐ Pass ☐ Fail ☐ Pending |

### Post-Implementation Testing

| Test Type | Description | Status |
|-----------|-------------|--------|
| Smoke Test | [DESCRIPTION] | ☐ Pass ☐ Fail ☐ Pending |
| Functional Test | [DESCRIPTION] | ☐ Pass ☐ Fail ☐ Pending |
| Performance Test | [DESCRIPTION] | ☐ Pass ☐ Fail ☐ Pending |

---

## Communication Plan

### Stakeholder Notifications

| Stakeholder | Notification Type | Timing |
|-------------|-------------------|--------|
| [STAKEHOLDER_1] | [Email / Slack / Meeting] | [TIMING] |
| [STAKEHOLDER_2] | [Email / Slack / Meeting] | [TIMING] |

### Notification Templates

**Pre-Change Notification:**
```
Subject: [Change ID] - Scheduled Change: [Title]

A change is scheduled for [DATE/TIME]:
- Change: [SUMMARY]
- Impact: [IMPACT_SUMMARY]
- Duration: [DURATION]

Contact [CONTACT] with questions.
```

**Post-Change Notification:**
```
Subject: [Change ID] - Change Complete: [Title]

The scheduled change has been completed successfully.
- Status: [SUCCESS / PARTIAL / ROLLBACK]
- Notes: [NOTES]
```

---

## Resource Requirements

### Personnel

| Role | Agent/Person | Availability Confirmed |
|------|--------------|------------------------|
| Change Implementer | [AGENT_ID] | ☐ |
| Technical Support | [AGENT_ID] | ☐ |
| Rollback Support | [AGENT_ID] | ☐ |

### Systems/Tools

| Resource | Purpose | Access Confirmed |
|----------|---------|------------------|
| [RESOURCE_1] | [PURPOSE] | ☐ |
| [RESOURCE_2] | [PURPOSE] | ☐ |

---

## Approvals

### Required Approvals

| Role | Approver | Decision | Date | Comments |
|------|----------|----------|------|----------|
| Change Manager | | ☐ Approve ☐ Reject | | |
| Technical Lead | | ☐ Approve ☐ Reject | | |
| Security (if applicable) | | ☐ Approve ☐ Reject | | |
| Business Owner | | ☐ Approve ☐ Reject | | |

### Approval Criteria by Change Type

**Standard Change:**
- Pre-approved, no additional approval needed
- Must match standard change definition

**Normal Change:**
- Technical lead approval required
- Change manager approval required
- Minimum 48 hours notice

**Emergency Change:**
- Verbal approval acceptable
- Retrospective documentation within 24 hours
- Post-implementation review required

---

## Post-Implementation Review

### Completion Status
| Item | Status |
|------|--------|
| Change Implemented | ☐ Yes ☐ No ☐ Partial |
| Rollback Required | ☐ Yes ☐ No |
| Issues Encountered | ☐ Yes ☐ No |

### Lessons Learned
[Document any issues, improvements, or learnings from this change]

### Follow-Up Actions

| Action | Owner | Due Date |
|--------|-------|----------|
| [ACTION_1] | [AGENT_ID] | [DATE] |
| [ACTION_2] | [AGENT_ID] | [DATE] |

---

*Template by HIVEMIND Change Management*
