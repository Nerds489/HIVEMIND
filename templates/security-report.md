# Security Assessment Report

---

## Report Information

| Field | Value |
|-------|-------|
| **Report ID** | [REPORT_ID] |
| **Assessment Type** | [Penetration Test / Vulnerability Assessment / Code Review] |
| **Classification** | [RESTRICTED / CONFIDENTIAL / INTERNAL] |
| **Version** | [VERSION] |
| **Date** | [DATE] |
| **Prepared By** | [AGENT_IDS] |
| **Reviewed By** | [REVIEWER_AGENT_IDS] |

---

## Distribution

| Recipient | Role | Access Level |
|-----------|------|--------------|
| [NAME] | [ROLE] | [Full / Executive Summary Only] |

---

## Executive Summary

### Assessment Overview

[2-3 paragraph summary of what was tested, methodology used, and overall findings. Written for non-technical executive audience.]

### Risk Rating

| Overall Risk Level | [CRITICAL / HIGH / MEDIUM / LOW] |
|--------------------|----------------------------------|
| Justification | [Brief explanation of rating] |

### Key Findings Summary

| Severity | Count | Trend |
|----------|-------|-------|
| Critical | [N] | [↑/↓/→] |
| High | [N] | [↑/↓/→] |
| Medium | [N] | [↑/↓/→] |
| Low | [N] | [↑/↓/→] |
| Informational | [N] | - |

### Top 3 Priorities

1. **[FINDING_TITLE]** - [One sentence impact and recommended action]
2. **[FINDING_TITLE]** - [One sentence impact and recommended action]
3. **[FINDING_TITLE]** - [One sentence impact and recommended action]

### Key Recommendations

- [RECOMMENDATION_1]
- [RECOMMENDATION_2]
- [RECOMMENDATION_3]

---

## Scope

### In Scope

| Target | Type | Description |
|--------|------|-------------|
| [TARGET_1] | [Web App / API / Network / etc.] | [DESCRIPTION] |
| [TARGET_2] | [TYPE] | [DESCRIPTION] |

### Out of Scope

- [EXCLUSION_1]
- [EXCLUSION_2]

### Testing Window

| Start Date | End Date | Total Hours |
|------------|----------|-------------|
| [DATE] | [DATE] | [N] |

### Rules of Engagement

- [RULE_1]
- [RULE_2]
- [RESTRICTIONS]

---

## Methodology

### Testing Approach

[Description of overall testing methodology - e.g., OWASP Testing Guide, PTES, custom approach]

### Testing Phases

| Phase | Description | Duration |
|-------|-------------|----------|
| Reconnaissance | [ACTIVITIES] | [DURATION] |
| Vulnerability Assessment | [ACTIVITIES] | [DURATION] |
| Exploitation | [ACTIVITIES] | [DURATION] |
| Post-Exploitation | [ACTIVITIES] | [DURATION] |
| Reporting | [ACTIVITIES] | [DURATION] |

### Tools Used

| Category | Tools |
|----------|-------|
| Scanning | [TOOL_LIST] |
| Exploitation | [TOOL_LIST] |
| Analysis | [TOOL_LIST] |

---

## Findings Summary

### By Severity

```
Critical  [████████████████████] N findings
High      [██████████████      ] N findings
Medium    [████████            ] N findings
Low       [████                ] N findings
Info      [██                  ] N findings
```

### By Category

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Injection | [N] | [N] | [N] | [N] | [N] |
| Authentication | [N] | [N] | [N] | [N] | [N] |
| Authorization | [N] | [N] | [N] | [N] | [N] |
| Cryptography | [N] | [N] | [N] | [N] | [N] |
| Configuration | [N] | [N] | [N] | [N] | [N] |
| Other | [N] | [N] | [N] | [N] | [N] |

### Findings Table

| ID | Title | Severity | CVSS | Status | Location |
|----|-------|----------|------|--------|----------|
| [ID] | [TITLE] | [SEV] | [SCORE] | [Open/Remediated] | [LOCATION] |

---

## Detailed Findings

### [FINDING_ID]: [FINDING_TITLE]

#### Overview

| Attribute | Value |
|-----------|-------|
| **Severity** | [CRITICAL / HIGH / MEDIUM / LOW / INFO] |
| **CVSS Score** | [SCORE] |
| **CVSS Vector** | [VECTOR_STRING] |
| **CWE** | [CWE-XXX: Title] |
| **OWASP** | [Category] |
| **Status** | [Open / Remediated / Accepted Risk] |

#### Affected Assets

- [ASSET_1]
- [ASSET_2]

#### Description

[Detailed technical description of the vulnerability. What is it? How does it work? Why is it a problem?]

#### Evidence

##### Request
```http
[RAW_REQUEST]
```

##### Response
```http
[RAW_RESPONSE]
```

##### Screenshot
![Description](path/to/screenshot.png)

#### Impact Analysis

**Confidentiality:** [HIGH / MEDIUM / LOW / NONE]
[Explanation of impact on data confidentiality]

**Integrity:** [HIGH / MEDIUM / LOW / NONE]
[Explanation of impact on data integrity]

**Availability:** [HIGH / MEDIUM / LOW / NONE]
[Explanation of impact on system availability]

**Business Impact:**
[Description of potential business consequences - financial, reputational, regulatory]

#### Remediation

**Recommended Fix:**
[Specific, actionable remediation guidance]

**Code Example (if applicable):**
```[language]
// Vulnerable code
[VULNERABLE_CODE]

// Fixed code
[FIXED_CODE]
```

**Verification Steps:**
1. [STEP_1]
2. [STEP_2]
3. [STEP_3]

#### References

- [CVE-XXXX-XXXXX](https://cve.mitre.org/...)
- [OWASP Reference](https://owasp.org/...)
- [Vendor Advisory](https://...)

---

*[Repeat Detailed Findings section for each finding]*

---

## Remediation Roadmap

### Priority Matrix

| Priority | Finding IDs | Owner | Due Date | Effort |
|----------|-------------|-------|----------|--------|
| Immediate (0-7 days) | [IDS] | [OWNER] | [DATE] | [EFFORT] |
| Short-term (7-30 days) | [IDS] | [OWNER] | [DATE] | [EFFORT] |
| Medium-term (30-90 days) | [IDS] | [OWNER] | [DATE] | [EFFORT] |
| Long-term (90+ days) | [IDS] | [OWNER] | [DATE] | [EFFORT] |

### Quick Wins

Findings that can be remediated with minimal effort:

1. [FINDING] - [EFFORT_DESCRIPTION]
2. [FINDING] - [EFFORT_DESCRIPTION]

### Strategic Improvements

Larger changes that address root causes:

1. [IMPROVEMENT] - [DESCRIPTION]
2. [IMPROVEMENT] - [DESCRIPTION]

---

## Compliance Mapping

### [FRAMEWORK_NAME] (e.g., PCI-DSS, SOC2, GDPR)

| Control | Status | Findings |
|---------|--------|----------|
| [CONTROL_ID] | [Compliant / Non-Compliant / Partial] | [FINDING_IDS] |

---

## Positive Observations

Areas where security controls were effective:

- [POSITIVE_1]
- [POSITIVE_2]
- [POSITIVE_3]

---

## Appendices

### Appendix A: Raw Scan Results

[Reference to attached scan output files]

### Appendix B: Testing Logs

[Reference to detailed testing logs]

### Appendix C: Tool Configurations

[Configuration files used for tools]

### Appendix D: Glossary

| Term | Definition |
|------|------------|
| [TERM] | [DEFINITION] |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| [VER] | [DATE] | [AUTHOR] | [CHANGES] |

---

*This report contains sensitive security information. Handle according to classification level.*

*Report generated by HIVEMIND Security Team*
