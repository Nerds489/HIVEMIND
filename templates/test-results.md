# Test Execution Report

---

## Execution Summary

| Field | Value |
|-------|-------|
| **Report ID** | [TEST-YYYYMMDD-XXX] |
| **Test Suite** | [SUITE_NAME] |
| **Environment** | [DEV | STAGING | PRODUCTION] |
| **Build/Version** | [VERSION] |
| **Executed By** | [AGENT_ID] |
| **Execution Date** | [DATE] |
| **Duration** | [DURATION] |

---

## Results Overview

### Overall Status: [PASS | FAIL | PARTIAL]

```
Total Tests:    [████████████████████] XXX
Passed:         [████████████████    ] XXX (XX%)
Failed:         [████                ] XXX (XX%)
Skipped:        [██                  ] XXX (XX%)
```

### By Category

| Category | Total | Passed | Failed | Skipped | Pass Rate |
|----------|-------|--------|--------|---------|-----------|
| Unit Tests | [N] | [N] | [N] | [N] | [XX%] |
| Integration | [N] | [N] | [N] | [N] | [XX%] |
| E2E | [N] | [N] | [N] | [N] | [XX%] |
| Performance | [N] | [N] | [N] | [N] | [XX%] |
| Security | [N] | [N] | [N] | [N] | [XX%] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **[XX%]** |

### By Priority

| Priority | Total | Passed | Failed |
|----------|-------|--------|--------|
| Critical (P0) | [N] | [N] | [N] |
| High (P1) | [N] | [N] | [N] |
| Medium (P2) | [N] | [N] | [N] |
| Low (P3) | [N] | [N] | [N] |

---

## Code Coverage

### Overall Coverage

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Line Coverage | [XX%] | [YY%] | [PASS | FAIL] |
| Branch Coverage | [XX%] | [YY%] | [PASS | FAIL] |
| Function Coverage | [XX%] | [YY%] | [PASS | FAIL] |

### Coverage by Module

| Module | Lines | Branches | Functions |
|--------|-------|----------|-----------|
| [MODULE_1] | [XX%] | [XX%] | [XX%] |
| [MODULE_2] | [XX%] | [XX%] | [XX%] |
| [MODULE_3] | [XX%] | [XX%] | [XX%] |

### Uncovered Critical Paths

- [ ] [PATH_DESCRIPTION_1]
- [ ] [PATH_DESCRIPTION_2]

---

## Failed Tests

### [TEST_NAME_1]

| Field | Value |
|-------|-------|
| **Test ID** | [TEST_ID] |
| **Category** | [CATEGORY] |
| **Priority** | [P0 | P1 | P2 | P3] |
| **File** | [FILE_PATH] |
| **Duration** | [DURATION] |

**Expected Result:**
```
[EXPECTED]
```

**Actual Result:**
```
[ACTUAL]
```

**Stack Trace:**
```
[STACK_TRACE]
```

**Screenshot/Evidence:**
![Test Failure](path/to/screenshot.png)

**Analysis:**
[Brief analysis of why this test failed]

**Recommended Action:**
[What needs to be done to fix this]

---

*[Repeat for each failed test]*

---

## Skipped Tests

| Test Name | Reason | Ticket |
|-----------|--------|--------|
| [TEST_NAME] | [REASON] | [TICKET_ID] |

---

## Performance Metrics

### Response Times

| Endpoint/Operation | Avg | P50 | P95 | P99 | Max | Target | Status |
|--------------------|-----|-----|-----|-----|-----|--------|--------|
| [ENDPOINT_1] | [MS] | [MS] | [MS] | [MS] | [MS] | [MS] | [PASS | FAIL] |
| [ENDPOINT_2] | [MS] | [MS] | [MS] | [MS] | [MS] | [MS] | [PASS | FAIL] |

### Throughput

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Requests/sec | [N] | [N] | [PASS | FAIL] |
| Transactions/sec | [N] | [N] | [PASS | FAIL] |

### Resource Usage

| Resource | Avg | Peak | Limit | Status |
|----------|-----|------|-------|--------|
| CPU | [XX%] | [XX%] | [XX%] | [PASS | FAIL] |
| Memory | [XX MB] | [XX MB] | [XX MB] | [PASS | FAIL] |
| Disk I/O | [XX MB/s] | [XX MB/s] | [XX MB/s] | [PASS | FAIL] |

---

## Security Test Results

### Vulnerability Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | [N] | [PASS if 0 | FAIL] |
| High | [N] | [PASS if 0 | FAIL] |
| Medium | [N] | [WARN if > 0] |
| Low | [N] | [INFO] |

### Security Findings

| ID | Title | Severity | Tool | Status |
|----|-------|----------|------|--------|
| [ID] | [TITLE] | [SEV] | [TOOL] | [New | Known | False Positive] |

---

## Test Environment

### Configuration

| Setting | Value |
|---------|-------|
| OS | [OS_VERSION] |
| Runtime | [RUNTIME_VERSION] |
| Database | [DB_VERSION] |
| Dependencies | [See package.json / requirements.txt] |

### Test Data

| Dataset | Size | Source |
|---------|------|--------|
| [DATASET_1] | [SIZE] | [SOURCE] |
| [DATASET_2] | [SIZE] | [SOURCE] |

---

## Trends

### Pass Rate Trend (Last 5 Runs)

```
Run 5: [████████████████████] XX% ← Current
Run 4: [██████████████████  ] XX%
Run 3: [████████████████████] XX%
Run 2: [██████████████      ] XX%
Run 1: [████████████████████] XX%
```

### Flaky Tests

| Test Name | Failure Rate | Last Failure | Ticket |
|-----------|--------------|--------------|--------|
| [TEST_NAME] | [XX%] | [DATE] | [TICKET_ID] |

---

## Recommendations

### Critical Actions (Must Address)

1. [ACTION_1]
2. [ACTION_2]

### Improvements (Should Address)

1. [IMPROVEMENT_1]
2. [IMPROVEMENT_2]

### Coverage Gaps

1. [GAP_1]
2. [GAP_2]

---

## Bug Tickets Created

| Ticket ID | Title | Priority | Assignee |
|-----------|-------|----------|----------|
| [TICKET_ID] | [TITLE] | [PRIORITY] | [AGENT_ID] |

---

## Attachments

| Item | Type | Location |
|------|------|----------|
| Full Test Log | Log | [PATH] |
| Coverage Report | HTML | [PATH] |
| Performance Data | CSV | [PATH] |
| Screenshots | ZIP | [PATH] |

---

## Sign-Off

| Role | Agent | Decision | Date |
|------|-------|----------|------|
| QA Lead | [AGENT_ID] | [APPROVED | NOT APPROVED] | [DATE] |
| Dev Lead | [AGENT_ID] | [ACKNOWLEDGED] | [DATE] |

---

*Report generated by HIVEMIND QA Team*
