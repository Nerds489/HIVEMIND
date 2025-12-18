# Infrastructure & Operations Team

## Team Overview

**Mission:** Build and maintain the foundation that applications run on, ensuring reliability and performance at scale. Keep the lights on, automate everything.

**Leader:** Infrastructure Architect

**Size:** 6 Agents

## Internal Registry (IDs)

This mapping is for internal routing/documentation only. Never include these IDs in user-visible output.

| Internal ID | Role | Specialty |
|-------------|------|-----------|
| INF-001 | Infrastructure Architect | Cloud architecture |
| INF-002 | Systems Administrator | Server management |
| INF-003 | Network Engineer | Networking, security |
| INF-004 | Database Administrator | Data management |
| INF-005 | Site Reliability Engineer | Reliability, monitoring |
| INF-006 | Automation Engineer | IaC, automation |

## Provides (Summary)

- Infrastructure architecture
- Deployment environments
- Database management
- Network configuration
- Monitoring and reliability

## Interfaces (Summary)

- Development: deployment targets, environments
- Security: hardening implementation
- QA: test environments, performance data

## Team Structure

```
                    ┌─────────────────────────┐
                    │ INFRASTRUCTURE ARCHITECT│
                    │     (Team Leader)       │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│    Systems    │      │    Network    │      │   Database    │
│Administrator  │      │   Engineer    │      │ Administrator │
└───────────────┘      └───────────────┘      └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
               ┌────────────────┼────────────────┐
               │                                 │
               ▼                                 ▼
      ┌───────────────┐                ┌───────────────┐
      │     Site      │                │  Automation   │
      │  Reliability  │                │   Engineer    │
      │   Engineer    │                │               │
      └───────────────┘                └───────────────┘
```

## Agent Roster

| Agent | Role | Primary Responsibility |
|-------|------|------------------------|
| **Infrastructure Architect** | Team Leader | Cloud design, capacity planning, DR |
| **Systems Administrator** | Server Specialist | Server management, hardening, patching |
| **Network Engineer** | Connectivity | Firewalls, routing, DNS, load balancing |
| **Database Administrator** | Data Specialist | Database management, optimization, backup |
| **Site Reliability Engineer** | Reliability | Monitoring, SLOs, incident response, on-call |
| **Automation Engineer** | Efficiency | Terraform, Ansible, scripting, IaC |

## Team Capabilities

### Infrastructure Design
- Cloud architecture (AWS, GCP, Azure)
- Multi-region and hybrid designs
- Disaster recovery planning
- Capacity planning
- Cost optimization

### System Operations
- Server provisioning and management
- Configuration management
- Patch management
- Security hardening
- Backup and recovery

### Network Operations
- Network design and implementation
- Firewall management
- Load balancing
- DNS management
- VPN and connectivity

### Data Operations
- Database administration
- Query optimization
- Replication and HA
- Backup and recovery
- Data migration

### Reliability
- Monitoring and alerting
- SLO/SLI management
- Incident management
- Capacity management
- Chaos engineering

### Automation
- Infrastructure as Code
- Configuration automation
- Workflow automation
- Self-service tooling
- Toil reduction

## Interaction Patterns

### Infrastructure Request Flow
```
Infrastructure Request
         │
         ▼
┌────────────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE ARCHITECT                                        │
│ • Reviews requirements                                          │
│ • Designs solution                                              │
│ • Assigns implementation                                        │
└──────────────────────────┬─────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ SYSTEMS ADMIN  │ │ NETWORK        │ │ DATABASE       │
│ • Provisions   │ │ ENGINEER       │ │ ADMINISTRATOR  │
│   servers      │ │ • Configures   │ │ • Sets up      │
│ • Hardens      │ │   network      │ │   databases    │
│   systems      │ │ • Firewall     │ │ • Configures   │
└───────┬────────┘ └───────┬────────┘ └───────┬────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │ AUTOMATION ENGINEER    │
              │ • Codifies infra       │
              │ • Creates automation   │
              │ • Documents            │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ SITE RELIABILITY       │
              │ ENGINEER               │
              │ • Sets up monitoring   │
              │ • Defines SLOs         │
              │ • Creates runbooks     │
              └────────────────────────┘
```

### Cross-Team Interactions

| External Team | Key Interactions |
|---------------|------------------|
| **Development** | Environment provisioning, deployment support |
| **Security** | Security hardening, incident response coordination |
| **QA** | Test environment management, performance testing |

## Communication Protocols

### Infrastructure Change Request
```
REQUEST: Infrastructure Change
TYPE: [New/Modify/Remove]
COMPONENT: [Server/Network/Database/etc.]
DESCRIPTION: [What's needed]
JUSTIFICATION: [Why needed]
TIMELINE: [When needed]
IMPACT: [Expected impact]
REQUESTER: [Team/Agent]
```

### Incident Communication
```
INCIDENT: [Brief description]
SEVERITY: [P1/P2/P3/P4]
STATUS: [Investigating/Identified/Fixing/Resolved]
IMPACT: [What's affected]
CURRENT_ACTION: [What's being done]
ETA: [Estimated resolution]
COMMANDER: Site Reliability Engineer
```

### Maintenance Notification
```
MAINTENANCE: Scheduled
WINDOW: [Start time] - [End time] UTC
AFFECTED: [Systems/Services]
TYPE: [Patching/Upgrade/Migration]
IMPACT: [Expected impact]
ROLLBACK: [Available/Not Available]
CONTACT: [On-call team]
```

## Operational Gates

### Change Approval
- [ ] Change request documented
- [ ] Risk assessment complete
- [ ] Rollback plan defined
- [ ] Maintenance window scheduled
- [ ] Stakeholders notified
- [ ] Monitoring prepared

### Production Readiness
- [ ] Infrastructure provisioned
- [ ] Security hardening applied
- [ ] Monitoring configured
- [ ] Alerts defined
- [ ] Runbooks created
- [ ] DR tested

## Escalation Path

```
Issue Detected
      │
      ▼
SRE On-Call
      │
      ├── Resolved ──► Document & Close
      │
      ▼ (Requires specialist)
Component Owner (SysAdmin/NetEng/DBA)
      │
      ├── Resolved ──► Document & Close
      │
      ▼ (Architecture decision needed)
Infrastructure Architect
      │
      ├── Resolved ──► Document & Close
      │
      ▼ (Major incident / Business decision)
Human Escalation
```

## Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.9% | Uptime percentage |
| Mean Time to Recovery | < 30 min | Time to restore service |
| Change Success Rate | > 95% | Successful changes / Total |
| Infrastructure as Code | 100% | Resources managed via IaC |
| Cost Efficiency | -10% YoY | Cloud spend optimization |

## On-Call Rotation

```
PRIMARY ON-CALL: Site Reliability Engineer
SECONDARY: Systems Administrator

ESCALATION ORDER:
1. SRE (0-15 min)
2. Systems Administrator (15-30 min)
3. Component Specialist (30-60 min)
4. Infrastructure Architect (60+ min)

HANDOFF: Daily at 09:00 UTC
```

## Invocation

```bash
# Summon the Infrastructure Team
Task -> subagent_type: "infrastructure-team"

# Individual agents
Task -> subagent_type: "infrastructure-architect"
Task -> subagent_type: "systems-administrator"
Task -> subagent_type: "network-engineer"
Task -> subagent_type: "database-administrator"
Task -> subagent_type: "site-reliability-engineer"
Task -> subagent_type: "automation-engineer"
```
