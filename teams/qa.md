# Quality Assurance & Validation Team

## Team Overview

**Mission:** Catch problems before users do. Verify that software meets requirements, performs well, and provides a good user experience.

**Leader:** QA Architect

**Size:** 6 Agents

## Internal Registry (IDs)

This mapping is for internal routing/documentation only. Never include these IDs in user-visible output.

| Internal ID | Role | Specialty |
|-------------|------|-----------|
| QA-001 | QA Architect | Test strategy |
| QA-002 | Test Automation Engineer | Automated testing |
| QA-003 | Performance Tester | Load testing |
| QA-004 | Security Tester | DevSecOps |
| QA-005 | Manual QA Tester | Exploratory testing |
| QA-006 | Test Data Manager | Test data |

## Provides (Summary)

- Test strategies
- Automated tests
- Performance benchmarks
- Security scan results
- Quality metrics

## Interfaces (Summary)

- Development: test results, bug reports
- Security: security test findings
- Infrastructure: performance data

## Team Structure

```
                    ┌─────────────────┐
                    │   QA ARCHITECT  │
                    │  (Team Leader)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│     Test      │   │  Performance  │   │   Security    │
│  Automation   │   │    Tester     │   │    Tester     │
│   Engineer    │   │               │   │               │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                                         │
        ▼                                         ▼
┌───────────────┐                       ┌───────────────┐
│   Manual QA   │                       │   Test Data   │
│    Tester     │                       │    Manager    │
└───────────────┘                       └───────────────┘
```

## Agent Roster

| Agent | Role | Primary Responsibility |
|-------|------|------------------------|
| **QA Architect** | Team Leader | Test strategy, coverage, quality metrics |
| **Test Automation Engineer** | Automation | Test frameworks, automated suites, CI integration |
| **Performance Tester** | Performance | Load testing, bottleneck analysis, optimization |
| **Security Tester** | AppSec | SAST, DAST, security automation, DevSecOps |
| **Manual QA Tester** | Exploratory | Exploratory testing, edge cases, usability |
| **Test Data Manager** | Data | Test data generation, environments, fixtures |

## Team Capabilities

### Test Strategy
- Risk-based testing approach
- Coverage analysis
- Test planning
- Quality gates definition
- Metrics and reporting

### Test Automation
- UI test automation (Playwright, Cypress)
- API test automation
- CI/CD integration
- Test framework development
- Regression testing

### Performance Testing
- Load testing
- Stress testing
- Endurance testing
- Bottleneck identification
- Capacity planning support

### Security Testing
- Static analysis (SAST)
- Dynamic analysis (DAST)
- Dependency scanning
- Security regression
- DevSecOps integration

### Exploratory Testing
- Edge case discovery
- Usability evaluation
- Accessibility testing
- Cross-browser testing
- User flow validation

### Test Data Management
- Data generation
- Data masking
- Environment management
- Fixture maintenance
- Privacy compliance

## Interaction Patterns

### Testing Flow
```
Feature Ready for Test
         │
         ▼
┌────────────────────────────────────────────────────────────────┐
│ QA ARCHITECT                                                    │
│ • Defines test approach                                         │
│ • Identifies risks                                              │
│ • Assigns testing tasks                                         │
└──────────────────────────┬─────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ TEST AUTOMATION│ │ SECURITY       │ │ MANUAL QA      │
│ ENGINEER       │ │ TESTER         │ │ TESTER         │
│ • Automated    │ │ • SAST/DAST    │ │ • Exploratory  │
│   tests        │ │ • Security     │ │ • Edge cases   │
│ • Regression   │ │   scans        │ │ • Usability    │
└───────┬────────┘ └───────┬────────┘ └───────┬────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     ┌────────────────┐       ┌────────────────┐
     │ TEST DATA      │       │ PERFORMANCE    │
     │ MANAGER        │       │ TESTER         │
     │ • Provides     │       │ • Load tests   │
     │   test data    │       │ • Performance  │
     │ • Manages      │       │   validation   │
     │   environments │       │                │
     └────────────────┘       └────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │ RESULTS SUMMARY │
         │ → QA Architect  │
         └─────────────────┘
```

### Cross-Team Interactions

| External Team | Key Interactions |
|---------------|------------------|
| **Development** | Test coverage, bug reports, automation support |
| **Security** | Security testing coordination, findings validation |
| **Infrastructure** | Test environments, performance baselines |

## Communication Protocols

### Test Results Summary
```
SUMMARY: Test Execution Complete
FEATURE: [Feature name]
BUILD: [Build number]
STATUS: [PASS/FAIL]

RESULTS:
  - Total: [count]
  - Passed: [count]
  - Failed: [count]
  - Blocked: [count]

COVERAGE:
  - Unit: [%]
  - Integration: [%]
  - E2E: [%]

BLOCKERS: [List if any]
RECOMMENDATION: [Ready/Not Ready for release]
```

### Bug Report
```
BUG REPORT
ID: BUG-[NNN]
TITLE: [Brief description]
SEVERITY: [Critical/High/Medium/Low]
FOUND_BY: [Agent name]
TEST_TYPE: [Automated/Manual/Exploratory]

STEPS:
1. [Step 1]
2. [Step 2]

EXPECTED: [What should happen]
ACTUAL: [What happened]
EVIDENCE: [Screenshots, logs]
ENVIRONMENT: [Browser, OS, etc.]
```

### Test Environment Request
```
REQUEST: Test Environment
TYPE: [New/Refresh/Modify]
PURPOSE: [What testing needs it]
SPECS: [Requirements]
DATA: [Data requirements]
DURATION: [How long needed]
REQUESTER: [Agent name]
```

## Quality Gates

### PR Gate (Automated)
- [ ] Unit tests pass
- [ ] Code coverage > 80%
- [ ] Lint checks pass
- [ ] Security scan clean

### QA Gate (Feature Testing)
- [ ] Functional tests pass
- [ ] Regression tests pass
- [ ] Security tests pass
- [ ] Exploratory testing complete
- [ ] No critical/high bugs open

### Release Gate
- [ ] All test types pass
- [ ] Performance validated
- [ ] Security approved
- [ ] Accessibility verified
- [ ] Documentation complete
- [ ] Stakeholder sign-off

## Escalation Path

```
Test Failure / Bug Found
         │
         ▼
Triage by Finder
         │
         ├── Known Issue ──► Link & Track
         │
         ▼ (New Issue)
Bug Report Created
         │
         ├── Low Severity ──► Standard Queue
         │
         ▼ (High/Critical)
QA Architect Notified
         │
         ├── Test Issue ──► Fix Test
         │
         ▼ (Product Issue)
Development Team Notified
         │
         ▼ (Blocking Release)
Release Decision Required
```

## Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test Coverage | > 80% | Code coverage percentage |
| Automation Rate | > 70% | Automated / Total tests |
| Defect Escape Rate | < 5% | Prod bugs / Total bugs |
| Test Cycle Time | < 2 hours | Time for full regression |
| False Positive Rate | < 5% | Flaky tests / Total tests |

## Test Automation Pyramid

```
                    ┌─────────┐
                    │   E2E   │  10%
                    │  Tests  │  Playwright/Cypress
                   ─┴─────────┴─
                  ┌─────────────┐
                  │ Integration │  20%
                  │    Tests    │  API tests
                 ─┴─────────────┴─
                ┌─────────────────┐
                │    Unit Tests   │  70%
                │                 │  Jest/pytest
                └─────────────────┘
```

## Invocation

```bash
# Summon the QA Team
Task -> subagent_type: "qa-team"

# Individual agents
Task -> subagent_type: "qa-architect"
Task -> subagent_type: "test-automation-engineer"
Task -> subagent_type: "performance-tester"
Task -> subagent_type: "security-tester"
Task -> subagent_type: "manual-qa-tester"
Task -> subagent_type: "test-data-manager"
```
