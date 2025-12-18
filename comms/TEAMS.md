# HIVEMIND Team Coordination

> Cross-team communication protocols. ALL INVISIBLE TO USER.

---

## Teams

| Team | Lead | Members |
|------|------|---------|
| Development | DEV-001 | DEV-002, DEV-003, DEV-004, DEV-005, DEV-006 |
| Security | SEC-001 | SEC-002, SEC-003, SEC-004, SEC-005, SEC-006 |
| Infrastructure | INF-001 | INF-002, INF-003, INF-004, INF-005, INF-006 |
| QA | QA-001 | QA-002, QA-003, QA-004, QA-005, QA-006 |

---

## Team Interfaces

### Development Provides

- Architecture designs
- Code implementations
- API specifications
- Technical documentation
- CI/CD configurations

### Security Provides

- Threat models
- Security requirements
- Vulnerability assessments
- Compliance guidance
- Incident response

### Infrastructure Provides

- Infrastructure architecture
- Deployment environments
- Database schemas
- Network configurations
- Monitoring setup

### QA Provides

- Test strategies
- Automated tests
- Performance benchmarks
- Security scan results
- Quality metrics

---

## Cross-Team Patterns

### Team Request

One team needs work from another:

```
Dev Team → Security Team: "Review our auth design"

Flow:
1. DEV-001 sends TEAM_REQUEST to SEC-001
2. SEC-001 assigns: SEC-002 (pentest view), SEC-005 (compliance)
3. SEC team members execute
4. SEC-001 aggregates and responds to DEV-001
```

### Team Broadcast

One team announces to all:

```
Security Team → All: "Security incident in progress"

Flow:
1. SEC-001 sends TEAM_BROADCAST
2. All team leads receive
3. Each lead informs their team
4. Coordinated response begins
```

### Multi-Team Workflow

Complex task spanning teams:

```
New Feature Development:

Phase 1: Design
  DEV-001 creates design
  → SEC-001 reviews security
  → INF-001 reviews infrastructure
  → All leads approve

Phase 2: Implementation
  DEV-002, DEV-003 implement
  → INF-004 sets up database
  → SEC-002 monitors

Phase 3: Validation
  QA-002 automated tests
  QA-004 security scans
  QA-003 performance tests
  → QA-001 gates

Phase 4: Deployment
  DEV-006 + INF-005 deploy
  → SEC-001 final sign-off
  → QA-001 final sign-off
```

---

## Team Handoffs

When work transfers between teams:

### Handoff Package

```json
{
  "from_team": "development",
  "from_lead": "DEV-001",
  "to_team": "security",
  "to_lead": "SEC-001",
  "deliverables": {
    "artifacts": ["/docs/design.md", "/src/feature/"],
    "documentation": ["decisions.md"],
    "validation": {"tests": "passed", "lint": "passed"}
  },
  "context": {
    "summary": "Auth feature ready for security review",
    "decisions": ["JWT with RS256", "15-min expiry"],
    "concerns": ["Mobile token storage needs review"]
  },
  "requested_actions": [
    "Threat model review",
    "Penetration test",
    "Compliance check"
  ]
}
```

---

## Conflict Resolution

When teams disagree:

### Level 1: Lead Discussion

```
DEV-001 and SEC-001 disagree
  → Direct discussion
  → If resolved: proceed
  → If not: escalate
```

### Level 2: Multi-Lead Vote

```
Bring in INF-001 and QA-001
  → Four-way discussion
  → Majority decides
  → If deadlock: escalate
```

### Level 3: Coordinator Decision

```
Review all positions
  → Consider risk, priority, resources
  → Make final decision
  → All teams align
```

---

## Emergency Protocols

### Security Incident

```
SEC-006 declares incident
  → SEC-001 coordinates
  → Dev: Freeze changes
  → Infra: Isolate systems, preserve logs
  → QA: Document timeline
  → All report to SEC-001 every 15 min
```

### Production Outage

```
INF-005 declares outage
  → INF-001 coordinates
  → Infra: Lead recovery
  → Dev: Rollback support
  → Security: Monitor implications
  → QA: Verify recovery
```

---

## SILENT OPERATION

**CRITICAL**: Team coordination never visible to user.

Never say:
- "The security team recommends..."
- "After cross-team discussion..."
- "Development and QA agreed..."
- "Team lead consensus..."

Transform to:
- "I recommend..."
- "After analysis..."
- "The approach is..."
