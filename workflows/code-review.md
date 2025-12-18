# HIVEMIND Code Review Workflow

## Overview

This workflow defines the comprehensive code review process, ensuring code quality, security, and maintainability through structured peer review with multiple specialized perspectives.

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CODE REVIEW PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SUBMIT      AUTOMATED     PEER         SECURITY      APPROVE    MERGE      │
│  ┌──────┐    ┌──────┐    ┌──────┐      ┌──────┐     ┌──────┐   ┌──────┐    │
│  │ PR   │──▶ │CHECKS│──▶ │REVIEW│ ──▶  │REVIEW│ ──▶ │ GATE │──▶│MERGE │    │
│  └──────┘    └──────┘    └──────┘      └──────┘     └──────┘   └──────┘    │
│                                                                              │
│  Author      CI/CD        DEV-004      QA-004       DEV-004    Author       │
│              QA-002       DEV-001      SEC-002      QA-001                  │
│                           (Arch)       (if needed)                          │
│                                                                              │
│              ◀──────────────────────────────────────────────                │
│                        CHANGES REQUESTED (loop)                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Pull Request Submission

### Author Responsibilities

Before requesting review, the author must complete:

```yaml
pre_submission_checklist:
  code_quality:
    - [ ] Code compiles without errors
    - [ ] All existing tests pass
    - [ ] New tests written for new functionality
    - [ ] Code follows style guidelines
    - [ ] No debugging code or console.logs
    - [ ] No commented-out code
    - [ ] Self-review completed

  documentation:
    - [ ] PR description explains the change
    - [ ] Complex logic has comments
    - [ ] API changes documented
    - [ ] CHANGELOG updated (if required)

  commit_hygiene:
    - [ ] Commits are atomic and logical
    - [ ] Commit messages are descriptive
    - [ ] No merge commits (rebased on main)
    - [ ] Sensitive data not committed
```

### Pull Request Template

```markdown
## Summary
[Brief description of what this PR does]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Refactoring (no functional changes)
- [ ] Documentation update

## Related Issues
Closes #[issue_number]

## Changes Made
- [Change 1]
- [Change 2]

## Testing Done
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes (or documented if breaking)

## Security Considerations
- [ ] No hardcoded secrets
- [ ] Input validation added where needed
- [ ] Authentication/authorization considered
- [ ] N/A - no security implications

## Reviewer Notes
[Any specific areas you want reviewers to focus on]
```

---

## Phase 2: Automated Checks

### CI Pipeline Requirements

```yaml
automated_checks:
  build:
    agent: "CI/CD System"
    checks:
      - Compilation succeeds
      - Dependencies resolve
      - Build artifacts generated
    blocking: true

  unit_tests:
    agent: QA-002
    checks:
      - All unit tests pass
      - No new test failures
      - Test execution time reasonable
    blocking: true

  code_coverage:
    agent: QA-002
    checks:
      - Coverage meets threshold (≥80%)
      - No significant coverage decrease
      - New code has test coverage
    blocking: true
    threshold: 80%

  linting:
    agent: "CI/CD System"
    checks:
      - ESLint/Pylint/etc. passes
      - No style violations
      - Formatting correct
    blocking: true

  static_analysis:
    agent: QA-004
    checks:
      - SAST scan clean
      - No critical/high findings
      - Code complexity acceptable
    blocking: true

  dependency_scan:
    agent: QA-004
    checks:
      - No critical vulnerabilities
      - No high vulnerabilities (unless accepted)
      - License compliance
    blocking: true

  secrets_scan:
    agent: QA-004
    checks:
      - No hardcoded credentials
      - No API keys
      - No private keys
    blocking: true
```

### Automated Check Results

```json
{
  "automated_checks": {
    "pr_number": 1234,
    "commit": "abc123",
    "timestamp": "2024-01-15T10:30:00Z",

    "results": {
      "build": {"status": "passed", "duration": "45s"},
      "unit_tests": {
        "status": "passed",
        "tests_run": 256,
        "tests_passed": 256,
        "duration": "2m 15s"
      },
      "coverage": {
        "status": "passed",
        "current": "87.3%",
        "delta": "+0.5%",
        "threshold": "80%"
      },
      "linting": {"status": "passed", "warnings": 2},
      "sast": {
        "status": "passed",
        "findings": {"critical": 0, "high": 0, "medium": 1, "low": 3}
      },
      "dependency_scan": {
        "status": "passed",
        "vulnerabilities": {"critical": 0, "high": 0}
      },
      "secrets_scan": {"status": "passed", "findings": 0}
    },

    "overall_status": "passed",
    "ready_for_review": true
  }
}
```

---

## Phase 3: Peer Review

### Primary Reviewer: DEV-004 (Code Reviewer)

### Review Assignment

```yaml
reviewer_assignment:
  automatic_rules:
    - CODEOWNERS file determines required reviewers
    - Changed files determine expertise needed
    - Workload balancing across team

  required_reviewers:
    default: 1
    sensitive_areas:
      authentication: 2
      payments: 2
      infrastructure: 2

  optional_reviewers:
    - Domain experts for specific areas
    - Original authors of modified code
```

### Code Review Checklist

```yaml
review_checklist:
  correctness:
    reviewer: DEV-004
    checks:
      - [ ] Logic is correct and handles edge cases
      - [ ] Error handling is appropriate
      - [ ] No obvious bugs or issues
      - [ ] Concurrency handled correctly (if applicable)
      - [ ] Resources properly managed (memory, connections, files)

  design:
    reviewer: DEV-004
    escalate_to: DEV-001
    checks:
      - [ ] Follows existing architectural patterns
      - [ ] Appropriate level of abstraction
      - [ ] No unnecessary complexity
      - [ ] SOLID principles followed
      - [ ] DRY principle followed (no unnecessary duplication)

  maintainability:
    reviewer: DEV-004
    checks:
      - [ ] Code is readable and understandable
      - [ ] Naming is clear and consistent
      - [ ] Functions are appropriately sized
      - [ ] Comments explain "why" not "what"
      - [ ] No magic numbers or strings

  testing:
    reviewer: DEV-004
    support: QA-002
    checks:
      - [ ] Tests cover new functionality
      - [ ] Tests cover edge cases
      - [ ] Tests are readable and maintainable
      - [ ] Mocks/stubs used appropriately
      - [ ] Integration tests added where needed

  performance:
    reviewer: DEV-004
    escalate_to: QA-003
    checks:
      - [ ] No obvious performance issues
      - [ ] Database queries are efficient
      - [ ] No N+1 query problems
      - [ ] Caching used appropriately
      - [ ] Large data sets handled correctly

  documentation:
    reviewer: DEV-004
    checks:
      - [ ] Public APIs documented
      - [ ] Complex algorithms explained
      - [ ] README updated if needed
      - [ ] API docs generated correctly
```

### Review Comment Types

```yaml
comment_types:
  blocking:
    prefix: "[BLOCKING]"
    description: "Must be addressed before merge"
    examples:
      - Security vulnerability
      - Logic error
      - Missing error handling
      - Breaking change without migration

  suggestion:
    prefix: "[SUGGESTION]"
    description: "Recommended improvement, author decides"
    examples:
      - Better naming
      - Refactoring opportunity
      - Alternative approach

  question:
    prefix: "[QUESTION]"
    description: "Clarification needed"
    examples:
      - Why this approach?
      - How does this handle X?
      - Is this intentional?

  nitpick:
    prefix: "[NIT]"
    description: "Minor style preference, optional"
    examples:
      - Formatting preference
      - Comment wording
      - Import ordering

  praise:
    prefix: "[NICE]"
    description: "Positive feedback"
    examples:
      - Clean implementation
      - Good test coverage
      - Elegant solution
```

### Review Comment Template

```json
{
  "review_comment": {
    "pr_number": 1234,
    "file": "src/api/users/router.py",
    "line": 45,
    "reviewer": "DEV-004",
    "type": "blocking",

    "comment": "[BLOCKING] SQL injection vulnerability. User input is directly interpolated into the query string.",

    "suggestion": {
      "original_code": "query = f\"SELECT * FROM users WHERE name = '{name}'\"",
      "suggested_code": "query = \"SELECT * FROM users WHERE name = %s\"\ncursor.execute(query, (name,))"
    },

    "references": [
      "https://owasp.org/SQL_Injection"
    ]
  }
}
```

---

## Phase 4: Security Review

### Trigger Conditions

```yaml
security_review_triggers:
  automatic:
    - Changes to authentication/authorization
    - Changes to encryption/cryptography
    - Changes to user input handling
    - Changes to database queries
    - Changes to file operations
    - Changes to external API integrations
    - Changes to secrets/configuration
    - Changes to permission/access control
    - New dependencies added

  manual_request:
    - Author requests security review
    - Peer reviewer escalates concern
```

### Security Reviewer: QA-004 (Security Tester) / SEC-002 (Penetration Tester)

### Security Review Checklist

```yaml
security_review:
  input_validation:
    checks:
      - [ ] All user inputs validated
      - [ ] Validation on server side (not just client)
      - [ ] Whitelist validation preferred
      - [ ] Input length limits enforced

  injection_prevention:
    checks:
      - [ ] Parameterized queries used
      - [ ] Output encoding applied
      - [ ] Command injection prevented
      - [ ] LDAP injection prevented

  authentication:
    checks:
      - [ ] Authentication required where needed
      - [ ] Session management secure
      - [ ] Password handling correct
      - [ ] MFA considered

  authorization:
    checks:
      - [ ] Authorization checks present
      - [ ] Principle of least privilege
      - [ ] No IDOR vulnerabilities
      - [ ] Role-based access correct

  data_protection:
    checks:
      - [ ] Sensitive data encrypted
      - [ ] PII handled correctly
      - [ ] Secrets not hardcoded
      - [ ] Logging doesn't expose sensitive data

  security_headers:
    checks:
      - [ ] CORS configured correctly
      - [ ] CSRF protection present
      - [ ] Security headers set
      - [ ] Cookie attributes correct
```

### Security Review Report

```json
{
  "security_review": {
    "pr_number": 1234,
    "reviewer": "QA-004",
    "reviewed_at": "2024-01-15T14:00:00Z",

    "scope": {
      "files_reviewed": 8,
      "security_sensitive_changes": true,
      "areas_reviewed": ["authentication", "input_validation", "database_queries"]
    },

    "findings": [
      {
        "severity": "high",
        "type": "injection",
        "file": "src/api/search.py",
        "line": 23,
        "description": "User input not sanitized before database query",
        "recommendation": "Use parameterized queries",
        "status": "blocking"
      }
    ],

    "verdict": "changes_requested",
    "notes": "One high severity finding must be addressed before merge"
  }
}
```

---

## Phase 5: Approval Gate

### Approval Requirements

```yaml
approval_requirements:
  standard_pr:
    required_approvals: 1
    required_reviewers: ["DEV-004"]
    automated_checks: "all_passing"

  security_sensitive_pr:
    required_approvals: 2
    required_reviewers: ["DEV-004", "QA-004"]
    automated_checks: "all_passing"
    security_review: "approved"

  architecture_pr:
    required_approvals: 2
    required_reviewers: ["DEV-004", "DEV-001"]
    automated_checks: "all_passing"

  critical_system_pr:
    required_approvals: 2
    required_reviewers: ["DEV-004", "DEV-001", "QA-001"]
    automated_checks: "all_passing"
    qa_signoff: "required"
```

### Final Approval Checklist

```yaml
final_approval:
  automated:
    - [ ] All CI checks passing
    - [ ] No merge conflicts
    - [ ] Branch up to date with main

  peer_review:
    - [ ] Required approvals obtained
    - [ ] All blocking comments resolved
    - [ ] All conversations resolved

  security:
    - [ ] Security review completed (if required)
    - [ ] No unresolved security findings

  process:
    - [ ] PR description complete
    - [ ] Documentation updated
    - [ ] CHANGELOG updated (if required)
```

### Approval Decision

```json
{
  "approval_decision": {
    "pr_number": 1234,
    "decision": "approved",
    "approved_by": "DEV-004",
    "approved_at": "2024-01-15T16:00:00Z",

    "review_summary": {
      "comments_total": 12,
      "blocking_resolved": 3,
      "suggestions_accepted": 5,
      "suggestions_declined": 2
    },

    "security_review": {
      "required": true,
      "completed": true,
      "approved_by": "QA-004"
    },

    "ready_to_merge": true,
    "merge_method": "squash"
  }
}
```

---

## Phase 6: Merge

### Merge Strategies

```yaml
merge_strategies:
  squash_merge:
    when: "Feature branches, multiple WIP commits"
    benefits: "Clean history, single commit per PR"
    settings:
      delete_branch: true

  merge_commit:
    when: "Large features, preserve history important"
    benefits: "Full commit history preserved"
    settings:
      delete_branch: true

  rebase_merge:
    when: "Linear history required"
    benefits: "Clean linear history"
    settings:
      delete_branch: true
```

### Post-Merge Actions

```yaml
post_merge:
  automatic:
    - Delete source branch
    - Close linked issues
    - Trigger deployment pipeline (if configured)
    - Update project board

  notifications:
    - Author notified of merge
    - Linked issue reporters notified
    - Team channel notification (optional)
```

---

## Special Review Scenarios

### Emergency Hotfix Review

```yaml
hotfix_review:
  trigger: "Production incident requiring immediate fix"

  process:
    - Create hotfix branch from main
    - Implement minimal fix
    - Run automated checks
    - Single reviewer approval (senior)
    - Merge to main and deploy
    - Full review post-deployment

  requirements:
    - Incident documented
    - Minimal change scope
    - Senior reviewer approval
    - Post-merge review scheduled

  timeline:
    review_sla: "30 minutes"
    full_review: "Within 24 hours"
```

### Large PR Review

```yaml
large_pr_review:
  definition: "> 500 lines changed OR > 20 files"

  recommendations:
    - Split into smaller PRs if possible
    - Provide detailed walkthrough document
    - Schedule synchronous review session
    - Review in stages (architecture, implementation, tests)

  process:
    - Author provides review guide
    - Assign multiple reviewers for different areas
    - Use draft PR for early feedback
    - Allow extended review time
```

### Cross-Team PR Review

```yaml
cross_team_review:
  trigger: "PR affects multiple team domains"

  process:
    - Identify affected teams
    - Request reviewer from each team
    - Each team reviews their domain
    - Coordinate resolution of cross-cutting concerns

  coordination:
    - Primary reviewer coordinates
    - Cross-team discussion if conflicts
    - Architecture review if needed (DEV-001)
```

---

## Review Metrics & KPIs

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Review Turnaround Time | < 4 hours | > 8 hours |
| Time to Merge | < 24 hours | > 48 hours |
| Review Iterations | < 3 | > 5 |
| Comment Resolution Rate | > 95% | < 90% |
| Post-Merge Bug Rate | < 5% | > 10% |
| Security Issue Detection | > 90% | < 80% |

---

## Review Best Practices

### For Authors

```yaml
author_best_practices:
  - Keep PRs small and focused (< 400 lines ideal)
  - Write descriptive PR descriptions
  - Self-review before requesting review
  - Respond to feedback promptly
  - Be open to suggestions
  - Explain complex decisions
  - Don't take feedback personally
```

### For Reviewers

```yaml
reviewer_best_practices:
  - Review promptly (within 4 hours)
  - Be constructive and respectful
  - Distinguish blocking from suggestions
  - Explain the "why" behind feedback
  - Praise good code
  - Suggest specific improvements
  - Don't bikeshed on style (use linters)
  - Ask questions before assuming
```

### Review Etiquette

```yaml
review_etiquette:
  do:
    - "This could be simplified by..." (constructive)
    - "Have you considered...?" (inquiry)
    - "Great use of X pattern here!" (praise)
    - "I don't understand this - can you explain?" (curiosity)

  avoid:
    - "This is wrong" (non-constructive)
    - "Why would you do this?" (accusatory)
    - "Just use X instead" (no explanation)
    - Long debates in comments (take offline)
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

### When to Rollback
- Critical issues discovered after merge
- Performance regression detected
- Security vulnerability introduced

### Rollback Steps
1. **Identify**: Locate problematic commit(s)
2. **Revert**: Create revert commit or rollback PR
3. **Review**: Fast-track review of rollback
4. **Deploy**: Push rollback to affected environments
5. **Notify**: Inform team of rollback and reason
6. **Root Cause**: Investigate why issue wasn't caught in review

### Prevention
- Update review checklist with missed pattern
- Add automated check if applicable
- Document lesson learned in team memory
