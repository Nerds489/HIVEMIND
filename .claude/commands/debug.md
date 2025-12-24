# Debug Command

Debug and troubleshoot issues with HIVEMIND multi-agent routing.

## Usage

```
/debug [component] [issue]
```

## Components

- `routing` - Agent routing and task dispatch
- `memory` - Memory system operations
- `engine` - AI engine connectivity
- `agents` - Agent status and health
- `all` - Full system diagnostic

## Examples

```
/debug routing "Tasks not reaching correct agent"
/debug memory "Memories not persisting"
/debug engine "Claude CLI not responding"
/debug agents "Some agents seem inactive"
/debug all
```

## Behavior

This command activates diagnostic mode:

1. **Routing Debug**: Shows task classification, keyword matching, agent selection
2. **Memory Debug**: Tests read/write operations, checks file permissions
3. **Engine Debug**: Verifies CLI availability, API connectivity
4. **Agent Debug**: Lists all 24 agents with status
5. **Full Debug**: Runs all diagnostics in sequence

## Output Format

```
━━━ HIVEMIND DIAGNOSTIC ━━━
Component: [component]
Status: [OK/WARNING/ERROR]

Checks performed:
✓ Check 1 passed
✓ Check 2 passed
✗ Check 3 failed: [reason]

Recommendations:
• [Fix suggestion 1]
• [Fix suggestion 2]
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Integration

When this command runs, internally:
- DEV-001 (Architect) analyzes system design issues
- INF-005 (SRE) investigates reliability problems
- DEV-006 (DevOps) checks CI/CD and deployment

The response is unified - user sees troubleshooting steps, not agent coordination.
