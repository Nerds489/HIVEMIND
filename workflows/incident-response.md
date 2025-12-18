# Incident Response Workflow

## Overview

This workflow coordinates emergency response to security incidents, system outages, and other critical events requiring immediate multi-team collaboration.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INCIDENT RESPONSE WORKFLOW                                │
│                                                                              │
│  DETECT ──► TRIAGE ──► CONTAIN ──► INVESTIGATE ──► ERADICATE ──► RECOVER   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Trigger Conditions

### Automatic Triggers
- Security alert threshold exceeded (SIEM)
- System availability below SLO for 5+ minutes
- Error rate > 5% for 10+ minutes
- Authentication failure spike (100+ in 5 min)

### Manual Triggers
- External threat notification
- User-reported breach
- Media inquiry about security
- Regulatory notification

---

## Phase 1: Detection & Triage (0-15 min)

### Lead Agent: SEC-006 (Incident Responder)
### Support: INF-005 (SRE), SEC-001 (Security Architect)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: DETECTION & TRIAGE                               │
│                    Timeline: 0-15 minutes                                    │
└─────────────────────────────────────────────────────────────────────────────┘

MINUTE 0-5: Alert Validation
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEC-006 (Incident Responder) + INF-005 (SRE)                               │
│                                                                              │
│ Activities:                                                                  │
│ • Receive and acknowledge alert                                              │
│ • Validate alert is not false positive                                       │
│ • Gather initial evidence                                                    │
│ • Assess initial scope                                                       │
│                                                                              │
│ Questions to Answer:                                                         │
│ • Is this a real incident?                                                   │
│ • What systems are affected?                                                 │
│ • Is the threat active?                                                      │
│ • What is the immediate impact?                                              │
└─────────────────────────────────────────────────────────────────────────────┘

MINUTE 5-10: Severity Classification
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEC-006 (Incident Responder)                                                 │
│                                                                              │
│ Severity Matrix:                                                             │
│                                                                              │
│ SEV1 (Critical):                                                             │
│ • Active data breach                                                         │
│ • Ransomware execution                                                       │
│ • Complete service outage                                                    │
│ • Credential compromise (admin/root)                                         │
│                                                                              │
│ SEV2 (High):                                                                 │
│ • Confirmed intrusion (not yet breach)                                       │
│ • Major feature unavailable                                                  │
│ • Vulnerability actively exploited                                           │
│ • >10% users affected                                                        │
│                                                                              │
│ SEV3 (Medium):                                                               │
│ • Security issue confirmed (not exploited)                                   │
│ • Partial service degradation                                                │
│ • <10% users affected                                                        │
│ • Workaround available                                                       │
│                                                                              │
│ SEV4 (Low):                                                                  │
│ • Suspicious activity (unconfirmed)                                          │
│ • Minor degradation                                                          │
│ • Minimal impact                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

MINUTE 10-15: Incident Declaration
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEC-006 (Incident Responder)                                                 │
│                                                                              │
│ Activities:                                                                  │
│ • Declare incident with severity                                             │
│ • Assign incident ID: INC-YYYY-NNN                                           │
│ • Open incident communication channel                                        │
│ • Notify required teams based on severity                                    │
│ • Begin incident timeline documentation                                      │
│                                                                              │
│ Notification Matrix:                                                         │
│                                                                              │
│ SEV1: All teams + Executives + Human operator                                │
│ SEV2: Security + Infrastructure + affected teams                             │
│ SEV3: Security + relevant team                                               │
│ SEV4: Security team only                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Incident Declaration Message
```json
{
  "incident_declaration": {
    "incident_id": "INC-2024-0042",
    "declared_at": "2024-01-15T10:15:00Z",
    "declared_by": "SEC-006",
    "severity": "SEV1",
    "type": "security_breach",

    "summary": "Unauthorized access detected to production database server",

    "initial_assessment": {
      "affected_systems": ["db-prod-01", "api-prod-01"],
      "affected_users": "Potentially all users",
      "threat_status": "Active",
      "data_at_risk": "User PII"
    },

    "response_team": {
      "incident_commander": "SEC-006",
      "technical_lead": "INF-005",
      "security_lead": "SEC-001"
    },

    "communication_channel": "#inc-2024-0042",
    "next_update": "2024-01-15T10:30:00Z"
  }
}
```

---

## Phase 2: Containment (15-60 min)

### Lead Agent: SEC-006 (Incident Responder)
### Support: INF-005 (SRE), INF-003 (Network Engineer), INF-002 (Systems Admin)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PHASE 2: CONTAINMENT                                    │
│                      Timeline: 15-60 minutes                                 │
└─────────────────────────────────────────────────────────────────────────────┘

PARALLEL CONTAINMENT ACTIONS
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐ │
│  │ INF-005 (SRE)    │    │ INF-003 (Network)│    │ INF-002 (SysAd) │ │
│  │                    │    │                    │    │                    │ │
│  │ • Isolate systems  │    │ • Block IPs        │    │ • Disable accounts │ │
│  │ • Preserve logs    │    │ • Segment network  │    │ • Stop services    │ │
│  │ • Capture state    │    │ • Enable logging   │    │ • Preserve evidence│ │
│  └────────────────────┘    └────────────────────┘    └────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

CONTAINMENT DECISION TREE
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                    Is threat actively spreading?                             │
│                              │                                               │
│               ┌──────────────┴──────────────┐                                │
│               │                             │                                │
│              YES                           NO                                │
│               │                             │                                │
│               ▼                             ▼                                │
│     AGGRESSIVE CONTAINMENT          SURGICAL CONTAINMENT                     │
│     • Isolate entire segment        • Target specific systems                │
│     • Kill all sessions             • Disable specific accounts              │
│     • Block all external            • Block specific IPs                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

EVIDENCE PRESERVATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEC-006 (Incident Responder) + INF-005 (SRE)                               │
│                                                                              │
│ CRITICAL: Preserve before remediation!                                       │
│                                                                              │
│ • Memory dumps of affected systems                                           │
│ • Disk images (or snapshots)                                                 │
│ • Network traffic captures                                                   │
│ • Log files (all relevant)                                                   │
│ • Process lists and network connections                                      │
│                                                                              │
│ Chain of Custody:                                                            │
│ • Document who collected what and when                                       │
│ • Hash all evidence files                                                    │
│ • Store in secure, isolated location                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Containment Status Update
```json
{
  "status_update": {
    "incident_id": "INC-2024-0042",
    "timestamp": "2024-01-15T10:45:00Z",
    "phase": "containment",
    "status": "in_progress",

    "actions_taken": [
      "Isolated db-prod-01 from network",
      "Blocked 15 suspicious IP addresses",
      "Disabled compromised service account",
      "Captured memory dump and disk snapshot"
    ],

    "current_scope": {
      "systems_affected": 2,
      "systems_isolated": 2,
      "threat_status": "Contained but not eradicated"
    },

    "next_steps": [
      "Complete forensic imaging",
      "Begin root cause analysis",
      "Prepare for eradication"
    ],

    "next_update": "2024-01-15T11:00:00Z"
  }
}
```

---

## Phase 3: Investigation (1-24 hours)

### Lead Agent: SEC-003 (Malware Analyst) for malware incidents, SEC-006 for others
### Support: Full Security Team

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PHASE 3: INVESTIGATION                                   │
│                     Timeline: 1-24 hours                                     │
└─────────────────────────────────────────────────────────────────────────────┘

INVESTIGATION TRACKS (Parallel)
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  TRACK A: Timeline Reconstruction                                            │
│  Lead: SEC-006                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ • Correlate logs across systems                                       │   │
│  │ • Identify initial access time                                        │   │
│  │ • Map attacker activities                                             │   │
│  │ • Determine scope of access                                           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  TRACK B: Malware Analysis (if applicable)                                   │
│  Lead: SEC-003                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ • Analyze malicious code                                              │   │
│  │ • Extract IOCs                                                        │   │
│  │ • Determine capabilities                                              │   │
│  │ • Create detection rules                                              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  TRACK C: Impact Assessment                                                  │
│  Lead: SEC-001                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ • Identify accessed data                                              │   │
│  │ • Assess data exfiltration                                            │   │
│  │ • Evaluate compliance impact                                          │   │
│  │ • Determine notification requirements                                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

ROOT CAUSE ANALYSIS
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEC-001 (Security Architect)                                                 │
│                                                                              │
│ Questions to Answer:                                                         │
│ • How did the attacker gain initial access?                                  │
│ • What vulnerability or weakness was exploited?                              │
│ • How did they move laterally?                                               │
│ • What persistence mechanisms were used?                                     │
│ • Why wasn't this detected earlier?                                          │
│                                                                              │
│ Output: Root Cause Analysis Document                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Eradication (Variable)

### Lead Agent: SEC-001 (Security Architect)
### Support: INF-002 (Systems Admin), DEV-002 (if code fix needed)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PHASE 4: ERADICATION                                    │
│                      Timeline: Variable                                      │
└─────────────────────────────────────────────────────────────────────────────┘

ERADICATION ACTIONS
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│ 1. REMOVE THREAT                                                             │
│    • Remove malware/backdoors                                                │
│    • Delete unauthorized accounts                                            │
│    • Remove persistence mechanisms                                           │
│    • Clean compromised systems (or rebuild)                                  │
│                                                                              │
│ 2. CLOSE VULNERABILITY                                                       │
│    • Patch exploited vulnerability                                           │
│    • Fix configuration issues                                                │
│    • Update security controls                                                │
│    • Strengthen authentication                                               │
│                                                                              │
│ 3. CREDENTIAL RESET                                                          │
│    • Reset all potentially compromised passwords                             │
│    • Rotate all potentially compromised keys                                 │
│    • Revoke all potentially compromised tokens                               │
│    • Review access permissions                                               │
│                                                                              │
│ 4. VERIFICATION                                                              │
│    • Scan for remaining threats                                              │
│    • Verify fixes are effective                                              │
│    • Test security controls                                                  │
│    • Confirm clean state                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 5: Recovery (Variable)

### Lead Agent: INF-005 (SRE)
### Support: All Infrastructure Team, DEV-006 (DevOps)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 5: RECOVERY                                     │
│                        Timeline: Variable                                    │
└─────────────────────────────────────────────────────────────────────────────┘

RECOVERY PROCESS
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│ STEP 1: System Restoration                                                   │
│ ┌──────────────────────────────────────────────────────────────────────┐    │
│ │ • Rebuild compromised systems from known-good images                  │    │
│ │ • Restore data from verified clean backups                            │    │
│ │ • Apply all security patches                                          │    │
│ │ • Implement additional security controls                              │    │
│ └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│ STEP 2: Validation                                                           │
│ ┌──────────────────────────────────────────────────────────────────────┐    │
│ │ • Security scan of restored systems                                   │    │
│ │ • Functionality testing                                               │    │
│ │ • Performance validation                                              │    │
│ │ • Security control verification                                       │    │
│ └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│ STEP 3: Gradual Service Restoration                                          │
│ ┌──────────────────────────────────────────────────────────────────────┐    │
│ │ • Restore internal services first                                     │    │
│ │ • Enable external access in stages                                    │    │
│ │ • Monitor closely for re-infection                                    │    │
│ │ • Be ready to re-isolate if needed                                    │    │
│ └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Post-Incident (1-2 weeks)

### Lead Agent: QA-001 (QA Architect)
### Support: All teams involved

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 6: POST-INCIDENT                                    │
│                    Timeline: 1-2 weeks                                       │
└─────────────────────────────────────────────────────────────────────────────┘

POST-INCIDENT REVIEW
┌─────────────────────────────────────────────────────────────────────────────┐
│ QA-001 facilitates, all involved agents participate                          │
│                                                                              │
│ Agenda:                                                                      │
│ 1. Incident Timeline Review                                                  │
│ 2. What Went Well                                                            │
│ 3. What Could Be Improved                                                    │
│ 4. Root Cause Discussion                                                     │
│ 5. Action Items                                                              │
│                                                                              │
│ Key Questions:                                                               │
│ • How quickly did we detect?                                                 │
│ • How effective was containment?                                             │
│ • What would have prevented this?                                            │
│ • How can we detect this faster next time?                                   │
│ • What process improvements are needed?                                      │
└─────────────────────────────────────────────────────────────────────────────┘

ACTION ITEMS
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│ Typical Action Categories:                                                   │
│                                                                              │
│ DETECTION IMPROVEMENTS                                                       │
│ • New monitoring rules                                                       │
│ • Additional logging                                                         │
│ • Alert threshold adjustments                                                │
│                                                                              │
│ PREVENTION IMPROVEMENTS                                                      │
│ • Security control enhancements                                              │
│ • Configuration hardening                                                    │
│ • Process changes                                                            │
│                                                                              │
│ RESPONSE IMPROVEMENTS                                                        │
│ • Playbook updates                                                           │
│ • Tool improvements                                                          │
│ • Training needs                                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Communication Templates

### Initial Notification (Internal)
```
SECURITY INCIDENT - [SEVERITY]
Incident ID: INC-YYYY-NNN
Time: [UTC]

Status: [Investigating/Containing/Eradicating/Recovering]
Impact: [Brief description]

Actions Underway:
- [Action 1]
- [Action 2]

Incident Commander: [Agent]
Next Update: [Time]

Join: [Communication Channel]
```

### Customer Notification (if required)
```
Security Update

We are currently investigating a security incident that
[may have/has] affected [scope].

What happened: [Brief, non-technical description]

What we're doing: [Current actions]

What you should do: [Recommended user actions]

We will provide updates as more information becomes available.
```

### Resolution Notification
```
INCIDENT RESOLVED - INC-YYYY-NNN
Resolution Time: [UTC]

Summary: [What happened]
Root Cause: [Brief description]
Impact: [Final impact assessment]
Duration: [Total incident duration]

Preventive measures being implemented.
Full post-incident review scheduled for [date].
```

---

## Escalation to Human

### Must Escalate Immediately
- Confirmed data breach affecting customers
- Ransomware with ransom demand
- Nation-state attribution
- Legal/regulatory notification required
- Media inquiries
- Law enforcement involvement needed

### Escalation Package
```json
{
  "human_escalation": {
    "incident_id": "INC-2024-0042",
    "escalated_at": "2024-01-15T11:00:00Z",
    "escalated_by": "SEC-006",

    "reason": "Confirmed data breach - customer notification required",

    "situation_summary": "...",
    "actions_taken": "...",
    "current_status": "...",

    "decisions_required": [
      "Approve customer notification text",
      "Authorize external forensics engagement",
      "Approve regulatory notification"
    ],

    "recommended_actions": "...",

    "attachments": [
      "incident_report.md",
      "timeline.json",
      "impact_assessment.md"
    ]
  }
}
```

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

### When to Rollback During Incident
- Containment action causes additional issues
- Fix attempt worsens situation
- Recovery action fails

### Emergency Rollback Steps
1. **Halt**: Stop current recovery action immediately
2. **Assess**: Evaluate new state vs previous state
3. **Revert**: Undo last action if possible
4. **Stabilize**: Focus on stable (even degraded) state
5. **Reassess**: Re-evaluate incident with new information
6. **Document**: Record rollback decision and rationale

### System Rollback
```
1. Identify last known good state
2. Prepare rollback deployment
3. Execute rollback during maintenance window (if possible)
4. Verify system functionality
5. Monitor for 30+ minutes post-rollback
6. Document in incident timeline
```

### Data Rollback (Extreme Caution)
- Requires approval from incident commander
- Assess data loss implications
- Coordinate with database team (INF-004)
- Document all data changes
