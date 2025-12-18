# HIVEMIND Security Gates Protocol

## Overview

Security gates are mandatory checkpoints that enforce security requirements before critical actions can proceed. This protocol defines all security gates, their criteria, and bypass procedures.

---

## Gate 1: Code Merge Gate

**Purpose:** Ensure code quality and security before merging to protected branches.

### Required Approvers
- **Primary:** DEV-004 (Code Reviewer)
- **Security-sensitive changes:** + QA-004 (Security Tester)

### Criteria Checklist

```
AUTOMATED CHECKS (All must pass)
[ ] Build succeeds
[ ] Unit tests pass (100%)
[ ] Code coverage ≥ 80%
[ ] Linting passes (zero errors)
[ ] SAST scan clean (no critical/high)
[ ] Dependency scan clean (no critical/high CVEs)
[ ] Secrets scan clean (no credentials detected)

CODE REVIEW CHECKS
[ ] Code follows established patterns
[ ] No obvious bugs or logic errors
[ ] Error handling is appropriate
[ ] Logging is adequate (not excessive)
[ ] No hardcoded secrets or credentials
[ ] No commented-out code
[ ] Functions are reasonably sized
[ ] Names are clear and consistent

SECURITY REVIEW CHECKS (if security-sensitive)
[ ] Input validation on all user inputs
[ ] Output encoding prevents XSS
[ ] Parameterized queries prevent SQL injection
[ ] Authentication/authorization correct
[ ] Sensitive data properly protected
[ ] Rate limiting where appropriate
[ ] CSRF protection on state-changing operations
[ ] Secure communication (TLS)

DOCUMENTATION CHECKS
[ ] Public APIs documented
[ ] Complex logic has explanatory comments
[ ] README updated if needed
[ ] CHANGELOG updated
```

### Security-Sensitive Triggers

Changes to these areas REQUIRE security review:
- Authentication/authorization logic
- Encryption/cryptography
- User input handling
- Database queries
- File operations
- External API integrations
- Configuration/secrets management
- Permission/access control

### Decision Matrix

| Automated | Code Review | Security Review | Decision |
|-----------|-------------|-----------------|----------|
| ✓ Pass | ✓ Approved | ✓ Approved (if needed) | **MERGE** |
| ✓ Pass | ✓ Approved | ✗ Not Done (needed) | **BLOCK** |
| ✓ Pass | ✗ Changes Req | N/A | **BLOCK** |
| ✗ Fail | N/A | N/A | **BLOCK** |

### Bypass Conditions

Emergency bypass requires:
1. P0 incident with documented business justification
2. SEC-001 (Security Architect) approval
3. Commitment to address within 24 hours
4. Audit entry created

```json
{
  "gate_bypass": {
    "gate": "code_merge",
    "pr": "#1234",
    "bypassed_by": "SEC-001",
    "timestamp": "2024-01-15T10:00:00Z",
    "justification": "P0 production incident - authentication failing",
    "criteria_bypassed": ["security_review"],
    "followup_required": "Security review within 24 hours",
    "followup_deadline": "2024-01-16T10:00:00Z",
    "audit_id": "AUDIT-2024-0042"
  }
}
```

---

## Gate 2: Production Deployment Gate

**Purpose:** Ensure system is ready for production deployment.

### Required Approvers
- **Primary:** QA-001 (QA Architect)
- **Infrastructure:** INF-005 (SRE)
- **Security:** SEC-001 (Security Architect)

### Criteria Checklist

```
QA VERIFICATION (QA-001)
[ ] All functional tests pass
[ ] Regression test suite passes
[ ] Performance tests meet baselines
[ ] No P0/P1 bugs open
[ ] Exploratory testing completed
[ ] User acceptance criteria met

INFRASTRUCTURE READINESS (INF-005)
[ ] Deployment artifacts validated
[ ] Target environment healthy
[ ] Rollback plan documented and tested
[ ] Monitoring dashboards ready
[ ] Alerts configured
[ ] Runbooks updated
[ ] On-call team notified

SECURITY APPROVAL (SEC-001)
[ ] Security testing completed
[ ] No critical/high vulnerabilities
[ ] Compliance requirements met
[ ] Data protection verified
[ ] Access controls validated
[ ] Audit logging confirmed

DEPLOYMENT READINESS
[ ] Change request approved
[ ] Maintenance window scheduled (if needed)
[ ] Stakeholders notified
[ ] Communication plan ready
[ ] Support team briefed
```

### Pre-Deployment Verification

```json
{
  "deployment_readiness": {
    "release": "v2.1.0",
    "target": "production",
    "timestamp": "2024-01-15T18:00:00Z",

    "qa_approval": {
      "approved_by": "QA-001",
      "approved_at": "2024-01-15T16:00:00Z",
      "test_results": {
        "functional": "256/256 passed",
        "regression": "1024/1024 passed",
        "performance": "All baselines met"
      },
      "open_bugs": {"P0": 0, "P1": 0, "P2": 3, "P3": 12}
    },

    "infra_approval": {
      "approved_by": "INF-005",
      "approved_at": "2024-01-15T17:00:00Z",
      "environment_health": "green",
      "rollback_plan": "/runbooks/rollback-v2.1.0.md",
      "monitoring_status": "configured"
    },

    "security_approval": {
      "approved_by": "SEC-001",
      "approved_at": "2024-01-15T17:30:00Z",
      "scan_results": "No critical/high findings",
      "compliance_status": "All controls satisfied"
    },

    "gate_status": "APPROVED"
  }
}
```

### Rollback Requirements

Every deployment must have:
1. Documented rollback procedure
2. Tested rollback (in staging)
3. Estimated rollback time
4. Rollback decision criteria
5. Data rollback plan (if applicable)

---

## Gate 3: Security Assessment Publication Gate

**Purpose:** Control distribution of security findings.

### Required Approvers
- **Primary:** SEC-001 (Security Architect)
- **Compliance:** SEC-005 (Compliance Auditor)

### Criteria Checklist

```
CONTENT REVIEW
[ ] All findings accurately described
[ ] Severity ratings appropriate
[ ] No false positives included
[ ] Remediation recommendations provided
[ ] Timeline for fixes agreed

SENSITIVE DATA HANDLING
[ ] No actual credentials included
[ ] No exploitable details in executive summary
[ ] Technical details appropriately restricted
[ ] POC code marked as sensitive
[ ] Screenshots sanitized

DISTRIBUTION CONTROL
[ ] Distribution list approved
[ ] Classification level assigned
[ ] Handling instructions included
[ ] Retention period defined
[ ] Destruction procedure documented

LEGAL/COMPLIANCE
[ ] Disclosure requirements met
[ ] Regulatory notifications identified
[ ] Legal review (if required)
[ ] NDA coverage confirmed
```

### Classification Levels

| Level | Description | Distribution | Handling |
|-------|-------------|--------------|----------|
| **Restricted** | Active exploits, credentials | Security team only | Encrypted, immediate deletion |
| **Confidential** | Detailed findings | Technical stakeholders | Encrypted storage |
| **Internal** | Summary findings | Company-wide OK | Standard controls |
| **Public** | Generic recommendations | External OK | No restrictions |

### Redaction Requirements

Must redact before broader distribution:
- Specific vulnerable versions
- Exact exploit code
- Internal IP addresses
- User credentials (even test)
- Customer data samples
- Security tool configurations

---

## Gate 4: Infrastructure Change Gate

**Purpose:** Ensure infrastructure changes are safe and controlled.

### Required Approvers
- **Primary:** INF-001 (Infrastructure Architect)
- **Network:** INF-003 (Network Engineer) for network changes
- **Security:** SEC-001 (Security Architect) for security-impacting changes

### Criteria Checklist

```
CHANGE DOCUMENTATION
[ ] Change request documented
[ ] Business justification provided
[ ] Technical approach reviewed
[ ] Impact assessment completed
[ ] Risk assessment completed

TESTING
[ ] Change tested in non-production
[ ] Test results documented
[ ] No unexpected side effects
[ ] Performance impact assessed

ROLLBACK
[ ] Rollback procedure documented
[ ] Rollback tested
[ ] Rollback time estimated
[ ] Rollback triggers defined

COORDINATION
[ ] Maintenance window approved
[ ] Affected teams notified
[ ] On-call coverage confirmed
[ ] Communication plan ready

SECURITY (for security-impacting changes)
[ ] Security review completed
[ ] Firewall rules reviewed
[ ] Access controls verified
[ ] Encryption requirements met
[ ] Compliance impact assessed
```

### Change Categories

| Category | Approval Level | Examples |
|----------|---------------|----------|
| **Standard** | INF-001 | Routine patching, scaling |
| **Normal** | INF-001 + affected team lead | New service, config change |
| **Security** | + SEC-001 | Firewall rules, access changes |
| **Emergency** | INF-001 + post-review | Critical fix |

### Change Window Requirements

| Environment | Standard Window | Emergency |
|-------------|-----------------|-----------|
| Production | Tue-Thu, 2-6 AM UTC | Anytime with approval |
| Staging | Business hours | Anytime |
| Development | Anytime | N/A |

---

## Gate 5: Incident Declaration Gate

**Purpose:** Ensure incidents are properly classified and resourced.

### Required Approvers
- **Primary:** SEC-006 (Incident Responder)
- **Support:** INF-005 (SRE)

### Severity Classification Criteria

```
SEV1 - CRITICAL
[ ] Complete service outage
[ ] Active security breach
[ ] Data loss confirmed
[ ] Customer-facing impact > 50%
[ ] Revenue impact immediate

SEV2 - HIGH
[ ] Major feature unavailable
[ ] Security vulnerability actively exploited
[ ] Data exposure potential
[ ] Customer-facing impact > 10%
[ ] Significant performance degradation

SEV3 - MEDIUM
[ ] Feature degradation
[ ] Security issue confirmed (not exploited)
[ ] Limited customer impact
[ ] Workaround available

SEV4 - LOW
[ ] Minor issue
[ ] No customer impact
[ ] Cosmetic or minor bug
```

### Declaration Checklist

```
INCIDENT DECLARATION
[ ] Severity level determined
[ ] Incident commander assigned
[ ] Communication channels opened
[ ] Initial notification sent
[ ] Response team activated

RESOURCE ALLOCATION
[ ] Required agents identified
[ ] Agents made available
[ ] External resources identified (if needed)
[ ] Management notified (SEV1/2)

DOCUMENTATION
[ ] Incident ticket created
[ ] Timeline started
[ ] Initial assessment documented
[ ] Affected systems listed
```

### Communication Protocol by Severity

| Severity | Internal Notification | Customer Notification | Executive Notification |
|----------|----------------------|----------------------|----------------------|
| SEV1 | Immediate, all teams | Within 30 minutes | Immediate |
| SEV2 | Immediate, affected teams | Within 2 hours | Within 1 hour |
| SEV3 | Within 4 hours | If asked | Daily summary |
| SEV4 | Next standup | No | No |

---

## Gate Audit Requirements

All gate decisions must be auditable:

```json
{
  "gate_audit": {
    "gate_id": "GATE-2024-0142",
    "gate_type": "production_deployment",
    "timestamp": "2024-01-15T18:00:00Z",
    "decision": "approved",

    "approvers": [
      {"agent": "QA-001", "approved_at": "2024-01-15T16:00:00Z"},
      {"agent": "INF-005", "approved_at": "2024-01-15T17:00:00Z"},
      {"agent": "SEC-001", "approved_at": "2024-01-15T17:30:00Z"}
    ],

    "criteria_status": {
      "qa_tests_passed": true,
      "security_scan_clean": true,
      "rollback_plan_ready": true
    },

    "bypasses": [],

    "artifacts": [
      "/artifacts/deployments/v2.1.0/qa-signoff.json",
      "/artifacts/deployments/v2.1.0/security-scan.json"
    ],

    "retention": "7 years"
  }
}
```

---

## Gate Metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Gate Pass Rate | > 90% | < 80% |
| Bypass Rate | < 5% | > 10% |
| Average Gate Time | < 4 hours | > 8 hours |
| Post-Bypass Issue Rate | 0% | > 0% |
| Audit Completeness | 100% | < 100% |
