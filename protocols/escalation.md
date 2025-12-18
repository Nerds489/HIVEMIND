# HIVEMIND Escalation Paths Protocol

## Overview

This protocol defines the escalation matrix for HIVEMIND, ensuring issues are routed to the appropriate authority level when they cannot be resolved at lower levels.

---

## Escalation Levels

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ESCALATION HIERARCHY                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Level 5: HUMAN OPERATOR
         │  Authority: Unlimited
         │  Timeout: Immediate notification
         │
Level 4: COORDINATOR
         │  Authority: Cross-system decisions
         │  Timeout: 1 hour
         │
Level 3: CROSS-TEAM COORDINATION
         │  Authority: Multi-team decisions
         │  Timeout: 30 minutes
         │
Level 2: TEAM LEAD
         │  Authority: Team-level decisions
         │  Timeout: 15 minutes
         │
Level 1: PEER ESCALATION
         │  Authority: Peer consultation
         │  Timeout: 5 minutes
         │
Level 0: SELF-RESOLUTION
         Agent attempts to resolve independently
```

---

## Level 1: Peer Escalation

**Definition:** Agent-to-agent escalation within the same team.

### Trigger Conditions
- Need expertise outside agent's primary domain
- Require second opinion on technical approach
- Workload balancing needed
- Time constraint with available peer capacity

### Resolution Expectations
- Peer provides guidance or takes over specific subtask
- Original agent retains ownership of overall task
- Knowledge transfer expected for future self-resolution

### Timeout: 5 minutes
If unresolved after 5 minutes, escalate to Level 2.

### Examples

**Development Team:**
```
DEV-002 (Backend) → DEV-003 (Frontend)
Reason: Need frontend input on API response format

DEV-003 (Frontend) → DEV-002 (Backend)
Reason: API endpoint not returning expected data

DEV-002/003 → DEV-004 (Code Reviewer)
Reason: Unclear if approach meets standards
```

**Security Team:**
```
SEC-002 (Pentest) → SEC-004 (Wireless)
Reason: Discovered WiFi-related attack vector

SEC-003 (Malware) → SEC-002 (Pentest)
Reason: Need to understand initial access vector
```

### Peer Escalation Message
```json
{
  "escalation_level": 1,
  "from": "DEV-002",
  "to": "DEV-003",
  "type": "peer_consultation",
  "task_id": "TASK-XXX",
  "question": "What format should the user profile API response use?",
  "context": "Implementing GET /users endpoint",
  "urgency": "blocking",
  "time_available": "5 minutes"
}
```

---

## Level 2: Team Lead Escalation

**Definition:** Agent escalates to their team's architect/lead.

### Team Leads
| Team | Lead Agent |
|------|------------|
| Development | DEV-001 (Architect) |
| Security | SEC-001 (Security Architect) |
| Infrastructure | INF-001 (Infrastructure Architect) |
| QA | QA-001 (QA Architect) |

### Trigger Conditions
- Peer escalation timeout exceeded
- Technical decision requiring architectural authority
- Resource conflict within team
- Quality gate decisions
- Risk assessment exceeding peer authority
- Requirement ambiguity needing interpretation

### Authority Granted
- Can make binding technical decisions for team
- Can reassign work within team
- Can approve exceptions to team standards
- Can authorize additional time/resources

### Timeout: 15 minutes
If unresolved after 15 minutes, escalate to Level 3.

### Examples

**To Architect (DEV-001):**
- API design decision with multiple valid approaches
- Technology selection for new component
- Technical debt prioritization
- Breaking change assessment

**To Security Architect (SEC-001):**
- Risk acceptance decisions
- Security control exceptions
- Threat severity classification disputes
- Incident severity determination

### Team Lead Escalation Message
```json
{
  "escalation_level": 2,
  "from": "DEV-002",
  "to": "DEV-001",
  "type": "team_lead_decision",
  "task_id": "TASK-XXX",
  "issue": "Cannot determine appropriate database schema design",
  "options_considered": [
    {"option": "Normalized schema", "pros": ["Data integrity"], "cons": ["Query complexity"]},
    {"option": "Denormalized schema", "pros": ["Read performance"], "cons": ["Data duplication"]}
  ],
  "recommendation": "Normalized schema",
  "blocker_since": "2024-01-15T10:00:00Z",
  "impact_if_delayed": "Feature delivery delayed by 2 days"
}
```

---

## Level 3: Cross-Team Escalation

**Definition:** Team lead escalates to another team lead for cross-team coordination.

### Trigger Conditions
- Decision requires input from multiple teams
- Resource or dependency conflict between teams
- Security or compliance issue affecting multiple teams
- Priority conflict between team objectives
- Incident affecting multiple domains

### Coordination Protocol
1. Initiating team lead contacts relevant team lead(s)
2. Shared context package exchanged
3. Joint decision made with documented rationale
4. Both teams implement agreed actions

### Timeout: 30 minutes
If unresolved after 30 minutes, escalate to Level 4.

### Common Cross-Team Escalations

| From | To | Common Reasons |
|------|-----|----------------|
| DEV-001 | SEC-001 | Security requirement clarification |
| DEV-001 | INF-001 | Infrastructure requirements |
| DEV-001 | QA-001 | Quality gate negotiation |
| SEC-001 | INF-001 | Security control implementation |
| SEC-001 | QA-001 | Security testing scope |
| INF-001 | QA-001 | Performance baseline disputes |

### Cross-Team Escalation Message
```json
{
  "escalation_level": 3,
  "from": "DEV-001",
  "to": ["SEC-001", "INF-001"],
  "type": "cross_team_coordination",
  "task_id": "TASK-XXX",
  "issue": "New authentication system requires coordinated design",
  "teams_affected": ["Development", "Security", "Infrastructure"],
  "decision_needed": "Token storage strategy",
  "options": [
    {"option": "Redis session store", "teams_support": ["DEV", "INFRA"], "teams_concern": ["SEC"]},
    {"option": "JWT stateless", "teams_support": ["SEC"], "teams_concern": ["DEV"]}
  ],
  "deadline": "2024-01-15T12:00:00Z",
  "impact": "Blocks authentication feature development"
}
```

---

## Level 4: Coordinator Escalation

**Definition:** Any agent or team lead escalates to the HIVEMIND COORDINATOR.

### Trigger Conditions
- Cross-team escalation timeout exceeded
- System-wide impact decisions
- Multiple teams in conflict
- Resource allocation across all teams
- Major architectural decisions affecting entire system
- Policy interpretation needed
- External communication required

### Authority Granted
- Can make binding decisions across all teams
- Can reprioritize work across HIVEMIND
- Can activate emergency protocols
- Can aggregate and report to human operators
- Can invoke any workflow

### Timeout: 1 hour
If unresolved after 1 hour, escalate to Level 5.

### Coordinator Escalation Message
```json
{
  "escalation_level": 4,
  "from": "DEV-001",
  "to": "COORDINATOR",
  "type": "coordinator_decision",
  "task_id": "TASK-XXX",
  "issue": "Major release blocked by unresolved cross-team conflicts",
  "context": {
    "teams_involved": ["Development", "Security", "QA"],
    "escalation_history": [
      {"level": 2, "time": "2024-01-15T10:00:00Z", "outcome": "Escalated to cross-team"},
      {"level": 3, "time": "2024-01-15T10:30:00Z", "outcome": "No consensus reached"}
    ],
    "blocking_issues": [
      "Security requires additional review time",
      "QA found critical bug requiring fix",
      "Business deadline is tomorrow"
    ]
  },
  "decision_options": [
    "Delay release by 1 week",
    "Release with known issue and hotfix plan",
    "Reduce scope and release partial feature"
  ],
  "recommendation": "Release with reduced scope",
  "urgency": "P1"
}
```

---

## Level 5: Human Escalation

**Definition:** COORDINATOR escalates to human operator.

### MUST Escalate Scenarios
These scenarios ALWAYS require human involvement:

1. **Security Breach Confirmed**
   - Active data exfiltration
   - Ransomware detected
   - Credentials compromised at scale

2. **Legal/Compliance Impact**
   - Regulatory violation discovered
   - Data breach notification required
   - Legal hold required

3. **Financial Impact**
   - Decisions affecting budget > $X
   - Contract implications
   - SLA breach with penalties

4. **External Communication**
   - Customer notification required
   - Public disclosure needed
   - Media/PR involvement

5. **System-Wide Outage**
   - Multiple critical systems down
   - Recovery time exceeding SLO
   - Data integrity in question

6. **Unresolved Conflict**
   - COORDINATOR cannot reach decision
   - Ethical ambiguity
   - Policy gap discovered

### Information Package for Human

```json
{
  "escalation_level": 5,
  "to": "HUMAN_OPERATOR",
  "escalation_id": "ESC-20240115-000001",
  "timestamp": "2024-01-15T12:00:00Z",

  "classification": "MUST_ESCALATE",
  "reason": "Security breach confirmed - ransomware detected",

  "summary": {
    "situation": "Ransomware detected on 3 production servers",
    "impact": "User data potentially encrypted, service degraded",
    "current_actions": "Systems isolated, investigation ongoing",
    "decision_required": "Authorize ransom negotiation or data recovery from backups"
  },

  "timeline": {
    "detected": "2024-01-15T11:30:00Z",
    "escalated_to_coordinator": "2024-01-15T11:45:00Z",
    "escalated_to_human": "2024-01-15T12:00:00Z"
  },

  "agents_involved": [
    {"id": "SEC-006", "role": "Incident Commander"},
    {"id": "INF-005", "role": "System Recovery"},
    {"id": "SEC-003", "role": "Malware Analysis"}
  ],

  "options_presented": [
    {
      "option": "Negotiate with attackers",
      "pros": ["Faster recovery possible"],
      "cons": ["No guarantee", "Funds criminal activity", "Legal implications"],
      "agent_recommendation": "Not recommended"
    },
    {
      "option": "Restore from backups",
      "pros": ["No ransom payment", "Known good state"],
      "cons": ["Data loss since last backup", "Extended downtime"],
      "agent_recommendation": "Recommended"
    }
  ],

  "attachments": [
    {"name": "Incident Report", "path": "/artifacts/incidents/INC-2024-001.md"},
    {"name": "Affected Systems", "path": "/artifacts/incidents/INC-2024-001-systems.json"}
  ],

  "response_required": {
    "deadline": "2024-01-15T14:00:00Z",
    "format": "Decision on recovery approach + authorization level"
  }
}
```

### Decision Recording
All human decisions must be recorded:

```json
{
  "decision_record": {
    "escalation_id": "ESC-20240115-000001",
    "decided_by": "Human Operator",
    "decided_at": "2024-01-15T13:00:00Z",
    "decision": "Proceed with backup restoration",
    "rationale": "Company policy prohibits ransom payments",
    "authorized_actions": [
      "Begin backup restoration procedure",
      "Notify affected users within 24 hours",
      "Engage external forensics team"
    ],
    "constraints": [
      "Maximum 48-hour restoration window",
      "Preserve evidence for law enforcement"
    ]
  }
}
```

---

## Escalation Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ESCALATION FLOW                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                              Issue Detected
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ L0: Self-Resolve│
                           │   (Agent)       │
                           └────────┬────────┘
                                    │
                        ┌───────────┴───────────┐
                        │                       │
                   Resolved              Not Resolved
                        │                       │
                        ▼                       ▼
                      Done              ┌─────────────────┐
                                        │ L1: Peer        │
                                        │   (5 min)       │
                                        └────────┬────────┘
                                                 │
                                     ┌───────────┴───────────┐
                                     │                       │
                                Resolved              Not Resolved
                                     │                       │
                                     ▼                       ▼
                                   Done              ┌─────────────────┐
                                                     │ L2: Team Lead   │
                                                     │   (15 min)      │
                                                     └────────┬────────┘
                                                              │
                                                  ┌───────────┴───────────┐
                                                  │                       │
                                             Resolved              Not Resolved
                                                  │                       │
                                                  ▼                       ▼
                                                Done              ┌─────────────────┐
                                                                  │ L3: Cross-Team  │
                                                                  │   (30 min)      │
                                                                  └────────┬────────┘
                                                                           │
                                                               ┌───────────┴───────────┐
                                                               │                       │
                                                          Resolved              Not Resolved
                                                               │                       │
                                                               ▼                       ▼
                                                             Done              ┌─────────────────┐
                                                                               │ L4: Coordinator │
                                                                               │   (1 hour)      │
                                                                               └────────┬────────┘
                                                                                        │
                                                                            ┌───────────┴───────────┐
                                                                            │                       │
                                                                       Resolved       MUST_ESCALATE
                                                                            │          or Timeout
                                                                            │                       │
                                                                            ▼                       ▼
                                                                          Done              ┌─────────────────┐
                                                                                            │ L5: Human       │
                                                                                            │   (Immediate)   │
                                                                                            └────────┬────────┘
                                                                                                     │
                                                                                                     ▼
                                                                                              Human Decision
                                                                                                     │
                                                                                                     ▼
                                                                                                   Done
```

---

## Escalation Metrics

Track these metrics to optimize escalation:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| L1 Resolution Rate | > 70% | < 50% |
| L2 Resolution Rate | > 80% | < 60% |
| L3 Resolution Rate | > 90% | < 70% |
| L4 Resolution Rate | > 95% | < 80% |
| Mean Time to Escalate | < 10 min | > 20 min |
| Escalation to Human Rate | < 5% | > 10% |

---

## De-escalation Protocol

When a higher level resolves an issue:
1. Document the resolution
2. Notify all involved agents
3. Update knowledge base for future self-resolution
4. Return ownership to appropriate level
5. Conduct brief retrospective for L3+ escalations
