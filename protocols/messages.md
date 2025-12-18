# HIVEMIND Message Types Protocol

## Overview

All communication between HIVEMIND agents uses structured message types. This protocol defines five message types with complete schemas, priority handling, and usage guidelines.

---

## Message Type 1: REQUEST

A REQUEST message asks an agent to perform work.

### Schema

```json
{
  "message_type": "REQUEST",
  "request_id": "REQ-YYYYMMDD-XXXXXX",
  "timestamp": "ISO8601",
  "priority": "P0|P1|P2|P3|P4",

  "routing": {
    "from_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name",
      "team": "Team Name"
    },
    "to_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name",
      "team": "Team Name"
    },
    "cc_agents": []
  },

  "request": {
    "title": "Short descriptive title",
    "description": "Detailed description of what needs to be done",
    "type": "implementation|review|assessment|analysis|documentation|deployment|investigation",
    "scope": {
      "inclusions": ["What is in scope"],
      "exclusions": ["What is explicitly out of scope"]
    }
  },

  "context": {
    "background": "Why this request is being made",
    "parent_task": "Parent task ID if applicable",
    "related_tasks": ["Related task IDs"],
    "previous_work": "Summary of relevant previous work"
  },

  "requirements": {
    "inputs_provided": [
      {
        "name": "Input name",
        "type": "document|code|data|config",
        "location": "Path or reference"
      }
    ],
    "outputs_expected": [
      {
        "name": "Output name",
        "type": "document|code|data|config",
        "format": "Format specification"
      }
    ],
    "success_criteria": ["Specific, measurable criteria"],
    "constraints": ["Technical or business constraints"]
  },

  "timeline": {
    "deadline": "ISO8601 or null",
    "deadline_type": "hard|soft",
    "estimated_effort": "hours|days",
    "checkpoints": [
      {
        "name": "Checkpoint name",
        "due": "ISO8601"
      }
    ]
  },

  "metadata": {
    "security_classification": "public|internal|confidential|restricted",
    "approval_required": true|false,
    "audit_required": true|false
  }
}
```

### Priority Levels

| Priority | Name | SLA Response | SLA Resolution | Use Cases |
|----------|------|--------------|----------------|-----------|
| **P0** | Critical | 15 minutes | 4 hours | Production down, active security breach, data loss |
| **P1** | High | 1 hour | 24 hours | Major feature broken, security vulnerability confirmed |
| **P2** | Medium | 4 hours | 3 days | Significant issue with workaround, important feature work |
| **P3** | Low | 24 hours | 1 week | Minor issues, enhancements, non-critical bugs |
| **P4** | Info | Best effort | Best effort | Documentation, research, nice-to-have items |

### Required vs Optional Fields

**Required Fields:**
- message_type
- request_id
- timestamp
- priority
- routing.from_agent
- routing.to_agent
- request.title
- request.description
- request.type

**Optional Fields:**
- routing.cc_agents
- context (all)
- requirements.constraints
- timeline.checkpoints
- metadata.audit_required

### Examples

#### P0 Example: Production Incident
```json
{
  "message_type": "REQUEST",
  "request_id": "REQ-20240115-000001",
  "timestamp": "2024-01-15T10:30:00Z",
  "priority": "P0",
  "routing": {
    "from_agent": {"id": "INF-005", "name": "SRE", "team": "Infrastructure"},
    "to_agent": {"id": "SEC-006", "name": "Incident Responder", "team": "Security"}
  },
  "request": {
    "title": "Suspicious Authentication Activity Detected",
    "description": "Anomalous login patterns detected: 500+ failed attempts from multiple IPs targeting admin accounts in last 10 minutes. Potential credential stuffing attack in progress.",
    "type": "investigation"
  },
  "timeline": {
    "deadline": "2024-01-15T11:00:00Z",
    "deadline_type": "hard"
  }
}
```

#### P2 Example: Feature Request
```json
{
  "message_type": "REQUEST",
  "request_id": "REQ-20240115-000042",
  "timestamp": "2024-01-15T14:00:00Z",
  "priority": "P2",
  "routing": {
    "from_agent": {"id": "DEV-001", "name": "Architect", "team": "Development"},
    "to_agent": {"id": "DEV-002", "name": "Backend Developer", "team": "Development"}
  },
  "request": {
    "title": "Implement User Profile API Endpoints",
    "description": "Create REST API endpoints for user profile CRUD operations according to approved design spec.",
    "type": "implementation"
  },
  "requirements": {
    "outputs_expected": [
      {"name": "API Implementation", "type": "code", "format": "Python/FastAPI"},
      {"name": "Unit Tests", "type": "code", "format": "pytest"}
    ],
    "success_criteria": [
      "All endpoints return correct status codes",
      "Input validation implemented",
      "Unit test coverage > 80%"
    ]
  },
  "timeline": {
    "deadline": "2024-01-18T18:00:00Z",
    "deadline_type": "soft"
  }
}
```

---

## Message Type 2: RESPONSE

A RESPONSE message returns results from completed (or failed) work.

### Schema

```json
{
  "message_type": "RESPONSE",
  "response_id": "RES-YYYYMMDD-XXXXXX",
  "request_id": "Original request ID",
  "timestamp": "ISO8601",

  "routing": {
    "from_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name",
      "team": "Team Name"
    },
    "to_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name",
      "team": "Team Name"
    }
  },

  "status": {
    "code": "success|partial_success|failure|blocked",
    "summary": "Brief status summary"
  },

  "results": {
    "findings": [
      {
        "id": "Finding ID",
        "type": "finding type",
        "severity": "critical|high|medium|low|info",
        "description": "Description",
        "evidence": "Evidence or reference",
        "recommendation": "Recommended action"
      }
    ],
    "deliverables": [
      {
        "name": "Deliverable name",
        "type": "document|code|data|config",
        "location": "Path or reference",
        "validation_status": "passed|failed|skipped"
      }
    ],
    "metrics": {
      "key": "value"
    }
  },

  "confidence": {
    "overall": 0.0-1.0,
    "factors": {
      "completeness": 0.0-1.0,
      "accuracy": 0.0-1.0,
      "uncertainty_areas": ["Areas with lower confidence"]
    }
  },

  "next_steps": {
    "recommended_actions": ["Recommended follow-up actions"],
    "handoff_ready": true|false,
    "handoff_destination": "TEAM-XXX or null"
  },

  "metadata": {
    "time_spent": "Duration",
    "tools_used": ["List of tools"],
    "blockers_encountered": ["Any blockers faced"]
  }
}
```

### Success Response Example
```json
{
  "message_type": "RESPONSE",
  "response_id": "RES-20240115-000042",
  "request_id": "REQ-20240115-000042",
  "timestamp": "2024-01-15T17:30:00Z",
  "routing": {
    "from_agent": {"id": "DEV-002", "name": "Backend Developer", "team": "Development"},
    "to_agent": {"id": "DEV-001", "name": "Architect", "team": "Development"}
  },
  "status": {
    "code": "success",
    "summary": "User Profile API implementation complete"
  },
  "results": {
    "deliverables": [
      {"name": "API Implementation", "location": "/src/api/users/", "validation_status": "passed"},
      {"name": "Unit Tests", "location": "/tests/api/users/", "validation_status": "passed"}
    ],
    "metrics": {
      "test_coverage": "87%",
      "endpoints_implemented": 5
    }
  },
  "confidence": {
    "overall": 0.95,
    "factors": {
      "completeness": 1.0,
      "accuracy": 0.95,
      "uncertainty_areas": ["Edge case handling for concurrent updates"]
    }
  },
  "next_steps": {
    "recommended_actions": ["Code review", "Integration testing"],
    "handoff_ready": true,
    "handoff_destination": "DEV-004"
  }
}
```

### Partial Success Response Example
```json
{
  "status": {
    "code": "partial_success",
    "summary": "3 of 5 endpoints implemented, blocked on database schema"
  },
  "results": {
    "deliverables": [
      {"name": "GET /users", "validation_status": "passed"},
      {"name": "GET /users/{id}", "validation_status": "passed"},
      {"name": "POST /users", "validation_status": "passed"},
      {"name": "PUT /users/{id}", "validation_status": "blocked"},
      {"name": "DELETE /users/{id}", "validation_status": "blocked"}
    ]
  },
  "confidence": {
    "overall": 0.60
  }
}
```

### Failure Response Example
```json
{
  "status": {
    "code": "failure",
    "summary": "Unable to complete request due to missing dependencies"
  },
  "results": {
    "findings": [
      {
        "id": "BLOCK-001",
        "type": "blocker",
        "severity": "high",
        "description": "Required API specification not found",
        "recommendation": "Request API spec from Architect"
      }
    ]
  },
  "confidence": {
    "overall": 0.0
  }
}
```

---

## Message Type 3: ALERT

An ALERT message notifies of urgent issues requiring attention.

### Schema

```json
{
  "message_type": "ALERT",
  "alert_id": "ALT-YYYYMMDD-XXXXXX",
  "timestamp": "ISO8601",

  "severity": "critical|high|medium|low|info",
  "category": "security|availability|performance|compliance|quality",

  "routing": {
    "from_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name",
      "team": "Team Name"
    },
    "to_agents": [
      {
        "id": "TEAM-XXX",
        "name": "Agent Name",
        "team": "Team Name",
        "role": "primary|secondary|informed"
      }
    ]
  },

  "alert": {
    "title": "Alert title",
    "description": "Detailed description",
    "impact": "Description of impact",
    "affected_systems": ["List of affected systems"],
    "affected_users": "Scope of user impact"
  },

  "evidence": {
    "indicators": ["Specific indicators that triggered alert"],
    "logs": "Log references",
    "metrics": "Metric references"
  },

  "recommended_action": {
    "immediate": ["Immediate actions to take"],
    "investigation": ["Investigation steps"],
    "mitigation": ["Mitigation options"]
  },

  "escalation": {
    "auto_escalate_at": "ISO8601",
    "escalation_path": ["Agent IDs in escalation order"],
    "current_level": 1
  },

  "acknowledgment": {
    "required": true|false,
    "deadline": "ISO8601",
    "acknowledged_by": "Agent ID or null",
    "acknowledged_at": "ISO8601 or null"
  }
}
```

### Severity Levels and Auto-Escalation

| Severity | Description | Response SLA | Auto-Escalate If Unacknowledged |
|----------|-------------|--------------|----------------------------------|
| **Critical** | Immediate threat, active attack, data breach | 5 minutes | 10 minutes |
| **High** | Significant security or availability issue | 15 minutes | 30 minutes |
| **Medium** | Notable issue, potential impact | 1 hour | 2 hours |
| **Low** | Minor issue, limited impact | 4 hours | 8 hours |
| **Info** | Informational, no action required | N/A | Never |

### Alert Examples

#### Critical Security Alert
```json
{
  "message_type": "ALERT",
  "alert_id": "ALT-20240115-000001",
  "timestamp": "2024-01-15T10:30:00Z",
  "severity": "critical",
  "category": "security",
  "routing": {
    "from_agent": {"id": "SEC-004", "name": "Security Tester"},
    "to_agents": [
      {"id": "SEC-006", "name": "Incident Responder", "role": "primary"},
      {"id": "SEC-001", "name": "Security Architect", "role": "secondary"}
    ]
  },
  "alert": {
    "title": "SQL Injection Vulnerability Actively Exploited",
    "description": "Detected SQL injection attack patterns in production logs targeting user search endpoint",
    "impact": "Potential unauthorized database access",
    "affected_systems": ["api-prod-01", "api-prod-02"]
  },
  "recommended_action": {
    "immediate": ["Block attacking IPs", "Enable WAF rule SQLI-001"],
    "investigation": ["Review access logs", "Assess data exposure"]
  },
  "acknowledgment": {
    "required": true,
    "deadline": "2024-01-15T10:35:00Z"
  }
}
```

---

## Message Type 4: STATUS

A STATUS message shares progress on ongoing work.

### Schema

```json
{
  "message_type": "STATUS",
  "status_id": "STS-YYYYMMDD-XXXXXX",
  "request_id": "Original request ID",
  "timestamp": "ISO8601",

  "routing": {
    "from_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name"
    },
    "to_agents": ["Agent IDs interested in status"]
  },

  "progress": {
    "overall_percent": 0-100,
    "current_phase": "Phase name",
    "phases": [
      {
        "name": "Phase name",
        "status": "not_started|in_progress|completed|blocked",
        "percent_complete": 0-100
      }
    ]
  },

  "checkpoints": {
    "completed": ["Completed checkpoint names"],
    "current": "Current checkpoint",
    "remaining": ["Remaining checkpoints"]
  },

  "timeline": {
    "started_at": "ISO8601",
    "estimated_completion": "ISO8601",
    "confidence_in_estimate": "high|medium|low",
    "factors_affecting_estimate": ["Factors"]
  },

  "blockers": [
    {
      "id": "Blocker ID",
      "description": "Description",
      "impact": "Impact on timeline",
      "resolution_path": "How to resolve",
      "help_needed": true|false
    }
  ],

  "notes": "Additional context or notes"
}
```

### Status Example
```json
{
  "message_type": "STATUS",
  "status_id": "STS-20240115-000015",
  "request_id": "REQ-20240115-000042",
  "timestamp": "2024-01-15T16:00:00Z",
  "progress": {
    "overall_percent": 60,
    "current_phase": "Implementation",
    "phases": [
      {"name": "Design Review", "status": "completed", "percent_complete": 100},
      {"name": "Implementation", "status": "in_progress", "percent_complete": 60},
      {"name": "Testing", "status": "not_started", "percent_complete": 0}
    ]
  },
  "timeline": {
    "started_at": "2024-01-15T14:00:00Z",
    "estimated_completion": "2024-01-15T18:00:00Z",
    "confidence_in_estimate": "high"
  },
  "blockers": [],
  "notes": "On track, 3 of 5 endpoints complete"
}
```

---

## Message Type 5: QUERY

A QUERY message requests information without requiring action.

### Schema

```json
{
  "message_type": "QUERY",
  "query_id": "QRY-YYYYMMDD-XXXXXX",
  "timestamp": "ISO8601",

  "routing": {
    "from_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name"
    },
    "to_agent": {
      "id": "TEAM-XXX",
      "name": "Agent Name"
    }
  },

  "query": {
    "question": "The specific question being asked",
    "context": "Context for why this information is needed",
    "expected_format": "How the answer should be formatted",
    "urgency": "blocking|needed_soon|when_available"
  },

  "response_requirements": {
    "timeout": "Duration to wait for response",
    "fallback": "What to do if no response",
    "cache_allowed": true|false,
    "cache_ttl": "Duration if caching allowed"
  }
}
```

### Query Example
```json
{
  "message_type": "QUERY",
  "query_id": "QRY-20240115-000008",
  "timestamp": "2024-01-15T15:30:00Z",
  "routing": {
    "from_agent": {"id": "DEV-002", "name": "Backend Developer"},
    "to_agent": {"id": "INF-004", "name": "Database Administrator"}
  },
  "query": {
    "question": "What is the maximum connection pool size for the production PostgreSQL cluster?",
    "context": "Need to configure connection pool for new service",
    "expected_format": "Integer value with any relevant limits",
    "urgency": "needed_soon"
  },
  "response_requirements": {
    "timeout": "30 minutes",
    "fallback": "Use default of 20 connections",
    "cache_allowed": true,
    "cache_ttl": "24 hours"
  }
}
```

---

## Message Routing Rules

### Priority-Based Routing
- P0/P1: Direct delivery with acknowledgment required
- P2/P3: Standard queue processing
- P4: Batch processing allowed

### Cross-Team Routing
- Messages crossing team boundaries must CC the respective team leads
- Security-related messages always CC SEC-001

### Aggregation Rules
- Multiple alerts of same type within 5 minutes → Aggregate
- Status updates from parallel tasks → Aggregate before reporting
- Duplicate queries → Return cached response if available
