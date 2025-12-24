# HIVEMIND Example Prompts

Real-world examples of how to effectively use HIVEMIND for various tasks.

---

## Development Tasks

### Full Stack Feature Development
```
HIVEMIND, build a user authentication system with:
- JWT-based auth with refresh tokens
- Login, register, password reset endpoints
- React login form with validation
- PostgreSQL user table with bcrypt passwords
- Unit tests for auth service
- API documentation
```

### Code Review Request
```
/reviewer

Review this pull request for:
- Security vulnerabilities
- Performance issues
- Code quality and maintainability
- Test coverage
- Documentation completeness

[paste code or PR link]
```

### Architecture Design
```
/architect

Design a microservices architecture for an e-commerce platform:
- User service
- Product catalog
- Order management
- Payment processing
- Inventory tracking

Consider: scalability, resilience, data consistency
```

### API Implementation
```
/dev

Implement a REST API for task management:
- CRUD operations for tasks
- User assignment
- Status workflow (todo → in_progress → done)
- Filtering and pagination
- Rate limiting

Tech: FastAPI + PostgreSQL + Redis cache
```

---

## Security Tasks

### Security Assessment
```
/sec

Perform a security assessment of this application:
- Authentication and authorization review
- Input validation analysis
- Dependency vulnerability scan
- Security headers check
- OWASP Top 10 coverage

[provide codebase or repo link]
```

### Penetration Test Planning
```
/pentest

Create a penetration test plan for:
- Web application at https://example.com
- Scope: All subdomains, APIs
- Exclude: Production database writes
- Timeline: 2 weeks
- Deliverable: Full report with findings
```

### Incident Response
```
/incident

Potential data breach detected:
- Unusual outbound traffic from web server
- Spike in failed login attempts
- Unknown process running as www-data

Need: Containment, investigation, remediation plan
```

### Compliance Review
```
/sec

Review our infrastructure for SOC 2 Type II compliance:
- Access control policies
- Logging and monitoring
- Change management
- Incident response
- Vendor management

Gap analysis and remediation roadmap needed.
```

---

## Infrastructure Tasks

### Cloud Architecture
```
/infra

Design AWS infrastructure for a SaaS application:
- High availability across 2 regions
- Auto-scaling based on load
- RDS PostgreSQL with read replicas
- Redis ElastiCache cluster
- CloudFront CDN
- VPC with public/private subnets

Provide: Terraform modules + architecture diagram
```

### Kubernetes Deployment
```
/infra

Create Kubernetes manifests for:
- Backend API (3 replicas, HPA)
- Frontend (2 replicas)
- PostgreSQL (StatefulSet)
- Redis (Sentinel mode)
- Ingress with TLS
- ConfigMaps and Secrets

Include: Helm chart structure
```

### Database Optimization
```
/infra

Optimize this slow PostgreSQL query:
[paste query]

Database size: 50GB
Table rows: 10 million
Current execution time: 45 seconds
Target: Under 500ms

Need: Query analysis, index recommendations, restructuring suggestions
```

### SRE Monitoring Setup
```
/sre

Set up comprehensive monitoring for production:
- Prometheus metrics collection
- Grafana dashboards
- PagerDuty alerting
- SLOs: 99.9% availability, P99 < 200ms
- Runbooks for common issues

Provide: Configuration files, dashboard JSON, alert rules
```

---

## QA Tasks

### Test Strategy
```
/qa

Create a test strategy for a banking mobile app:
- Risk-based testing approach
- Test levels (unit, integration, E2E, UAT)
- Security testing requirements
- Performance benchmarks
- Accessibility standards
- Test environment needs

Deliverable: Test plan document
```

### Test Automation
```
/qa

Write Playwright E2E tests for checkout flow:
1. Add product to cart
2. Apply discount code
3. Enter shipping info
4. Select payment method
5. Complete purchase
6. Verify confirmation

Include: Page objects, fixtures, CI integration
```

### Performance Testing
```
/qa

Design load tests for API:
- Target: 1000 concurrent users
- Test scenarios: Browse, Search, Checkout
- Ramp-up: 5 minutes to peak
- Duration: 30 minutes steady state
- Metrics: Response time, throughput, errors

Tool: k6
Provide: Test scripts + Grafana dashboard
```

### Security Testing
```
/qa

Integrate security testing in CI/CD:
- SAST: Semgrep rules
- SCA: Snyk for dependencies
- DAST: ZAP baseline scan
- Container: Trivy scan
- IaC: Checkov for Terraform

Provide: GitHub Actions workflow
```

---

## Multi-Team Workflows

### Full SDLC
```
/sdlc

New feature: Real-time notifications
- WebSocket-based push notifications
- User preferences for notification types
- Mobile push via Firebase
- Email fallback
- Admin dashboard for broadcasts

Execute full lifecycle: Design → Implement → Test → Deploy
```

### Security-First Development
```
HIVEMIND

Build a secrets management solution:
1. Architecture design (SEC-001 + DEV-001)
2. Implementation (DEV-002)
3. Security review (SEC-002)
4. Infrastructure (INF-001 + INF-006)
5. Testing (QA-002 + QA-004)
6. Documentation (DEV-005)

Coordinate all teams for secure delivery.
```

---

## Memory & Context

### Store Preferences
```
Remember that for this project we use:
- Python 3.11 with FastAPI
- PostgreSQL 15
- React 18 with TypeScript
- Tailwind CSS
- pytest for testing
- GitHub Actions for CI/CD
```

### Recall Context
```
/recall

What were the decisions we made about:
- Database schema
- API authentication
- Error handling patterns
```

### Project Setup
```
HIVEMIND

Starting new project "TaskFlow":
- Task management SaaS
- Multi-tenant architecture
- React + FastAPI + PostgreSQL
- AWS deployment

Remember this context for all future work.
```

---

## Troubleshooting

### Debug Routing
```
/debug routing

Tasks seem to go to wrong agents.
Example: Security questions going to DEV team.
```

### Check System
```
/status full

Show all agents, memory, and engine status.
```

### Memory Issues
```
/debug memory

Memories from yesterday not appearing.
Check if persistence is working.
```

---

## Tips for Best Results

1. **Be specific** - Include details, constraints, requirements
2. **Use slash commands** - Route to the right expertise
3. **Provide context** - Share relevant code, configs, links
4. **Store learnings** - Use "remember" for project patterns
5. **Check status** - Use `/status` to verify system health

---

*HIVEMIND - Unified Intelligence for Complex Tasks*
