# Code Review Report

---

## Review Information

| Field | Value |
|-------|-------|
| **Review ID** | [REV-YYYYMMDD-XXX] |
| **Repository** | [REPO_NAME] |
| **Branch** | [BRANCH_NAME] |
| **PR/MR Number** | [#NUMBER] |
| **Author** | [AUTHOR_ID] |
| **Reviewers** | [AGENT_IDS] |
| **Review Date** | [DATE] |

---

## Summary

### Overview

| Metric | Value |
|--------|-------|
| Files Changed | [N] |
| Lines Added | [+N] |
| Lines Removed | [-N] |
| Commits | [N] |

### Findings Summary

| Severity | Count |
|----------|-------|
| Blocker | [N] |
| Critical | [N] |
| Major | [N] |
| Minor | [N] |
| Info | [N] |
| **Total** | **[N]** |

### Verdict

| Status | ☐ Approved | ☐ Approved with Comments | ☐ Changes Requested | ☐ Rejected |
|--------|------------|-------------------------|---------------------|------------|

---

## Automated Checks

| Check | Status | Details |
|-------|--------|---------|
| Build | [PASS | FAIL] | [DETAILS] |
| Unit Tests | [PASS | FAIL] | [N/N passed] |
| Coverage | [PASS | FAIL] | [XX%] (threshold: [YY%]) |
| Linting | [PASS | FAIL] | [N warnings, N errors] |
| SAST Scan | [PASS | FAIL] | [N findings] |
| Dependency Scan | [PASS | FAIL] | [N vulnerabilities] |
| Secrets Scan | [PASS | FAIL] | [N detected] |

---

## Review Checklist

### Code Quality
- [ ] Code follows project style guidelines
- [ ] No unnecessary complexity
- [ ] Functions are appropriately sized
- [ ] Naming is clear and consistent
- [ ] No commented-out code
- [ ] No debug statements left in

### Logic & Correctness
- [ ] Logic is correct and handles edge cases
- [ ] Error handling is appropriate
- [ ] No obvious bugs or issues
- [ ] Concurrency handled correctly (if applicable)

### Security
- [ ] Input validation present
- [ ] No injection vulnerabilities
- [ ] Authentication/authorization correct
- [ ] Sensitive data protected
- [ ] No hardcoded secrets

### Testing
- [ ] Tests cover new functionality
- [ ] Edge cases tested
- [ ] Tests are maintainable
- [ ] Test coverage adequate

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic has comments
- [ ] README updated if needed

---

## Detailed Findings

### [FINDING_ID]: [TITLE]

**Severity:** [BLOCKER | CRITICAL | MAJOR | MINOR | INFO]

**Category:** [Security | Performance | Maintainability | Logic | Style]

**File:** `[FILE_PATH]`

**Line(s):** [LINE_NUMBER(S)]

**Description:**
[Detailed description of the issue]

**Current Code:**
```[language]
[CODE_SNIPPET]
```

**Suggested Fix:**
```[language]
[SUGGESTED_CODE]
```

**Rationale:**
[Explanation of why this change is recommended]

**References:**
- [REFERENCE_LINK]

---

*[Repeat for each finding]*

---

## Positive Observations

What was done well in this PR:

- [POSITIVE_1]
- [POSITIVE_2]
- [POSITIVE_3]

---

## Required Changes

Before merge, the following MUST be addressed:

| # | Finding ID | Description | Priority |
|---|------------|-------------|----------|
| 1 | [ID] | [DESCRIPTION] | [BLOCKER | CRITICAL] |

---

## Recommended Changes

Suggested improvements (author's discretion):

| # | Finding ID | Description |
|---|------------|-------------|
| 1 | [ID] | [DESCRIPTION] |

---

## Questions for Author

- [QUESTION_1]
- [QUESTION_2]

---

## Security Review

**Security Review Required:** [YES | NO]

**Security Sensitive Areas:**
- [ ] Authentication/Authorization changes
- [ ] Encryption/Cryptography
- [ ] User input handling
- [ ] Database queries
- [ ] File operations
- [ ] External API integrations

**Security Review Status:** [PENDING | APPROVED | REJECTED]

**Security Reviewer:** [AGENT_ID]

---

## Approval

| Reviewer | Role | Decision | Date |
|----------|------|----------|------|
| [AGENT_ID] | Primary Reviewer | [DECISION] | [DATE] |
| [AGENT_ID] | Security Reviewer | [DECISION] | [DATE] |
| [AGENT_ID] | Domain Expert | [DECISION] | [DATE] |

---

## Follow-Up Items

| Item | Owner | Due | Ticket |
|------|-------|-----|--------|
| [ITEM] | [AGENT_ID] | [DATE] | [TICKET_ID] |

---

*Review completed by HIVEMIND Development Team*
