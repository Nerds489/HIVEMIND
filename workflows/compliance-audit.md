# HIVEMIND Compliance Audit Workflow

## Overview

This workflow orchestrates comprehensive compliance audits, from scoping through remediation verification, ensuring adherence to regulatory frameworks and industry standards.

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       COMPLIANCE AUDIT PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1      PHASE 2      PHASE 3      PHASE 4      PHASE 5      PHASE 6  │
│  ┌──────┐    ┌──────┐     ┌──────┐     ┌──────┐     ┌──────┐     ┌──────┐  │
│  │SCOPE │──▶ │GATHER│ ──▶ │ASSESS│ ──▶ │REPORT│ ──▶ │REMEDIATE──▶ │VERIFY│  │
│  └──────┘    └──────┘     └──────┘     └──────┘     └──────┘     └──────┘  │
│                                                                              │
│  SEC-005     SEC-005      SEC-005      SEC-005      ALL TEAMS    SEC-005   │
│  SEC-001     ALL TEAMS    SEC-001      DEV-005                    SEC-001   │
│                           QA-004                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Supported Compliance Frameworks

| Framework | Scope | Typical Duration |
|-----------|-------|------------------|
| SOC 2 Type I | Trust Service Criteria snapshot | 2-4 weeks |
| SOC 2 Type II | Trust Service Criteria over time | 3-6 months |
| PCI-DSS | Payment card data security | 4-8 weeks |
| HIPAA | Healthcare data protection | 4-8 weeks |
| GDPR | EU data protection | 4-6 weeks |
| ISO 27001 | Information security management | 8-12 weeks |
| NIST CSF | Cybersecurity framework | 4-8 weeks |
| FedRAMP | Federal cloud security | 6-12 months |

---

## Trigger Conditions

This workflow is activated when:
- Annual compliance audit scheduled
- New compliance certification required
- Regulatory requirement changes
- Customer audit request received
- Pre-acquisition due diligence needed
- Incident requires compliance review

---

## Phase 1: Scoping & Planning

### Lead Agent: SEC-005 (Compliance Auditor)

### Duration: 3-5 days

### Activities

```yaml
scoping_activities:
  compliance_auditor:
    - Identify applicable frameworks
    - Define audit scope and boundaries
    - Identify systems in scope
    - Map data flows
    - Identify control owners
    - Create audit timeline
    - Prepare evidence request list

  security_architect:
    - Review current security posture
    - Identify known gaps
    - Provide architecture documentation
    - Clarify security controls
```

### Scope Definition Document

```json
{
  "audit_scope": {
    "audit_id": "AUDIT-2024-SOC2-001",
    "framework": "SOC 2 Type II",
    "trust_services_criteria": [
      "Security",
      "Availability",
      "Confidentiality"
    ],
    "audit_period": {
      "start": "2024-01-01",
      "end": "2024-06-30"
    },

    "systems_in_scope": [
      {
        "system": "Production Application",
        "components": ["Web servers", "API servers", "Database"],
        "data_classification": "Confidential"
      },
      {
        "system": "CI/CD Pipeline",
        "components": ["GitHub", "Jenkins", "Artifact Registry"],
        "data_classification": "Internal"
      }
    ],

    "systems_out_of_scope": [
      "Development environments",
      "Marketing website",
      "Internal wiki"
    ],

    "control_owners": {
      "access_management": "INF-002",
      "change_management": "DEV-006",
      "incident_response": "SEC-006",
      "data_protection": "SEC-001",
      "monitoring": "INF-005"
    },

    "evidence_sources": [
      "AWS CloudTrail logs",
      "GitHub audit logs",
      "PagerDuty incident records",
      "Jira tickets",
      "Confluence documentation"
    ]
  }
}
```

### Gate: Scope Approval

| Approver | Criteria |
|----------|----------|
| SEC-005 | Scope complete and achievable |
| SEC-001 | Systems correctly identified |
| Business Owner | Timeline approved |

---

## Phase 2: Evidence Gathering

### Lead Agent: SEC-005 (Compliance Auditor)

### Duration: 1-3 weeks

### Activities

```yaml
evidence_gathering:
  compliance_auditor:
    - Send evidence requests to control owners
    - Track evidence collection progress
    - Validate evidence completeness
    - Organize evidence repository
    - Document evidence chain of custody

  control_owners_by_domain:
    access_management:
      owner: INF-002
      evidence:
        - User access lists
        - Access review records
        - Privileged access logs
        - Termination procedures

    change_management:
      owner: DEV-006
      evidence:
        - Change request tickets
        - Approval workflows
        - Deployment logs
        - Rollback procedures

    incident_management:
      owner: SEC-006
      evidence:
        - Incident tickets
        - Response timelines
        - Post-mortems
        - Escalation records

    security_operations:
      owner: SEC-001
      evidence:
        - Security policies
        - Risk assessments
        - Vulnerability scans
        - Penetration test reports

    monitoring:
      owner: INF-005
      evidence:
        - Monitoring configurations
        - Alert records
        - SLO dashboards
        - Uptime reports
```

### Evidence Request Template

```markdown
## Evidence Request: [CONTROL_ID]

**Control:** [CONTROL_DESCRIPTION]

**Control Owner:** [AGENT_ID]

**Due Date:** [DATE]

**Evidence Required:**
1. [EVIDENCE_ITEM_1]
2. [EVIDENCE_ITEM_2]
3. [EVIDENCE_ITEM_3]

**Format:** [Document / Screenshot / System Export / Log File]

**Time Period:** [START_DATE] to [END_DATE]

**Notes:** [ADDITIONAL_CONTEXT]
```

### Evidence Tracking

| Control Area | Total Evidence | Collected | Pending | Gap |
|--------------|----------------|-----------|---------|-----|
| Access Management | 15 | 12 | 2 | 1 |
| Change Management | 12 | 12 | 0 | 0 |
| Incident Response | 8 | 6 | 2 | 0 |
| Security Operations | 20 | 18 | 1 | 1 |
| Monitoring | 10 | 10 | 0 | 0 |

---

## Phase 3: Control Assessment

### Lead Agent: SEC-005 (Compliance Auditor)

### Duration: 1-2 weeks

### Activities

```yaml
assessment_activities:
  compliance_auditor:
    - Evaluate control design
    - Test control operating effectiveness
    - Document control gaps
    - Assess risk impact
    - Interview control owners

  security_architect:
    - Validate security control implementation
    - Review technical configurations
    - Assess compensating controls

  security_tester:
    - Perform technical validation
    - Test access controls
    - Verify encryption
    - Validate logging
```

### Control Assessment Matrix

```markdown
## Control Assessment Results

| Control ID | Control Description | Design | Effectiveness | Evidence | Status |
|------------|---------------------|--------|---------------|----------|--------|
| CC6.1 | Logical access controls | ✓ | ✓ | Complete | Pass |
| CC6.2 | Access provisioning | ✓ | ✗ | Complete | Gap |
| CC6.3 | Access removal | ✓ | ✓ | Partial | Pass |
| CC7.1 | Change management | ✓ | ✓ | Complete | Pass |
| CC7.2 | Change testing | ✓ | ✓ | Complete | Pass |

Legend:
✓ = Satisfactory
✗ = Deficiency identified
◐ = Partial/Needs improvement
```

### Gap Documentation

```json
{
  "gap_finding": {
    "gap_id": "GAP-2024-001",
    "control_id": "CC6.2",
    "control": "Access Provisioning",
    "framework": "SOC 2",

    "finding": {
      "description": "Access provisioning requests are not consistently documented with business justification",
      "root_cause": "No formal access request template enforced",
      "impact": "Inability to demonstrate access was appropriately approved",
      "risk_level": "Medium"
    },

    "evidence": {
      "sample_size": 25,
      "exceptions": 8,
      "exception_rate": "32%"
    },

    "recommendation": {
      "action": "Implement formal access request workflow with mandatory business justification field",
      "owner": "INF-002",
      "timeline": "30 days",
      "compensating_control": "Manager approval emails retained"
    }
  }
}
```

### Gate: Assessment Review

| Approver | Criteria |
|----------|----------|
| SEC-005 | All controls assessed |
| SEC-001 | Technical findings validated |
| Business Owner | Gap remediation timeline acceptable |

---

## Phase 4: Reporting

### Lead Agent: SEC-005 (Compliance Auditor)

### Duration: 3-5 days

### Activities

```yaml
reporting_activities:
  compliance_auditor:
    - Compile audit findings
    - Write executive summary
    - Document detailed findings
    - Create remediation roadmap
    - Prepare management response

  technical_writer:
    - Format final report
    - Create visual summaries
    - Ensure consistency
    - Review for clarity
```

### Report Structure

```markdown
# Compliance Audit Report

## 1. Executive Summary
- Audit scope and objectives
- Overall assessment
- Key findings summary
- Recommendations

## 2. Audit Scope
- Framework(s) assessed
- Systems in scope
- Time period
- Methodology

## 3. Assessment Results
- Control summary table
- Pass/fail by control area
- Trend analysis (if recurring audit)

## 4. Detailed Findings
- Finding ID, description, evidence
- Risk rating
- Recommendation
- Management response

## 5. Gap Analysis
- Gaps by severity
- Root cause analysis
- Remediation timeline

## 6. Remediation Roadmap
- Prioritized action items
- Owners and deadlines
- Resource requirements

## 7. Appendices
- Evidence index
- Interview notes
- Technical test results
```

### Finding Severity Classification

| Severity | Criteria | Remediation Timeline |
|----------|----------|---------------------|
| Critical | Significant control failure, material risk | Immediate (7 days) |
| High | Control weakness with notable risk | 30 days |
| Medium | Control improvement needed | 60 days |
| Low | Minor enhancement opportunity | 90 days |
| Observation | Best practice recommendation | As capacity allows |

### Outputs Produced

- Executive Summary (2-3 pages)
- Detailed Audit Report (20-50 pages)
- Gap Register (spreadsheet)
- Remediation Roadmap
- Evidence Package (for auditors)

---

## Phase 5: Remediation

### Lead Agents: Various (per finding owner)

### Duration: 30-90 days (varies by findings)

### Activities

```yaml
remediation_activities:
  finding_owners:
    - Review assigned findings
    - Develop remediation plans
    - Implement fixes
    - Document changes
    - Collect closure evidence

  compliance_auditor:
    - Track remediation progress
    - Provide guidance on requirements
    - Validate remediation approach
    - Update gap register

  security_architect:
    - Review technical remediations
    - Validate security improvements
    - Approve control implementations
```

### Remediation Tracking

```json
{
  "remediation_tracker": {
    "audit_id": "AUDIT-2024-SOC2-001",
    "findings_total": 12,
    "findings_critical": 0,
    "findings_high": 2,
    "findings_medium": 6,
    "findings_low": 4,

    "status": {
      "remediated": 8,
      "in_progress": 3,
      "not_started": 1,
      "accepted_risk": 0
    },

    "findings": [
      {
        "gap_id": "GAP-2024-001",
        "severity": "Medium",
        "owner": "INF-002",
        "status": "Remediated",
        "remediation_date": "2024-02-15",
        "evidence": "/evidence/GAP-2024-001-remediation.pdf"
      }
    ]
  }
}
```

### Remediation Approaches

| Type | Description | Example |
|------|-------------|---------|
| Control Implementation | Add missing control | Implement MFA |
| Process Improvement | Enhance existing process | Add approval step |
| Documentation | Create/update policy | Write access policy |
| Technical Fix | Configure system | Enable logging |
| Compensating Control | Alternative control | Manual review |
| Risk Acceptance | Accept residual risk | Executive sign-off |

---

## Phase 6: Verification & Closure

### Lead Agent: SEC-005 (Compliance Auditor)

### Duration: 3-5 days

### Activities

```yaml
verification_activities:
  compliance_auditor:
    - Verify remediation completion
    - Test control effectiveness
    - Collect closure evidence
    - Update final report
    - Close audit findings

  security_architect:
    - Validate technical fixes
    - Confirm security posture
    - Sign off on remediations
```

### Verification Checklist

```markdown
## Finding Closure Checklist: [GAP_ID]

### Remediation Evidence
- [ ] Fix implemented
- [ ] Implementation documented
- [ ] Evidence collected
- [ ] Evidence reviewed

### Control Testing
- [ ] Control design validated
- [ ] Control effectiveness tested
- [ ] Sample testing passed
- [ ] No regression identified

### Approval
- [ ] Finding owner confirms completion
- [ ] Compliance auditor validates
- [ ] Security architect approves (if technical)
- [ ] Finding closed in tracker
```

### Audit Closure Report

```json
{
  "audit_closure": {
    "audit_id": "AUDIT-2024-SOC2-001",
    "status": "Closed",
    "closure_date": "2024-03-15",

    "final_results": {
      "controls_assessed": 85,
      "controls_passed": 82,
      "controls_with_findings": 12,
      "findings_remediated": 11,
      "findings_accepted_risk": 1,
      "overall_assessment": "Satisfactory"
    },

    "certification_status": {
      "eligible": true,
      "certification_date": "2024-03-20",
      "valid_until": "2025-03-20",
      "next_audit": "2024-07-01"
    },

    "lessons_learned": [
      "Start evidence collection earlier",
      "Improve documentation practices",
      "Automate compliance monitoring"
    ],

    "sign_off": {
      "compliance_auditor": "SEC-005",
      "security_architect": "SEC-001",
      "executive_sponsor": "[Name]"
    }
  }
}
```

---

## Continuous Compliance

### Ongoing Monitoring

| Activity | Frequency | Owner |
|----------|-----------|-------|
| Control self-assessment | Monthly | Control owners |
| Evidence refresh | Quarterly | SEC-005 |
| Policy review | Annually | SEC-001 |
| Risk assessment update | Annually | SEC-001 |
| Gap tracking review | Weekly | SEC-005 |

### Compliance Dashboard Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Controls with evidence | 100% | [X%] |
| Open gaps | 0 | [X] |
| Overdue remediations | 0 | [X] |
| Policy review completion | 100% | [X%] |
| Training completion | 100% | [X%] |

---

## Agent Responsibilities Summary

| Agent | Primary Role | Key Deliverables |
|-------|--------------|------------------|
| SEC-005 | Audit Lead | Scope, assessment, report |
| SEC-001 | Security Oversight | Technical validation, sign-off |
| QA-004 | Technical Testing | Control validation |
| DEV-005 | Documentation | Report formatting |
| INF-002 | Access Controls | Access evidence |
| DEV-006 | Change Management | Change evidence |
| SEC-006 | Incident Management | Incident evidence |
| INF-005 | Monitoring | Monitoring evidence |

---

## Templates Used

- `/templates/compliance-checklist.md` - Control assessment checklist
- `/templates/change-request.md` - Remediation change requests
- `/templates/security-report.md` - Audit report format

---

## Framework-Specific Considerations

### SOC 2
- Trust Service Criteria mapping
- Type I vs Type II considerations
- Service organization controls

### PCI-DSS
- Cardholder data environment scoping
- Compensating controls documentation
- Self-assessment vs QSA audit

### HIPAA
- PHI data mapping
- Business associate agreements
- Breach notification requirements

### GDPR
- Data subject rights
- Data processing agreements
- Cross-border transfer mechanisms

---

## Memory Integration

### Workflow Start
```
1. Load project memory context
2. Load relevant team memories
3. Create workflow session memory
4. Record workflow_id in session state
```

### Per-Phase Memory
```
Phase Entry:
- Load phase-specific memories
- Query relevant past executions

Phase Exit:
- Commit phase learnings
- Update workflow progress
```

### Workflow Completion
```
1. Consolidate all phase memories
2. Create workflow summary memory (episodic)
3. Update project memory with outcomes
4. Capture lessons learned (procedural)
5. Archive workflow session
```

### Memory Artifacts
| Artifact | Memory Type | Destination |
|----------|-------------|-------------|
| Decisions | semantic | team/project |
| Learnings | procedural | team |
| Issues Found | episodic | team |
| Outcomes | episodic | project |
