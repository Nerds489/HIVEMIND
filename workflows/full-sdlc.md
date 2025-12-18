# Full SDLC Workflow

## Overview

This workflow orchestrates a complete Software Development Lifecycle from requirements to production deployment, coordinating all 4 teams and multiple agents.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FULL SDLC PIPELINE                                  │
│                                                                              │
│  DESIGN ──► IMPLEMENT ──► REVIEW ──► TEST ──► DEPLOY ──► VALIDATE          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Requirements & Design

### Duration: 1-3 days (varies by complexity)

### Agents Involved
- **DEV-001** (Architect) - Lead
- **SEC-001** (Security Architect)
- **QA-001** (QA Architect)
- **INF-001** (Infrastructure Architect) - if infrastructure changes needed

### Input
- Business requirements document
- User stories / acceptance criteria
- Existing system documentation
- Constraints (timeline, budget, technology)

### Activities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: DESIGN                                       │
└─────────────────────────────────────────────────────────────────────────────┘

DAY 1: Architecture Design
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-001 (Architect)                                                          │
│                                                                              │
│ Activities:                                                                  │
│ • Review business requirements                                               │
│ • Identify system components                                                 │
│ • Design API contracts                                                       │
│ • Create system diagrams                                                     │
│ • Document technology decisions                                              │
│                                                                              │
│ Outputs:                                                                     │
│ • Architecture Decision Record (ADR)                                         │
│ • System component diagram                                                   │
│ • API specification (OpenAPI)                                                │
│ • Data model design                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
DAY 2: Security & Infrastructure Review (Parallel)
┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│ SEC-001 (Security Architect)    │   │ INF-001 (Infrastructure Arch) │
│                                 │   │                                 │
│ Activities:                     │   │ Activities:                     │
│ • Create threat model           │   │ • Assess infrastructure needs   │
│ • Define security requirements  │   │ • Estimate resource requirements│
│ • Review API for security       │   │ • Identify deployment targets   │
│ • Identify compliance needs     │   │ • Plan scaling strategy         │
│                                 │   │                                 │
│ Outputs:                        │   │ Outputs:                        │
│ • Threat model document         │   │ • Infrastructure requirements   │
│ • Security requirements list    │   │ • Resource estimates            │
│ • Compliance checklist          │   │ • Environment specifications    │
└─────────────────────────────────┘   └─────────────────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
DAY 2-3: Test Strategy
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-001 (QA Architect)                                                        │
│                                                                              │
│ Activities:                                                                  │
│ • Define test strategy based on architecture                                 │
│ • Identify test levels (unit, integration, E2E)                              │
│ • Define quality gates                                                       │
│ • Plan test data requirements                                                │
│ • Estimate testing effort                                                    │
│                                                                              │
│ Outputs:                                                                     │
│ • Test strategy document                                                     │
│ • Test data requirements                                                     │
│ • Quality gate definitions                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quality Gate: Design Approval

**Required Approvers:**
- DEV-001 (Architect) ✓
- SEC-001 (Security Architect) ✓
- QA-001 (QA Architect) ✓
- INF-001 (if infrastructure changes) ✓

**Criteria:**
- [ ] Architecture documented and reviewed
- [ ] Security requirements defined
- [ ] Threat model complete
- [ ] Test strategy approved
- [ ] All open questions resolved
- [ ] Stakeholders signed off

---

## Phase 2: Implementation

### Duration: 1-2 weeks (varies by scope)

### Agents Involved
- **DEV-002** (Backend Developer)
- **DEV-003** (Frontend Developer)
- **DEV-005** (Technical Writer)
- **QA-006** (Test Data Manager)

### Input
- Approved design documents
- API specifications
- Security requirements
- Test strategy

### Activities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PHASE 2: IMPLEMENTATION                                 │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌───────────────────────────────────────────┐
                    │          PARALLEL EXECUTION               │
                    └───────────────────────────────────────────┘

TRACK A: Backend Development
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-002 (Backend Developer)                                                  │
│                                                                              │
│ Daily Activities:                                                            │
│ • Implement API endpoints per spec                                           │
│ • Create database models and migrations                                      │
│ • Write unit tests (80%+ coverage)                                           │
│ • Implement business logic                                                   │
│ • Integrate with external services                                           │
│                                                                              │
│ Daily Outputs:                                                               │
│ • Working code with tests                                                    │
│ • Updated API implementation                                                 │
│ • Migration files                                                            │
│ • Daily commit to feature branch                                             │
│                                                                              │
│ Handoffs:                                                                    │
│ • → DEV-003: API contracts for frontend integration                          │
│ • → DEV-004: Code ready for review (end of track)                            │
└─────────────────────────────────────────────────────────────────────────────┘

TRACK B: Frontend Development
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-003 (Frontend Developer)                                                 │
│                                                                              │
│ Daily Activities:                                                            │
│ • Implement UI components                                                    │
│ • Create state management                                                    │
│ • Integrate with backend APIs                                                │
│ • Write unit/component tests                                                 │
│ • Ensure accessibility compliance                                            │
│                                                                              │
│ Daily Outputs:                                                               │
│ • Working UI components                                                      │
│ • Component tests                                                            │
│ • API integration code                                                       │
│ • Daily commit to feature branch                                             │
│                                                                              │
│ Handoffs:                                                                    │
│ • ← DEV-002: Receives API implementation details                             │
│ • → DEV-004: Code ready for review (end of track)                            │
└─────────────────────────────────────────────────────────────────────────────┘

TRACK C: Documentation
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-005 (Technical Writer)                                                   │
│                                                                              │
│ Activities (ongoing):                                                        │
│ • Document API endpoints                                                     │
│ • Create user guides                                                         │
│ • Update architecture docs                                                   │
│ • Write integration guides                                                   │
│                                                                              │
│ Outputs:                                                                     │
│ • API documentation                                                          │
│ • User guides                                                                │
│ • Integration documentation                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

TRACK D: Test Data Preparation
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-006 (Test Data Manager)                                                   │
│                                                                              │
│ Activities:                                                                  │
│ • Generate test data sets                                                    │
│ • Prepare test environments                                                  │
│ • Create fixtures for automated tests                                        │
│                                                                              │
│ Outputs:                                                                     │
│ • Test data files                                                            │
│ • Environment configurations                                                 │
│ • Data generation scripts                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quality Gate: Feature Complete

**Criteria:**
- [ ] All planned features implemented
- [ ] Unit tests pass (80%+ coverage)
- [ ] Integration points working
- [ ] Documentation drafted
- [ ] Code committed to feature branch

---

## Phase 3: Code Review

### Duration: 1-2 days

### Agents Involved
- **DEV-004** (Code Reviewer) - Lead
- **QA-004** (Security Tester)

### Activities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 3: CODE REVIEW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: Automated Checks
┌─────────────────────────────────────────────────────────────────────────────┐
│ CI Pipeline (Automated)                                                      │
│                                                                              │
│ • Build verification                                                         │
│ • Unit test execution                                                        │
│ • Linting and formatting                                                     │
│ • SAST security scan                                                         │
│ • Dependency vulnerability scan                                              │
│                                                                              │
│ All must pass before human review                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
STEP 2: Code Review (Parallel Reviews)
┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│ DEV-004 (Code Reviewer)         │   │ QA-004 (Security Tester)        │
│                                 │   │                                 │
│ Focus:                          │   │ Focus:                          │
│ • Code quality                  │   │ • Security vulnerabilities      │
│ • Design patterns               │   │ • Input validation              │
│ • Maintainability               │   │ • Authentication/authorization  │
│ • Performance                   │   │ • Data protection               │
│ • Test coverage                 │   │ • OWASP Top 10                  │
│                                 │   │                                 │
│ Output:                         │   │ Output:                         │
│ • Review comments               │   │ • Security findings             │
│ • Approval/Changes requested    │   │ • Security approval/block       │
└─────────────────────────────────┘   └─────────────────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
STEP 3: Resolution (if needed)
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-002 + DEV-003                                                            │
│                                                                              │
│ • Address review feedback                                                    │
│ • Fix security findings                                                      │
│ • Update tests                                                               │
│ • Re-submit for review                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quality Gate: Code Review Passed

**Required Approvers:**
- DEV-004 (Code Reviewer) ✓
- QA-004 (Security Tester) ✓

**Criteria:**
- [ ] All automated checks pass
- [ ] No critical/high code review findings open
- [ ] No critical/high security findings open
- [ ] Test coverage maintained/improved
- [ ] Documentation reviewed

---

## Phase 4: Testing

### Duration: 2-5 days

### Agents Involved
- **QA-002** (Test Automation Engineer)
- **QA-003** (Performance Tester)
- **QA-004** (Security Tester)
- **QA-005** (Manual QA Tester)

### Activities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 4: TESTING                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌───────────────────────────────────────────┐
                    │          PARALLEL TEST EXECUTION          │
                    └───────────────────────────────────────────┘

TRACK A: Functional Testing
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-002 (Test Automation Engineer)                                            │
│                                                                              │
│ Activities:                                                                  │
│ • Execute automated test suites                                              │
│ • Run integration tests                                                      │
│ • Execute E2E tests                                                          │
│ • Analyze test results                                                       │
│ • Report failures                                                            │
│                                                                              │
│ Outputs:                                                                     │
│ • Test execution report                                                      │
│ • Bug tickets for failures                                                   │
│ • Coverage report                                                            │
└─────────────────────────────────────────────────────────────────────────────┘

TRACK B: Performance Testing
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-003 (Performance Tester)                                                  │
│                                                                              │
│ Activities:                                                                  │
│ • Execute load tests                                                         │
│ • Run stress tests                                                           │
│ • Identify bottlenecks                                                       │
│ • Compare against baselines                                                  │
│                                                                              │
│ Outputs:                                                                     │
│ • Performance test report                                                    │
│ • Bottleneck analysis                                                        │
│ • Performance recommendations                                                │
└─────────────────────────────────────────────────────────────────────────────┘

TRACK C: Security Testing
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-004 (Security Tester)                                                     │
│                                                                              │
│ Activities:                                                                  │
│ • Run DAST scans                                                             │
│ • Execute security regression tests                                          │
│ • Validate security fixes                                                    │
│ • Check compliance                                                           │
│                                                                              │
│ Outputs:                                                                     │
│ • Security test report                                                       │
│ • Vulnerability findings                                                     │
│ • Compliance status                                                          │
└─────────────────────────────────────────────────────────────────────────────┘

TRACK D: Exploratory Testing
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-005 (Manual QA Tester)                                                    │
│                                                                              │
│ Activities:                                                                  │
│ • Exploratory testing sessions                                               │
│ • Edge case discovery                                                        │
│ • Usability evaluation                                                       │
│ • Accessibility testing                                                      │
│                                                                              │
│ Outputs:                                                                     │
│ • Session notes                                                              │
│ • Bug reports                                                                │
│ • Usability findings                                                         │
└─────────────────────────────────────────────────────────────────────────────┘

                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
TEST RESULTS AGGREGATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-001 (QA Architect)                                                        │
│                                                                              │
│ • Aggregate all test results                                                 │
│ • Assess overall quality                                                     │
│ • Prioritize bug fixes                                                       │
│ • Make release recommendation                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quality Gate: QA Approved

**Required Approvers:**
- QA-001 (QA Architect) ✓

**Criteria:**
- [ ] All P0/P1 bugs resolved
- [ ] Test pass rate > 95%
- [ ] Performance meets baselines
- [ ] No critical security findings
- [ ] Accessibility requirements met

---

## Phase 5: Deployment

### Duration: 1-2 days

### Agents Involved
- **DEV-006** (DevOps Liaison) - Lead
- **INF-005** (SRE)
- **INF-001** (Infrastructure Architect)

### Activities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 5: DEPLOYMENT                                   │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: Pre-Deployment
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-006 (DevOps Liaison) + INF-005 (SRE)                                   │
│                                                                              │
│ Activities:                                                                  │
│ • Prepare deployment artifacts                                               │
│ • Update deployment configurations                                           │
│ • Verify target environment                                                  │
│ • Run deployment dry-run                                                     │
│ • Prepare rollback procedure                                                 │
│ • Notify stakeholders                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
STEP 2: Staging Deployment
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-006 (DevOps Liaison)                                                     │
│                                                                              │
│ Activities:                                                                  │
│ • Deploy to staging environment                                              │
│ • Run smoke tests                                                            │
│ • Verify functionality                                                       │
│ • Get final approval                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
STEP 3: Production Deployment
┌─────────────────────────────────────────────────────────────────────────────┐
│ DEV-006 (DevOps Liaison) + INF-005 (SRE)                                   │
│                                                                              │
│ Activities:                                                                  │
│ • Execute deployment to production                                           │
│ • Monitor deployment progress                                                │
│ • Run smoke tests                                                            │
│ • Verify health checks                                                       │
│ • Monitor error rates                                                        │
│ • Stand by for rollback if needed                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quality Gate: Deployment Complete

**Criteria:**
- [ ] Deployment successful
- [ ] Health checks passing
- [ ] Error rates normal
- [ ] Performance acceptable
- [ ] No rollback triggered

---

## Phase 6: Production Validation

### Duration: 1 day

### Agents Involved
- **QA-001** (QA Architect)
- **SEC-001** (Security Architect)
- **INF-005** (SRE)

### Activities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 6: PRODUCTION VALIDATION                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│ QA-001 (QA Architect)           │   │ INF-005 (SRE)                 │
│                                 │   │                                 │
│ Activities:                     │   │ Activities:                     │
│ • Verify production behavior    │   │ • Monitor system metrics        │
│ • Spot-check functionality      │   │ • Verify SLOs are met           │
│ • Confirm user acceptance       │   │ • Check alerting                │
│                                 │   │ • Validate monitoring           │
│ Output:                         │   │                                 │
│ • Production sign-off           │   │ Output:                         │
│                                 │   │ • Operations sign-off           │
└─────────────────────────────────┘   └─────────────────────────────────┘

                ┌─────────────────────────────────────────┐
                │ SEC-001 (Security Architect)            │
                │                                         │
                │ Activities:                             │
                │ • Verify security controls active       │
                │ • Confirm audit logging working         │
                │ • Validate access controls              │
                │                                         │
                │ Output:                                 │
                │ • Security sign-off                     │
                └─────────────────────────────────────────┘
```

### Final Quality Gate: Go-Live Approved

**Required Approvers:**
- QA-001 (QA Architect) ✓
- SEC-001 (Security Architect) ✓
- INF-005 (SRE) ✓

**Criteria:**
- [ ] Production functioning correctly
- [ ] SLOs being met
- [ ] Security controls verified
- [ ] Monitoring active
- [ ] No critical issues

---

## Rollback Procedures

### Trigger Conditions
- Error rate > 5% (sustained 10 minutes)
- P0 bug discovered in production
- Security vulnerability actively exploited
- Performance degradation > 50%

### Rollback Process
1. **Decide:** SRE or DevOps makes call
2. **Execute:** Deploy previous version
3. **Verify:** Confirm rollback successful
4. **Communicate:** Notify stakeholders
5. **Investigate:** Root cause analysis
6. **Fix:** Address issues
7. **Re-deploy:** When ready

---

## Escalation Triggers

| Phase | Trigger | Escalate To |
|-------|---------|-------------|
| Design | Unresolved architecture conflict | DEV-001 |
| Implementation | Blocked > 4 hours | DEV-001 |
| Code Review | Security finding dispute | SEC-001 |
| Testing | P0 bug disagreement | QA-001 |
| Deployment | Rollback decision | INF-005 + DEV-001 |
| Validation | Go-live dispute | All team leads |

---

## Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Design | 1-3 days | 1-3 days |
| Implementation | 5-10 days | 6-13 days |
| Code Review | 1-2 days | 7-15 days |
| Testing | 2-5 days | 9-20 days |
| Deployment | 1-2 days | 10-22 days |
| Validation | 1 day | 11-23 days |

**Typical Sprint:** 2-3 weeks for medium feature

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
