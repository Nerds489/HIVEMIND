# Deployment Checklist

---

## Deployment Information

| Field | Value |
|-------|-------|
| **Deployment ID** | [DEPLOY-YYYYMMDD-XXX] |
| **Release Version** | [VERSION] |
| **Target Environment** | [DEV / STAGING / PRODUCTION] |
| **Deployment Type** | [Standard / Hotfix / Rollback] |
| **Deployment Window** | [START_TIME] - [END_TIME] |
| **Deployment Lead** | [AGENT_ID] |

---

## Pre-Deployment Checklist

### Code & Build

| # | Item | Status | Verified By | Notes |
|---|------|--------|-------------|-------|
| 1 | All code merged to release branch | ☐ | | |
| 2 | Build passes in CI | ☐ | | |
| 3 | All unit tests pass | ☐ | | |
| 4 | All integration tests pass | ☐ | | |
| 5 | Code coverage meets threshold (≥[XX]%) | ☐ | | |
| 6 | No critical/high SAST findings | ☐ | | |
| 7 | No critical/high dependency vulnerabilities | ☐ | | |
| 8 | Release notes prepared | ☐ | | |

### Approvals

| # | Item | Status | Approver | Date |
|---|------|--------|----------|------|
| 1 | Code review approved | ☐ | | |
| 2 | Security review approved | ☐ | | |
| 3 | QA sign-off obtained | ☐ | | |
| 4 | Change request approved | ☐ | | |
| 5 | Stakeholder notification sent | ☐ | | |

### Infrastructure Readiness

| # | Item | Status | Verified By | Notes |
|---|------|--------|-------------|-------|
| 1 | Target environment healthy | ☐ | | |
| 2 | Sufficient capacity available | ☐ | | |
| 3 | Database migrations tested | ☐ | | |
| 4 | Configuration changes ready | ☐ | | |
| 5 | Secrets/credentials verified | ☐ | | |
| 6 | Load balancer configured | ☐ | | |
| 7 | SSL certificates valid | ☐ | | |

### Monitoring & Alerting

| # | Item | Status | Verified By | Notes |
|---|------|--------|-------------|-------|
| 1 | Monitoring dashboards ready | ☐ | | |
| 2 | Alerts configured | ☐ | | |
| 3 | Log aggregation working | ☐ | | |
| 4 | Health check endpoints ready | ☐ | | |
| 5 | On-call team notified | ☐ | | |

### Rollback Preparation

| # | Item | Status | Verified By | Notes |
|---|------|--------|-------------|-------|
| 1 | Rollback procedure documented | ☐ | | |
| 2 | Rollback tested in staging | ☐ | | |
| 3 | Database rollback plan ready | ☐ | | |
| 4 | Previous version artifacts available | ☐ | | |
| 5 | Rollback decision criteria defined | ☐ | | |

---

## Deployment Steps

### Step 1: Pre-Flight Verification
**Executor:** [AGENT_ID]
**Time:** [ESTIMATED_DURATION]

- [ ] Verify all pre-deployment items complete
- [ ] Confirm deployment window active
- [ ] Open communication channels
- [ ] Notify stakeholders: "Deployment starting"

### Step 2: Backup Current State
**Executor:** [AGENT_ID]
**Time:** [ESTIMATED_DURATION]

- [ ] Database backup completed
- [ ] Configuration backup completed
- [ ] Current version noted: [VERSION]
- [ ] Backup verification passed

### Step 3: Infrastructure Changes
**Executor:** [AGENT_ID]
**Time:** [ESTIMATED_DURATION]

- [ ] Apply infrastructure changes
- [ ] Verify resource provisioning
- [ ] Confirm networking updates
- [ ] Validate security groups

### Step 4: Database Migration
**Executor:** [AGENT_ID]
**Time:** [ESTIMATED_DURATION]

- [ ] Apply database migrations
- [ ] Verify schema changes
- [ ] Validate data integrity
- [ ] Confirm indexes updated

### Step 5: Application Deployment
**Executor:** [AGENT_ID]
**Time:** [ESTIMATED_DURATION]

- [ ] Deploy new application version
- [ ] Verify deployment success
- [ ] Confirm container/service health
- [ ] Validate configuration loaded

### Step 6: Traffic Routing
**Executor:** [AGENT_ID]
**Time:** [ESTIMATED_DURATION]

- [ ] Update load balancer
- [ ] Enable traffic to new version
- [ ] Drain old instances (if blue/green)
- [ ] Verify traffic routing

### Step 7: Smoke Tests
**Executor:** [AGENT_ID]
**Time:** [ESTIMATED_DURATION]

- [ ] Health endpoints responding
- [ ] Critical user flows working
- [ ] API endpoints functional
- [ ] No error spikes in logs

---

## Post-Deployment Checklist

### Immediate Verification (0-15 minutes)

| # | Item | Status | Verified By | Notes |
|---|------|--------|-------------|-------|
| 1 | Health checks passing | ☐ | | |
| 2 | No elevated error rates | ☐ | | |
| 3 | Response times normal | ☐ | | |
| 4 | No customer-reported issues | ☐ | | |
| 5 | Logs showing normal operation | ☐ | | |

### Extended Monitoring (15-60 minutes)

| # | Item | Status | Verified By | Notes |
|---|------|--------|-------------|-------|
| 1 | Error rate stable | ☐ | | |
| 2 | Performance within SLO | ☐ | | |
| 3 | No memory leaks detected | ☐ | | |
| 4 | Database connections healthy | ☐ | | |
| 5 | Cache hit rates normal | ☐ | | |

### Documentation & Communication

| # | Item | Status | Verified By | Notes |
|---|------|--------|-------------|-------|
| 1 | Deployment log completed | ☐ | | |
| 2 | Stakeholders notified: "Deployment complete" | ☐ | | |
| 3 | Release notes published | ☐ | | |
| 4 | Status page updated | ☐ | | |
| 5 | Change ticket closed | ☐ | | |

---

## Rollback Procedure

### Rollback Triggers

Initiate rollback if ANY of the following occur:

- [ ] Error rate exceeds [X]% for [Y] minutes
- [ ] Response time P99 exceeds [X]ms
- [ ] Health checks failing for [X] minutes
- [ ] Critical functionality broken
- [ ] Data corruption detected
- [ ] Security vulnerability discovered

### Rollback Steps

1. **Announce rollback**
   - [ ] Notify team: "Initiating rollback"
   - [ ] Open incident channel

2. **Stop deployment**
   - [ ] Halt any in-progress deployment
   - [ ] Prevent new deployments

3. **Revert traffic**
   - [ ] Route traffic to previous version
   - [ ] Verify traffic routing

4. **Revert database (if needed)**
   - [ ] Execute database rollback script
   - [ ] Verify data integrity

5. **Verify rollback**
   - [ ] Health checks passing
   - [ ] Error rates normalized
   - [ ] Functionality restored

6. **Post-rollback**
   - [ ] Document incident
   - [ ] Notify stakeholders
   - [ ] Schedule post-mortem

---

## Sign-Off

### Pre-Deployment Approval

| Role | Agent | Signature | Date |
|------|-------|-----------|------|
| Deployment Lead | | ☐ | |
| QA Approval | | ☐ | |
| Security Approval | | ☐ | |

### Post-Deployment Approval

| Role | Agent | Signature | Date |
|------|-------|-----------|------|
| Deployment Lead | | ☐ | |
| On-Call SRE | | ☐ | |

---

## Deployment Log

| Time | Event | Actor | Notes |
|------|-------|-------|-------|
| | Deployment started | | |
| | | | |
| | | | |
| | Deployment completed | | |

---

*Checklist template by HIVEMIND Infrastructure Team*
