# HIVEMIND Changelog

## [2.0.0] - Minimal Output Edition

### Added
- **HEAD_CODEX** - Master orchestration intelligence with consolidated reporting
- **Minimal Output Protocol** - All agents report in 2-4 words maximum
- **Quality Gates Display** - Visible gate status updates (G1-G5)
- **Consolidated Reports** - Single comprehensive report per task
- **Status Templates** - Pre-defined status phrases for each agent
- **Report Templates** - Standardized report formats

### Changed
- Agent output reduced from verbose explanations to 2-4 word status
- COORDINATOR upgraded to enforce minimal output
- Internal handoffs now invisible to user
- Reporting moved from per-agent to consolidated HEAD_CODEX reports

### Removed
- Verbose agent reasoning output
- Step-by-step narration
- Per-agent progress reports

### Technical
- New `output_rules` in settings.json
- Agent `status_templates` in agents.json
- MINIMAL_OUTPUT.md protocol specification
- HEAD_CODEX.md orchestrator specification

## [1.0.0] - Initial Release

### Added
- 24 specialized AI agents
- 4 functional teams (DEV, SEC, INF, QA)
- COORDINATOR orchestration
- Slash commands integration
- Workflow definitions
- Quality gates
- Persistent memory

---

## Version Numbering

HIVEMIND follows semantic versioning:
- **MAJOR** - Breaking changes to output format or architecture
- **MINOR** - New agents, workflows, or features
- **PATCH** - Bug fixes and minor improvements
