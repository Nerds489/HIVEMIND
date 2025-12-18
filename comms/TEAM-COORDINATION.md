# HIVEMIND Team Coordination

> Cross-team communication and collaboration protocols.
> **ALL COORDINATION IS INVISIBLE TO USER** - See runtime/OUTPUT-FILTER.md

---

## Team Structure

### Team Leads

| Team | Lead Agent | Role |
|------|------------|------|
| **Development** | DEV-001 (Architect) | Technical decisions, design authority |
| **Security** | SEC-001 (Security Architect) | Security decisions, risk authority |
| **Infrastructure** | INF-001 (Infrastructure Architect) | Infrastructure decisions, capacity authority |
| **QA** | QA-001 (QA Architect) | Quality decisions, release authority |

Team leads are automatically included in cross-team communications.

---

## Team Interfaces

### What Each Team Provides

```yaml
Development Team:
  provides:
    - Architecture designs and decisions
    - Code implementations
    - API specifications
    - Technical documentation
    - CI/CD pipeline configurations
  requires_from:
    security: [threat models, security requirements, vulnerability assessments]
    infrastructure: [deployment targets, database schemas, capacity plans]
    qa: [test results, quality gates, bug reports]

Security Team:
  provides:
    - Threat models and risk assessments
    - Security requirements and controls
    - Vulnerability assessments
    - Compliance guidance
    - Incident response coordination
    - Penetration test results
  requires_from:
    development: [architecture docs, code for review, API specs]
    infrastructure: [network diagrams, access controls, logs]
    qa: [security test results, scan reports]

Infrastructure Team:
  provides:
    - Infrastructure architecture
    - Deployment environments
    - Database schemas and optimization
    - Network configurations
    - Monitoring and alerting
    - Capacity planning
  requires_from:
    development: [resource requirements, deployment artifacts]
    security: [hardening requirements, access policies]
    qa: [performance baselines, environment needs]

QA Team:
  provides:
    - Test strategies and plans
    - Automated test suites
    - Manual test results
    - Performance benchmarks
    - Security scan results
    - Quality metrics and gates
  requires_from:
    development: [code changes, feature specs, test requirements]
    security: [security test cases, compliance checklists]
    infrastructure: [test environments, data sets]
```

---

## Cross-Team Communication Patterns

### Pattern 1: Team Lead Sync

For strategic decisions requiring multiple team perspectives.

```
DEV-001 initiates:
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                    TEAM LEAD SYNC                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  DEV-001 ◄────────────────────────► SEC-001             │
│     ▲                                   ▲                │
│     │                                   │                │
│     │                                   │                │
│     ▼                                   ▼                │
│  QA-001 ◄────────────────────────► INF-001              │
│                                                          │
└─────────────────────────────────────────────────────────┘
         │
         ▼
   [Consensus decision]
```

**Message Format:**
```json
{
  "type": "TEAM_LEAD_SYNC",
  "initiator": "DEV-001",
  "topic": "New authentication system architecture",
  "participants": ["DEV-001", "SEC-001", "INF-001", "QA-001"],
  "questions": [
    "Security: What auth mechanisms are approved?",
    "Infrastructure: What are our scaling constraints?",
    "QA: What testing coverage do we need?"
  ],
  "deadline": "2025-12-18T12:00:00Z"
}
```

### Pattern 2: Team-to-Team Request

One team needs deliverables from another.

```
Development → Security: "Review our authentication design"
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│ DEV-001 sends team request to SEC-001                   │
│                                                          │
│ SEC-001 assigns:                                         │
│   - SEC-002 for penetration testing perspective         │
│   - SEC-005 for compliance perspective                   │
│                                                          │
│ SEC-001 aggregates and responds to DEV-001              │
└─────────────────────────────────────────────────────────┘
```

**Message Format:**
```json
{
  "type": "TEAM_REQUEST",
  "from_team": "development",
  "from_lead": "DEV-001",
  "to_team": "security",
  "to_lead": "SEC-001",
  "request": {
    "type": "security_review",
    "subject": "Authentication system design",
    "artifacts": ["/docs/auth-design.md", "/src/auth/"],
    "aspects_needed": ["threat model", "compliance check", "vulnerability assessment"]
  },
  "priority": "P2",
  "deadline": "2025-12-19T18:00:00Z"
}
```

### Pattern 3: Team Broadcast

One team announces to all teams.

```
Security Team detects incident:
         │
         ▼
SEC-001 ──TEAM_BROADCAST──> DEV-001, INF-001, QA-001
                               │
                               ▼
                    [Each lead informs their team]
```

**Message Format:**
```json
{
  "type": "TEAM_BROADCAST",
  "from_team": "security",
  "from_lead": "SEC-001",
  "to_teams": ["development", "infrastructure", "qa"],
  "priority": "P0",
  "content": {
    "alert": "Security incident in progress",
    "impact": "All deployments paused",
    "action_required": {
      "development": "Freeze all merges",
      "infrastructure": "Enable enhanced logging",
      "qa": "Pause automated tests"
    }
  }
}
```

### Pattern 4: Cross-Team Workflow

Multiple teams collaborate on complex deliverable.

```
New Feature Development:

Phase 1: Design
┌──────────────────────────────────────────────────────────────┐
│ DEV-001 creates design                                        │
│    │                                                          │
│    ├──> SEC-001 reviews security aspects                     │
│    │                                                          │
│    └──> INF-001 reviews infrastructure needs                 │
│                                                               │
│    [Design approved by all leads]                            │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 2: Implementation
┌──────────────────────────────────────────────────────────────┐
│ DEV-002, DEV-003 implement                                    │
│    │                                                          │
│    └──> INF-004 sets up database                             │
│                                                               │
│ SEC-002 monitors for security issues                         │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 3: Validation
┌──────────────────────────────────────────────────────────────┐
│ QA-002 runs automated tests                                   │
│ QA-004 runs security scans                                    │
│ QA-003 runs performance tests                                 │
│                                                               │
│ QA-001 aggregates and gates                                  │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 4: Deployment
┌──────────────────────────────────────────────────────────────┐
│ DEV-006 + INF-005 coordinate deployment                      │
│ SEC-001 final security sign-off                              │
│ QA-001 final quality sign-off                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Team Handoff Protocol

When work transfers between teams:

### Pre-Handoff (Source Team)

```
Source team lead (e.g., DEV-001) prepares:
1. Complete deliverables per team interface
2. Document decisions made
3. List assumptions
4. Identify risks and concerns
5. Create handoff package
```

### Handoff Package

```json
{
  "handoff_id": "TH-DEV-SEC-20251218-001",
  "from_team": "development",
  "from_lead": "DEV-001",
  "to_team": "security",
  "to_lead": "SEC-001",

  "deliverables": {
    "artifacts": [
      {"name": "Architecture Design", "path": "/docs/arch.md"},
      {"name": "API Specification", "path": "/docs/api.yaml"},
      {"name": "Source Code", "path": "/src/feature/"}
    ],
    "documentation": ["decisions.md", "assumptions.md"],
    "validation_status": {
      "unit_tests": "passed",
      "lint": "passed",
      "build": "passed"
    }
  },

  "context": {
    "summary": "Authentication feature ready for security review",
    "decisions_made": ["Using JWT with RS256", "15-minute token expiry"],
    "assumptions": ["Database schema finalized", "Network policies in place"],
    "concerns": ["Token storage on mobile clients needs review"],
    "timeline": "Security review needed by Dec 20"
  },

  "requested_actions": [
    "Threat model review",
    "Penetration test of auth endpoints",
    "Compliance check for PCI-DSS"
  ]
}
```

### Post-Handoff (Receiving Team)

```
Receiving team lead (e.g., SEC-001):
1. Acknowledge receipt
2. Assign team members to tasks
3. Request clarification if needed
4. Provide estimated completion
5. Execute and report back
```

---

## Conflict Resolution

When teams disagree:

### Level 1: Team Lead Discussion

```
DEV-001 and SEC-001 disagree on approach
         │
         ▼
Direct discussion between leads
         │
         ├── Agreement reached → Proceed
         │
         └── No agreement → Escalate to Level 2
```

### Level 2: Multi-Lead Arbitration

```
Bring in INF-001 and QA-001 for perspective
         │
         ▼
Four-way discussion
         │
         ├── Majority consensus → Proceed
         │
         └── Deadlock → Escalate to Level 3
```

### Level 3: COORDINATOR Decision

```
COORDINATOR reviews:
- All team positions
- Risk assessment
- Priority alignment
- Resource constraints
         │
         ▼
COORDINATOR makes final decision
         │
         ▼
All teams align
```

### Resolution Record

```json
{
  "conflict_id": "CONF-001",
  "timestamp": "2025-12-18T10:00:00Z",
  "parties": ["DEV-001", "SEC-001"],
  "topic": "Token expiration duration",
  "positions": {
    "DEV-001": "30-minute tokens for better UX",
    "SEC-001": "5-minute tokens for security"
  },
  "resolution": "15-minute tokens with refresh",
  "resolved_by": "Team lead consensus",
  "rationale": "Balance security and usability"
}
```

---

## Team Metrics

### Cross-Team Health Indicators

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Handoff acceptance rate | >95% | <90% |
| Avg handoff response time | <2 hours | >4 hours |
| Cross-team blockers | <2 active | >5 active |
| Conflict escalation rate | <5% | >10% |
| Team sync attendance | 100% | <75% |

---

## Emergency Protocols

### Incident Response (All Teams)

When SEC-006 declares incident:

```
SEC-001 assumes coordination
         │
         ▼
┌────────────────────────────────────────────────────────┐
│ Development: Freeze changes, provide system access     │
│ Security: Lead investigation and containment           │
│ Infrastructure: Isolate systems, preserve logs         │
│ QA: Document timeline, assist with verification        │
└────────────────────────────────────────────────────────┘
         │
         ▼
All teams report to SEC-001 every 15 minutes
```

### Production Outage (All Teams)

When INF-005 declares outage:

```
INF-001 assumes coordination
         │
         ▼
┌────────────────────────────────────────────────────────┐
│ Infrastructure: Lead recovery                          │
│ Development: Provide code expertise, rollback support  │
│ Security: Monitor for security implications            │
│ QA: Verify recovery, regression testing                │
└────────────────────────────────────────────────────────┘
```

---

## Integration Notes

### With Message Bus

Team-level messages route through MESSAGE-BUS.md with:
- Team lead CC on all cross-team messages
- Priority inheritance from team-level priority

### With Spawn Protocol

Cross-team requests may trigger spawning:
- Team lead always spawned first
- Lead decides which team members to spawn

### With Output Filter

**CRITICAL**: All team coordination is internal.
Never output:
- "The security team recommends..."
- "After cross-team discussion..."
- "Development and QA agreed..."
- Any reference to team structure

Transform to:
- "I recommend..." (synthesized from teams)
- "After analysis..."
- "The approach will be..."
