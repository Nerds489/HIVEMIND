# Full SDLC Pipeline Command

Activates the **Full Software Development Lifecycle Pipeline** coordinating all teams for end-to-end delivery.

## Pipeline Overview

```
DESIGN → IMPLEMENT → REVIEW → TEST → DEPLOY → VALIDATE
```

## Phase Details

### Phase 1: Design
**Lead:** DEV-001 (Architect)
- Requirements analysis
- Architecture design
- Technical specification
- Security design (SEC-001)
- Infrastructure planning (INF-001)

### Phase 2: Implement
**Lead:** DEV-002/DEV-003 (Developers)
- Backend development
- Frontend development
- Unit test creation
- Documentation (DEV-005)
- CI/CD setup (DEV-006)

### Phase 3: Review
**Lead:** DEV-004 (Code Reviewer)
- Code review
- Security review (QA-004)
- Architecture validation (DEV-001)

### Phase 4: Test
**Lead:** QA-001 (QA Architect)
- Test automation (QA-002)
- Performance testing (QA-003)
- Security testing (QA-004)
- Manual QA (QA-005)
- Test data (QA-006)

### Phase 5: Deploy
**Lead:** INF-005 (SRE)
- Environment preparation (INF-002)
- Database migrations (INF-004)
- Deployment execution
- Monitoring setup

### Phase 6: Validate
**Lead:** QA-001 (QA Architect)
- Production validation
- User acceptance
- Performance monitoring
- Incident readiness

## Quality Gates

Each phase must pass quality gates before proceeding:

- **Design Gate:** Architecture approved, security reviewed
- **Code Gate:** All tests pass, coverage ≥80%
- **Review Gate:** Code review approved, no blocking issues
- **Test Gate:** All tests pass, no P0/P1 bugs
- **Deploy Gate:** QA, INFRA, SEC all approve
- **Release Gate:** Production metrics healthy

## Load Full Workflow

For complete workflow details:
`/workflows/full-sdlc.md`

---

**Project/Feature:** $ARGUMENTS
