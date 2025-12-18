# HIVEMIND Security Assessment Workflow

## Overview

This workflow defines the complete security assessment process, from initial scoping through final reporting and remediation verification.

---

## Workflow Phases

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SECURITY ASSESSMENT PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1        PHASE 2        PHASE 3        PHASE 4        PHASE 5       │
│  ┌──────┐      ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐       │
│  │SCOPE │ ──▶  │RECON │  ──▶  │TEST  │  ──▶  │REPORT│  ──▶  │VERIFY│       │
│  └──────┘      └──────┘       └──────┘       └──────┘       └──────┘       │
│                                                                              │
│  SEC-001       SEC-002        SEC-002        SEC-001        QA-004          │
│  SEC-005       SEC-004        SEC-003        SEC-005        SEC-002         │
│                               SEC-004        SEC-006                         │
│                               QA-004                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Scoping & Planning

### Lead Agent: SEC-001 (Security Architect)

### Activities

```yaml
scope_definition:
  activities:
    - Define assessment boundaries
    - Identify target systems and applications
    - Document exclusions and constraints
    - Establish rules of engagement
    - Define success criteria

  inputs:
    - Business requirements
    - System inventory
    - Previous assessment reports
    - Compliance requirements

  outputs:
    - Scope document
    - Rules of engagement
    - Test plan
    - Timeline and milestones
```

### Scope Document Template

```json
{
  "assessment_scope": {
    "assessment_id": "SEC-ASSESS-2024-001",
    "assessment_type": "penetration_test",
    "requested_by": "Engineering Leadership",
    "start_date": "2024-01-20",
    "end_date": "2024-01-27",

    "targets": {
      "in_scope": [
        {
          "target": "api.example.com",
          "type": "API",
          "description": "Production REST API",
          "testing_allowed": ["authentication", "authorization", "injection", "business_logic"]
        },
        {
          "target": "app.example.com",
          "type": "Web Application",
          "description": "Customer portal",
          "testing_allowed": ["full_pentest"]
        },
        {
          "target": "10.0.0.0/24",
          "type": "Network",
          "description": "Internal application network",
          "testing_allowed": ["vulnerability_scan", "service_enumeration"]
        }
      ],
      "out_of_scope": [
        "Production database (direct access)",
        "Third-party integrations",
        "Social engineering attacks",
        "Physical security testing"
      ]
    },

    "rules_of_engagement": {
      "testing_window": "Mon-Fri, 22:00-06:00 UTC",
      "notification_required": true,
      "emergency_contact": "security-oncall@example.com",
      "stop_conditions": [
        "Production impact detected",
        "Data exfiltration (actual customer data)",
        "System crash or instability"
      ],
      "allowed_techniques": [
        "Automated vulnerability scanning",
        "Manual penetration testing",
        "Code review (provided access)",
        "Configuration review"
      ],
      "prohibited_techniques": [
        "Denial of Service",
        "Data destruction",
        "Lateral movement beyond scope",
        "Credential stuffing with real credentials"
      ]
    },

    "compliance_context": {
      "frameworks": ["SOC2", "PCI-DSS"],
      "specific_requirements": [
        "PCI-DSS 11.3 - Penetration testing",
        "SOC2 CC6.1 - Security testing"
      ]
    },

    "approvals": [
      {"role": "CISO", "approved_at": "2024-01-18T10:00:00Z"},
      {"role": "Engineering Lead", "approved_at": "2024-01-18T14:00:00Z"}
    ]
  }
}
```

### Team Assembly

```yaml
team_assignment:
  lead: SEC-001
  members:
    - SEC-002: "Penetration testing execution"
    - SEC-004: "Wireless security (if applicable)"
    - QA-004: "Automated security scanning"
    - SEC-005: "Compliance mapping"

  support:
    - INF-002: "System access and credentials"
    - DEV-001: "Code access and architecture review"
```

### Entry Criteria

- [ ] Scope document approved by stakeholders
- [ ] Rules of engagement signed off
- [ ] Emergency contacts established
- [ ] Test environment access confirmed
- [ ] Backup and recovery plan in place

---

## Phase 2: Reconnaissance & Discovery

### Lead Agent: SEC-002 (Penetration Tester)

### Activities

```yaml
passive_reconnaissance:
  agent: SEC-002
  activities:
    - OSINT gathering
    - DNS enumeration
    - Technology fingerprinting
    - Public information analysis

  tools:
    - Shodan/Censys
    - DNS tools
    - WHOIS
    - Google dorking

active_reconnaissance:
  agent: SEC-002
  support: SEC-004
  activities:
    - Port scanning
    - Service enumeration
    - Version detection
    - Network mapping

  tools:
    - Nmap
    - Masscan
    - Service-specific scanners

wireless_reconnaissance:
  agent: SEC-004
  condition: "wireless_in_scope == true"
  activities:
    - Wireless network discovery
    - Signal strength mapping
    - Client enumeration
    - Protocol analysis

  tools:
    - Aircrack-ng suite
    - Kismet
    - WiFi Pineapple
```

### Reconnaissance Report

```json
{
  "reconnaissance_report": {
    "assessment_id": "SEC-ASSESS-2024-001",
    "phase": "reconnaissance",
    "completed_at": "2024-01-21T06:00:00Z",

    "attack_surface": {
      "external_services": [
        {
          "host": "api.example.com",
          "ip": "203.0.113.10",
          "ports": [443],
          "services": ["HTTPS/TLS 1.3", "REST API"],
          "technologies": ["nginx/1.24", "Python/FastAPI"],
          "notes": "API gateway detected"
        },
        {
          "host": "app.example.com",
          "ip": "203.0.113.11",
          "ports": [443],
          "services": ["HTTPS/TLS 1.3"],
          "technologies": ["React", "CloudFlare"],
          "notes": "SPA with CDN"
        }
      ],

      "internal_network": {
        "live_hosts": 45,
        "services_discovered": 127,
        "high_value_targets": [
          "10.0.0.10 - Database server (PostgreSQL)",
          "10.0.0.20 - Application server",
          "10.0.0.30 - Redis cache"
        ]
      },

      "wireless": {
        "networks_discovered": 3,
        "ssids": ["CorpWiFi", "Guest", "IoT-Devices"],
        "security_protocols": ["WPA3-Enterprise", "WPA2-PSK", "WPA2-PSK"]
      }
    },

    "initial_findings": [
      {
        "finding": "Exposed version information in HTTP headers",
        "severity": "informational",
        "location": "api.example.com",
        "details": "Server header reveals nginx version"
      },
      {
        "finding": "TLS configuration allows CBC ciphers",
        "severity": "low",
        "location": "api.example.com",
        "details": "BEAST attack theoretically possible"
      }
    ],

    "test_priorities": [
      "Authentication bypass on API",
      "Authorization flaws (IDOR)",
      "SQL injection in search functionality",
      "SSRF via file upload feature"
    ]
  }
}
```

### Handoff to Testing Phase

```json
{
  "handoff_package": {
    "from": "SEC-002",
    "to": ["SEC-002", "SEC-003", "SEC-004", "QA-004"],
    "phase_transition": "reconnaissance → testing",

    "deliverables": {
      "reconnaissance_report": "/artifacts/security/SEC-ASSESS-2024-001/recon-report.json",
      "network_map": "/artifacts/security/SEC-ASSESS-2024-001/network-diagram.png",
      "target_list": "/artifacts/security/SEC-ASSESS-2024-001/targets.csv"
    },

    "testing_assignments": {
      "SEC-002": ["API penetration testing", "Web application testing"],
      "SEC-003": ["Malware/payload analysis if needed"],
      "SEC-004": ["Wireless security testing"],
      "QA-004": ["Automated vulnerability scanning", "SAST/DAST"]
    }
  }
}
```

---

## Phase 3: Testing & Exploitation

### Lead Agents: SEC-002, QA-004

### Parallel Testing Tracks

```yaml
track_1_automated_scanning:
  agent: QA-004
  activities:
    - Vulnerability scanning (Nessus/Qualys)
    - DAST scanning (OWASP ZAP, Burp)
    - SAST analysis (if code access)
    - Dependency scanning (Snyk, Dependabot)
    - Container scanning (Trivy)

  output: automated_scan_results.json

track_2_manual_penetration_testing:
  agent: SEC-002
  activities:
    - Authentication testing
    - Authorization testing
    - Input validation testing
    - Business logic testing
    - API security testing

  methodology: OWASP Testing Guide
  output: manual_pentest_findings.json

track_3_wireless_testing:
  agent: SEC-004
  condition: "wireless_in_scope"
  activities:
    - WPA/WPA2/WPA3 testing
    - Rogue AP detection
    - Client isolation testing
    - Captive portal bypass

  output: wireless_assessment.json

track_4_code_review:
  agent: SEC-002
  support: DEV-004
  condition: "code_access_granted"
  activities:
    - Security-focused code review
    - Hardcoded secrets detection
    - Cryptographic implementation review
    - Authentication/authorization logic review

  output: code_review_findings.json
```

### Finding Classification

```yaml
severity_classification:
  critical:
    cvss: "9.0-10.0"
    criteria:
      - Remote code execution
      - Authentication bypass
      - SQL injection (privileged)
      - Complete data breach possible
    response_time: "Immediate (within 24 hours)"

  high:
    cvss: "7.0-8.9"
    criteria:
      - Privilege escalation
      - Significant data exposure
      - SSRF to internal systems
      - Stored XSS (admin context)
    response_time: "Within 7 days"

  medium:
    cvss: "4.0-6.9"
    criteria:
      - Information disclosure
      - CSRF
      - Reflected XSS
      - Session management flaws
    response_time: "Within 30 days"

  low:
    cvss: "0.1-3.9"
    criteria:
      - Minor information leakage
      - Missing security headers
      - Verbose error messages
    response_time: "Within 90 days"

  informational:
    cvss: "0.0"
    criteria:
      - Best practice recommendations
      - Defense in depth suggestions
    response_time: "Advisory only"
```

### Finding Documentation Template

```json
{
  "finding": {
    "finding_id": "FIND-2024-001-007",
    "title": "SQL Injection in User Search API",
    "severity": "critical",
    "cvss_score": 9.8,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",

    "location": {
      "endpoint": "GET /api/v1/users/search",
      "parameter": "q",
      "file": "/src/api/users/search.py",
      "line": 45
    },

    "description": "The user search endpoint is vulnerable to SQL injection via the 'q' parameter. User input is directly concatenated into the SQL query without sanitization or parameterization.",

    "technical_details": {
      "vulnerable_code": "query = f\"SELECT * FROM users WHERE name LIKE '%{search_term}%'\"",
      "payload_used": "' OR '1'='1' --",
      "impact": "Full database access, including ability to read, modify, or delete all data"
    },

    "proof_of_concept": {
      "request": "GET /api/v1/users/search?q=' UNION SELECT username,password,email,null,null FROM admin_users-- HTTP/1.1",
      "response": "[Admin user credentials returned]",
      "screenshot": "/artifacts/security/findings/FIND-2024-001-007-poc.png"
    },

    "remediation": {
      "recommendation": "Use parameterized queries or ORM methods",
      "example_fix": "query = session.query(User).filter(User.name.ilike(f'%{search_term}%'))",
      "references": [
        "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
      ]
    },

    "compliance_impact": {
      "PCI-DSS": "6.5.1 - Injection flaws",
      "SOC2": "CC6.1 - Security vulnerabilities"
    },

    "discovered_by": "SEC-002",
    "discovered_at": "2024-01-22T03:15:00Z",
    "verified_by": "QA-004",
    "verified_at": "2024-01-22T04:00:00Z"
  }
}
```

### Testing Progress Tracking

```json
{
  "testing_progress": {
    "assessment_id": "SEC-ASSESS-2024-001",
    "last_updated": "2024-01-23T12:00:00Z",

    "coverage": {
      "targets_tested": "12/15",
      "test_cases_executed": "245/280",
      "coverage_percentage": 87
    },

    "findings_summary": {
      "critical": 1,
      "high": 3,
      "medium": 8,
      "low": 12,
      "informational": 15
    },

    "track_status": {
      "automated_scanning": "complete",
      "manual_testing": "in_progress",
      "wireless_testing": "complete",
      "code_review": "pending"
    },

    "blockers": [],

    "estimated_completion": "2024-01-24T06:00:00Z"
  }
}
```

---

## Phase 4: Reporting

### Lead Agent: SEC-001 (Security Architect)

### Report Components

```yaml
executive_summary:
  author: SEC-001
  audience: "Executive leadership"
  content:
    - Assessment overview
    - Key findings summary
    - Risk rating
    - Recommended actions
  length: "1-2 pages"

technical_report:
  author: SEC-002
  reviewer: SEC-001
  audience: "Technical teams"
  content:
    - Detailed methodology
    - All findings with technical details
    - Proof of concepts
    - Remediation guidance
  length: "Full detail"

compliance_mapping:
  author: SEC-005
  audience: "Compliance/Audit"
  content:
    - Findings mapped to controls
    - Compliance gaps identified
    - Remediation requirements
    - Audit evidence

remediation_plan:
  author: SEC-001
  collaborators: [DEV-001, INF-001]
  content:
    - Prioritized fix list
    - Owner assignments
    - Timeline recommendations
    - Verification criteria
```

### Report Structure

```markdown
# Security Assessment Report
## Assessment ID: SEC-ASSESS-2024-001

### 1. Executive Summary
- Overall risk rating: HIGH
- Critical findings: 1
- High findings: 3
- Immediate actions required: 2

### 2. Scope and Methodology
- Targets assessed
- Testing methodology (OWASP, PTES)
- Tools used
- Limitations

### 3. Findings Summary
| ID | Title | Severity | Status |
|----|-------|----------|--------|
| FIND-001 | SQL Injection | Critical | Open |

### 4. Detailed Findings
[Each finding with full details]

### 5. Remediation Roadmap
| Priority | Finding | Owner | Due Date |
|----------|---------|-------|----------|
| 1 | SQL Injection | DEV-002 | Jan 25 |

### 6. Appendices
- A: Raw scan results
- B: Screenshots/POCs
- C: Compliance mapping
```

### Report Review Gate

```yaml
review_checklist:
  technical_accuracy:
    reviewer: SEC-002
    checks:
      - [ ] All findings accurately described
      - [ ] POCs are reproducible
      - [ ] Severity ratings appropriate
      - [ ] Remediation recommendations valid

  compliance_accuracy:
    reviewer: SEC-005
    checks:
      - [ ] Compliance mappings correct
      - [ ] Regulatory requirements addressed
      - [ ] Audit evidence complete

  classification_review:
    reviewer: SEC-001
    checks:
      - [ ] No sensitive data exposed
      - [ ] POCs sanitized
      - [ ] Distribution list appropriate
      - [ ] Handling instructions included

  final_approval:
    approver: SEC-001
    gate: "Security Assessment Publication Gate"
```

---

## Phase 5: Remediation Verification

### Lead Agent: QA-004 (Security Tester)

### Verification Process

```yaml
remediation_verification:
  for_each_finding:
    steps:
      - Confirm fix deployed
      - Re-test original vulnerability
      - Test for regressions
      - Test for bypass attempts
      - Document verification results

    outcomes:
      - "verified_fixed": "Original issue resolved, no bypass found"
      - "partially_fixed": "Some vectors addressed, others remain"
      - "not_fixed": "Vulnerability still present"
      - "regression": "Fix introduced new issues"
```

### Verification Report

```json
{
  "remediation_verification": {
    "assessment_id": "SEC-ASSESS-2024-001",
    "verification_date": "2024-02-01",
    "verified_by": "QA-004",

    "findings_status": [
      {
        "finding_id": "FIND-2024-001-007",
        "original_severity": "critical",
        "fix_status": "verified_fixed",
        "verification_notes": "Parameterized queries implemented. Re-tested all injection vectors - none successful.",
        "verified_at": "2024-02-01T10:00:00Z"
      },
      {
        "finding_id": "FIND-2024-001-003",
        "original_severity": "high",
        "fix_status": "partially_fixed",
        "verification_notes": "Main vector fixed but similar pattern found in /api/v2/search",
        "new_finding_id": "FIND-2024-002-001",
        "verified_at": "2024-02-01T11:00:00Z"
      }
    ],

    "summary": {
      "total_findings": 24,
      "verified_fixed": 20,
      "partially_fixed": 2,
      "not_fixed": 1,
      "deferred": 1
    },

    "recommendation": "Schedule follow-up assessment for remaining issues"
  }
}
```

### Closure Criteria

```yaml
assessment_closure:
  criteria:
    - All critical findings verified fixed
    - All high findings verified fixed OR have approved risk acceptance
    - Final report delivered and acknowledged
    - Compliance evidence archived
    - Lessons learned documented

  sign_off_required:
    - SEC-001: "Technical closure"
    - SEC-005: "Compliance closure"
    - Stakeholder: "Business acceptance"
```

---

## Assessment Types Quick Reference

### Full Penetration Test
```yaml
scope: "Complete security assessment"
duration: "2-4 weeks"
agents: [SEC-001, SEC-002, SEC-004, QA-004, SEC-005]
phases: [Scope, Recon, Test, Report, Verify]
```

### Vulnerability Assessment
```yaml
scope: "Automated scanning + validation"
duration: "1-2 weeks"
agents: [QA-004, SEC-002]
phases: [Scope, Scan, Validate, Report]
```

### Code Security Review
```yaml
scope: "Source code analysis"
duration: "1-2 weeks"
agents: [SEC-002, DEV-004, QA-004]
phases: [Scope, SAST, Manual Review, Report]
```

### Wireless Assessment
```yaml
scope: "Wireless network security"
duration: "3-5 days"
agents: [SEC-004, SEC-002]
phases: [Scope, Recon, Test, Report]
```

### Compliance Assessment
```yaml
scope: "Control validation"
duration: "2-3 weeks"
agents: [SEC-005, SEC-001, QA-004]
phases: [Scope, Evidence Collection, Gap Analysis, Report]
```

---

## Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Finding Detection Rate | > 90% | Findings / Known Vulnerabilities |
| False Positive Rate | < 10% | Invalid Findings / Total Findings |
| Remediation Verification Time | < 48 hours | Time to verify fix |
| Report Delivery Time | < 5 days | End of testing to report |
| Critical Finding Response | < 24 hours | Detection to stakeholder notification |
| Assessment Coverage | > 95% | Tested Targets / In-Scope Targets |

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

---

## Rollback Procedure

### When to Rollback
- Testing causes unintended system impact
- False positive leads to incorrect remediation
- Remediation breaks functionality

### Assessment Rollback Steps
1. **Pause**: Stop current assessment activities
2. **Document**: Record current state and findings
3. **Assess Impact**: Determine scope of rollback needed
4. **Coordinate**: Notify affected teams
5. **Execute**: Perform rollback of any changes made
6. **Verify**: Confirm system returned to baseline

### Remediation Rollback
```
1. Identify problematic remediation
2. Revert configuration/code changes
3. Restore from backup if needed
4. Re-test affected functionality
5. Document issue for future assessments
6. Update finding with rollback note
```

### Prevention
- Always test remediations in non-production first
- Document baseline before any changes
- Maintain rollback scripts for common fixes
- Include rollback plan in remediation tickets
