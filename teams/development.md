# Development & Architecture Team

## Team Overview

**Mission:** Transform requirements into working software through thoughtful design and disciplined implementation.

**Leader:** Architect

**Size:** 6 Agents

## Internal Registry (IDs)

This mapping is for internal routing/documentation only. Never include these IDs in user-visible output.

| Internal ID | Role | Specialty |
|-------------|------|-----------|
| DEV-001 | System Architect | Architecture, design |
| DEV-002 | Backend Developer | APIs, server-side |
| DEV-003 | Frontend Developer | UI/UX, client-side |
| DEV-004 | Code Reviewer | Quality, standards |
| DEV-005 | Technical Writer | Documentation |
| DEV-006 | DevOps Liaison | CI/CD, deployment |

## Provides (Summary)

- Architecture designs
- Code implementations
- API specifications
- Technical documentation
- CI/CD pipelines

## Interfaces (Summary)

- Security: design reviews, security requirements
- Infrastructure: deployment needs, resource requirements
- QA: feature handoffs, test support

## Team Structure

```
                    ┌─────────────────┐
                    │    ARCHITECT    │
                    │  (Team Leader)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Backend     │   │   Frontend    │   │     Code      │
│   Developer   │   │   Developer   │   │   Reviewer    │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                                         │
        ▼                                         ▼
┌───────────────┐                       ┌───────────────┐
│   Technical   │                       │    DevOps     │
│    Writer     │                       │    Liaison    │
└───────────────┘                       └───────────────┘
```

## Agent Roster

| Agent | Role | Primary Responsibility |
|-------|------|------------------------|
| **Architect** | Team Leader | System design, technical blueprints, technology decisions |
| **Backend Developer** | Core Developer | APIs, databases, server logic, business logic |
| **Frontend Developer** | Core Developer | UI/UX, client-side code, user interactions |
| **Code Reviewer** | Quality Gate | Code quality, standards enforcement, security review |
| **Technical Writer** | Documentation | Docs, guides, API references, architecture docs |
| **DevOps Liaison** | Deployment | CI/CD, containerization, deployment automation |

## Team Capabilities

### Design & Architecture
- System design and architecture patterns
- API design (REST, GraphQL, gRPC)
- Database schema design
- Microservices architecture
- Technology evaluation and selection

### Development
- Full-stack application development
- API implementation
- Database operations
- UI/UX implementation
- State management

### Quality
- Code review and standards
- Documentation
- Testing integration
- Security-aware coding

### Delivery
- CI/CD pipelines
- Container management
- Deployment automation
- Environment management

## Interaction Patterns

### Internal Team Flow
```
Requirements
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ ARCHITECT                                                    │
│ • Reviews requirements                                       │
│ • Creates technical design                                   │
│ • Defines API contracts                                      │
│ • Assigns work to developers                                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│ BACKEND DEVELOPER       │   │ FRONTEND DEVELOPER      │
│ • Implements APIs       │◄──│ • Implements UI         │
│ • Database operations   │   │ • Client-side logic     │
│ • Business logic        │──►│ • API integration       │
└───────────┬─────────────┘   └───────────┬─────────────┘
            │                             │
            └─────────────┬───────────────┘
                          │
                          ▼
            ┌─────────────────────────┐
            │ CODE REVIEWER           │
            │ • Reviews all changes   │
            │ • Enforces standards    │
            │ • Security check        │
            └───────────┬─────────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
┌─────────────────────┐ ┌─────────────────────┐
│ TECHNICAL WRITER    │ │ DEVOPS LIAISON      │
│ • Documents changes │ │ • Prepares deploy   │
│ • Updates guides    │ │ • CI/CD integration │
└─────────────────────┘ └─────────────────────┘
```

### Cross-Team Interactions

| External Team | Key Interactions |
|---------------|------------------|
| **Security** | Security architecture review, vulnerability remediation |
| **Infrastructure** | Environment needs, deployment requirements |
| **QA** | Test coverage, bug fixes, quality validation |

## Communication Protocols

### Handoff Messages

**To Security Team:**
```
REQUEST: Security Review
FROM: Development Team
PRIORITY: [High/Medium/Low]
CONTEXT: [What needs review]
DEADLINE: [When needed]
ARTIFACTS: [Code location, design docs]
```

**To QA Team:**
```
REQUEST: Testing
FROM: Development Team
FEATURE: [Feature name]
STATUS: Ready for QA
CHANGES: [Summary of changes]
TEST_FOCUS: [Areas needing attention]
DOCS: [Test documentation link]
```

**To Infrastructure Team:**
```
REQUEST: Environment/Resources
FROM: Development Team
TYPE: [New environment / Resource change]
SPECS: [Requirements]
TIMELINE: [When needed]
PURPOSE: [What it's for]
```

## Quality Gates

### Code Merge Requirements
- [ ] Code review approved
- [ ] Unit tests pass (>80% coverage)
- [ ] Linting passes
- [ ] Security scan clean
- [ ] Documentation updated
- [ ] API contracts validated

### Release Requirements
- [ ] All code reviews complete
- [ ] Integration tests pass
- [ ] Security review approved
- [ ] Performance validated
- [ ] Documentation complete
- [ ] Deployment artifacts ready

## Escalation Path

```
Issue Detected
      │
      ▼
Local Resolution Attempt
      │
      ├── Resolved ──► Document & Close
      │
      ▼ (Not Resolved)
Team Lead (Architect)
      │
      ├── Resolved ──► Document & Close
      │
      ▼ (Cross-team issue)
Cross-Team Coordination
      │
      ├── Resolved ──► Document & Close
      │
      ▼ (Needs human decision)
Human Escalation
```

## Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Code Review Turnaround | < 24 hours | Time from PR to review |
| Build Success Rate | > 95% | Successful builds / Total |
| Code Coverage | > 80% | Covered lines / Total |
| Documentation Coverage | 100% | Documented APIs / Total |
| Deployment Frequency | Daily | Deploys per day |

## Invocation

```bash
# Summon the Development Team
Task -> subagent_type: "development-team"

# Individual agents
Task -> subagent_type: "architect"
Task -> subagent_type: "backend-developer"
Task -> subagent_type: "frontend-developer"
Task -> subagent_type: "code-reviewer"
Task -> subagent_type: "technical-writer"
Task -> subagent_type: "devops-liaison"
```
