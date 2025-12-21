# HIVEMIND Agent Reference

Complete reference for all 24 specialized agents organized across 4 expert teams.

---

## Overview

HIVEMIND coordinates 24 AI agents that work together as a unified intelligence. Each agent has specific expertise, and tasks are automatically routed based on keywords and context.

**Key Principle**: All agents speak with ONE unified voice. You never see individual agent responses—HIVEMIND synthesizes all expertise into coherent output.

---

## Development Team (DEV)

6 agents focused on software development, architecture, and code quality.

### DEV-001: Architect

**Role**: System design and technical strategy

**Expertise**:
- System architecture and design patterns
- API design (REST, GraphQL, gRPC)
- Microservices and monolith decisions
- Database schema design
- Technology selection
- Scalability planning

**Keywords**: `architecture`, `design`, `system`, `blueprint`, `api design`, `data model`, `microservices`, `patterns`

**Invoke**: `/architect` or describe architectural needs

---

### DEV-002: Backend Developer

**Role**: Server-side implementation

**Expertise**:
- Python, Go, Java, Node.js development
- REST API implementation
- Database queries and optimization
- Authentication/authorization
- Background jobs and queues
- Third-party integrations

**Keywords**: `backend`, `api`, `server`, `endpoint`, `python`, `go`, `java`, `service`

**Invoke**: Describe backend implementation needs

---

### DEV-003: Frontend Developer

**Role**: User interface development

**Expertise**:
- React, Vue, Angular development
- CSS/Tailwind/styled-components
- Responsive design
- State management (Redux, Zustand)
- Accessibility (WCAG)
- Performance optimization

**Keywords**: `frontend`, `ui`, `ux`, `react`, `vue`, `css`, `component`, `responsive`

**Invoke**: Describe UI/UX implementation needs

---

### DEV-004: Code Reviewer

**Role**: Code quality and standards enforcement

**Expertise**:
- Code review best practices
- Design pattern validation
- Performance analysis
- Security vulnerability detection
- Technical debt assessment
- Refactoring recommendations

**Keywords**: `review`, `code review`, `PR`, `quality`, `standards`, `best practices`

**Invoke**: `/reviewer` or request code review

---

### DEV-005: Technical Writer

**Role**: Documentation and knowledge transfer

**Expertise**:
- API documentation
- README files
- Architecture decision records (ADRs)
- User guides and tutorials
- Code comments and docstrings
- Runbooks and playbooks

**Keywords**: `document`, `docs`, `readme`, `guide`, `tutorial`, `api docs`

**Invoke**: Request documentation creation

---

### DEV-006: DevOps Liaison

**Role**: CI/CD and deployment coordination

**Expertise**:
- GitHub Actions, GitLab CI, Jenkins
- Docker containerization
- Kubernetes deployment
- Release management
- Environment configuration
- Build optimization

**Keywords**: `deploy`, `release`, `ci/cd`, `pipeline`, `docker`, `kubernetes`, `github actions`

**Invoke**: Describe deployment or CI/CD needs

---

## Security Team (SEC)

6 agents focused on offensive and defensive security.

### SEC-001: Security Architect

**Role**: Security design and threat modeling

**Expertise**:
- Threat modeling (STRIDE, PASTA)
- Security architecture patterns
- Zero trust design
- Encryption strategies
- Identity and access management
- Security requirements

**Keywords**: `security design`, `threat model`, `security architecture`, `zero trust`, `encryption`

**Invoke**: `/sec` or describe security design needs

---

### SEC-002: Penetration Tester

**Role**: Offensive security testing

**Expertise**:
- Web application testing (OWASP Top 10)
- API security testing
- Network penetration testing
- Social engineering assessment
- Vulnerability exploitation
- Security tool usage (Burp, Metasploit)

**Keywords**: `pentest`, `hack`, `exploit`, `vulnerability`, `owasp`, `attack`, `security test`

**Invoke**: `/pentest` or request security testing

---

### SEC-003: Malware Analyst

**Role**: Threat analysis and reverse engineering

**Expertise**:
- Malware reverse engineering
- Binary analysis
- IOC (Indicators of Compromise) identification
- Threat intelligence
- Sandbox analysis
- Static and dynamic analysis

**Keywords**: `malware`, `reverse engineer`, `binary`, `ioc`, `threat intel`

**Invoke**: Describe malware analysis needs

---

### SEC-004: Wireless Security Expert

**Role**: Wireless and IoT security

**Expertise**:
- WiFi security (WPA2/3, Evil Twin)
- Bluetooth security
- RF analysis
- IoT device security
- Wireless protocol analysis
- Signal interception

**Keywords**: `wireless`, `wifi`, `bluetooth`, `rf`, `iot security`

**Invoke**: Describe wireless security needs

---

### SEC-005: Compliance Auditor

**Role**: Regulatory compliance and audit

**Expertise**:
- SOC 2 Type I/II
- GDPR compliance
- PCI DSS
- HIPAA
- NIST frameworks
- ISO 27001
- Audit preparation

**Keywords**: `compliance`, `audit`, `soc2`, `gdpr`, `pci`, `hipaa`, `nist`

**Invoke**: Request compliance assessment

---

### SEC-006: Incident Responder

**Role**: Security incident handling

**Expertise**:
- Incident detection and triage
- Containment strategies
- Digital forensics
- Evidence preservation
- Root cause analysis
- Incident documentation
- Recovery procedures

**Keywords**: `incident`, `breach`, `emergency`, `forensics`, `containment`

**Invoke**: `/incident` or report security incident

---

## Infrastructure Team (INF)

6 agents focused on infrastructure, operations, and reliability.

### INF-001: Infrastructure Architect

**Role**: Cloud and infrastructure design

**Expertise**:
- AWS, Azure, GCP architecture
- Multi-cloud strategies
- Infrastructure as Code
- Capacity planning
- Cost optimization
- High availability design

**Keywords**: `infrastructure`, `cloud`, `aws`, `gcp`, `azure`, `capacity`, `scaling`

**Invoke**: `/infra` or describe infrastructure needs

---

### INF-002: Systems Administrator

**Role**: Server and system management

**Expertise**:
- Linux/Windows administration
- Server hardening
- Patch management
- User management
- Backup and recovery
- System monitoring

**Keywords**: `sysadmin`, `server`, `linux`, `windows`, `hardening`, `patching`

**Invoke**: Describe system administration needs

---

### INF-003: Network Engineer

**Role**: Network infrastructure

**Expertise**:
- Network architecture
- Firewall configuration
- DNS management
- Load balancing
- VPN setup
- Network troubleshooting

**Keywords**: `network`, `firewall`, `dns`, `routing`, `vpn`, `load balancer`

**Invoke**: Describe networking needs

---

### INF-004: Database Administrator

**Role**: Database management and optimization

**Expertise**:
- PostgreSQL, MySQL, MongoDB
- Query optimization
- Schema design
- Replication and clustering
- Backup strategies
- Performance tuning

**Keywords**: `database`, `sql`, `postgres`, `mysql`, `mongodb`, `query`, `schema`, `dba`

**Invoke**: Describe database needs

---

### INF-005: Site Reliability Engineer

**Role**: Reliability and observability

**Expertise**:
- SLO/SLI/SLA definition
- Monitoring and alerting
- On-call procedures
- Incident management
- Capacity planning
- Chaos engineering

**Keywords**: `sre`, `monitoring`, `slo`, `reliability`, `uptime`, `observability`

**Invoke**: `/sre` or describe reliability needs

---

### INF-006: Automation Engineer

**Role**: Infrastructure automation

**Expertise**:
- Terraform
- Ansible
- Puppet/Chef
- Shell scripting
- Python automation
- GitOps workflows

**Keywords**: `automate`, `terraform`, `ansible`, `script`, `iac`

**Invoke**: Describe automation needs

---

## QA Team (QA)

6 agents focused on quality assurance and testing.

### QA-001: QA Architect

**Role**: Test strategy and quality processes

**Expertise**:
- Test strategy design
- Quality gate definition
- Coverage analysis
- Risk-based testing
- Test process improvement
- Quality metrics

**Keywords**: `test strategy`, `qa plan`, `coverage`, `quality process`

**Invoke**: `/qa` or describe QA strategy needs

---

### QA-002: Test Automation Engineer

**Role**: Automated testing

**Expertise**:
- Selenium, Playwright, Cypress
- pytest, Jest, Mocha
- API testing (Postman, REST Assured)
- CI/CD integration
- Page Object Model
- Test data management

**Keywords**: `automated test`, `selenium`, `playwright`, `pytest`, `jest`

**Invoke**: Describe test automation needs

---

### QA-003: Performance Tester

**Role**: Load and performance testing

**Expertise**:
- k6, JMeter, Gatling
- Load testing strategies
- Stress testing
- Capacity testing
- Performance profiling
- Bottleneck analysis

**Keywords**: `load test`, `performance`, `benchmark`, `stress test`, `k6`, `jmeter`

**Invoke**: Describe performance testing needs

---

### QA-004: Security Tester

**Role**: Security-focused testing

**Expertise**:
- SAST (Static analysis)
- DAST (Dynamic analysis)
- Dependency scanning
- Container scanning
- DevSecOps integration
- Vulnerability management

**Keywords**: `sast`, `dast`, `security scan`, `devsecops`, `vulnerability scan`

**Invoke**: Request security testing

---

### QA-005: Manual QA Tester

**Role**: Exploratory and user acceptance testing

**Expertise**:
- Exploratory testing
- Usability testing
- Accessibility testing
- User acceptance testing (UAT)
- Bug documentation
- Test case writing

**Keywords**: `manual test`, `exploratory`, `usability`, `acceptance`

**Invoke**: Describe manual testing needs

---

### QA-006: Test Data Manager

**Role**: Test environment and data management

**Expertise**:
- Test data generation
- Data masking/anonymization
- Environment provisioning
- Mock services
- Fixture management
- Data-driven testing

**Keywords**: `test data`, `fixtures`, `test environment`, `mock`

**Invoke**: Describe test data/environment needs

---

## Agent Coordination

### Automatic Routing

HIVEMIND automatically routes tasks based on keywords:

```
"Design a REST API for users" → DEV-001 (Architect)
"Review this code for security" → DEV-004 + SEC-002
"Deploy to production" → DEV-006 + INF-005
```

### Multi-Agent Tasks

Complex tasks automatically engage multiple agents:

```
"Build a secure payment API"
→ DEV-001: Architecture
→ DEV-002: Implementation
→ SEC-001: Security requirements
→ SEC-002: Security testing
→ QA-002: Test automation
```

### Team Coordination

Request entire teams for comprehensive work:

```
"Security team, assess our infrastructure"
→ All 6 SEC agents coordinate
→ Unified report generated
```

---

## Slash Command Reference

| Command | Primary Agent | Description |
|---------|---------------|-------------|
| `/hivemind` | All | Activate full orchestration |
| `/architect` | DEV-001 | System design |
| `/dev` | DEV Team | Development coordination |
| `/sec` | SEC Team | Security coordination |
| `/infra` | INF Team | Infrastructure coordination |
| `/qa` | QA Team | QA coordination |
| `/pentest` | SEC-002 | Penetration testing |
| `/reviewer` | DEV-004 | Code review |
| `/sre` | INF-005 | Site reliability |
| `/incident` | SEC-006 | Incident response |
| `/sdlc` | All Teams | Full development lifecycle |

---

## Agent Files

Agent definitions are stored in `agents/`:

```
agents/
├── dev/
│   ├── architect.md
│   ├── backend.md
│   ├── frontend.md
│   ├── reviewer.md
│   ├── writer.md
│   └── devops.md
├── security/
│   ├── architect.md
│   ├── pentester.md
│   ├── malware.md
│   ├── wireless.md
│   ├── compliance.md
│   └── incident.md
├── infrastructure/
│   ├── architect.md
│   ├── sysadmin.md
│   ├── network.md
│   ├── dba.md
│   ├── sre.md
│   └── automation.md
├── qa/
│   ├── architect.md
│   ├── automation.md
│   ├── performance.md
│   ├── security.md
│   ├── manual.md
│   └── data.md
└── registry/
    ├── DEV-001.md through DEV-006.md
    ├── SEC-001.md through SEC-006.md
    ├── INF-001.md through INF-006.md
    └── QA-001.md through QA-006.md
```

---

*HIVEMIND - 24 Agents | 4 Teams | 1 Unified Intelligence*
