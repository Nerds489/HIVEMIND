# Changelog

All notable changes to HIVEMIND will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Web UI dashboard for monitoring agents
- Custom agent creation wizard
- Memory export/import functionality
- Kubernetes deployment manifests

---

## [2.0.0] - 2024-12-20

### Added

#### Python Backend
- **FastAPI REST API** with full OpenAPI documentation
- **WebSocket support** for real-time streaming responses
- **gRPC API** for high-performance inter-process communication
- **PostgreSQL database** with Alembic migrations
- **Qdrant vector database** for semantic memory search
- **Redis caching** and pub/sub messaging
- **RabbitMQ message queue** for agent coordination
- Multi-stage **Dockerfile** for optimized production builds

#### Observability Stack
- **Prometheus metrics** collection
- **Grafana dashboards** for visualization
- **Jaeger distributed tracing**
- **OpenTelemetry** instrumentation
- **Structured logging** with structlog
- Health check endpoints (`/health`, `/ready`)

#### Terminal User Interface (TUI)
- **Textual-based TUI** for terminal interaction
- Three-panel layout (Agents, Chat, Status)
- Real-time agent status monitoring
- Markdown rendering in chat
- Keyboard-driven navigation
- Dark/light mode toggle

#### Slash Commands
- `/hivemind` - Activate HIVEMIND orchestration
- `/architect` - System architecture agent
- `/dev` - Development team coordination
- `/sec` - Security team coordination
- `/infra` - Infrastructure team coordination
- `/qa` - QA team coordination
- `/pentest` - Penetration testing
- `/reviewer` - Code review
- `/sre` - Site reliability engineering
- `/incident` - Incident response
- `/sdlc` - Full SDLC pipeline

#### Docker Deployment
- Complete **docker-compose.yml** for full stack
- Service health checks with dependency ordering
- Persistent volumes for all data stores
- Optional monitoring profile (`--profile monitoring`)
- Production-ready configuration

#### Makefile Commands
- `make up` / `make down` - Start/stop services
- `make logs` - View logs
- `make health` - Check service health
- `make migrate` - Run database migrations
- `make test` - Run test suite
- `make monitoring-up` - Start with monitoring stack
- `make backup-db` / `make restore-db` - Database backup

#### API Middleware
- Rate limiting with configurable limits
- Request validation and sanitization
- CORS configuration
- Distributed tracing headers
- Request/response logging

#### Resilience Patterns
- Circuit breakers with pybreaker
- Retry logic with tenacity
- Dead letter queues for failed messages
- Graceful degradation

### Changed
- Upgraded from CLI-only to full backend architecture
- Memory system now supports vector search via Qdrant
- Agent coordination via message queues instead of direct calls
- Configuration via environment variables and TOML files

### Security
- JWT-based API authentication
- Request validation middleware
- Rate limiting per endpoint
- CORS origin restrictions
- Secrets management via environment variables

---

## [1.0.0] - 2024-12-19

### Added

#### Core System
- Multi-agent orchestration system with 24 specialized AI agents
- Dual-engine architecture: Codex (orchestrator) + Claude (agents)
- Intelligent task routing based on keywords and context
- Unified voice output - all agents speak as one coherent response

#### Agent Teams (24 Total)
- **Development Team** (6 agents): Architect, Backend Developer, Frontend Developer, Code Reviewer, Technical Writer, DevOps Liaison
- **Security Team** (6 agents): Security Architect, Penetration Tester, Malware Analyst, Wireless Security Expert, Compliance Auditor, Incident Responder
- **Infrastructure Team** (6 agents): Infrastructure Architect, Systems Administrator, Network Engineer, Database Administrator, Site Reliability Engineer, Automation Engineer
- **QA Team** (6 agents): QA Architect, Test Automation Engineer, Performance Tester, Security Tester, Manual QA Tester, Test Data Manager

#### Installation & Setup
- `setup.sh` - Complete one-command installer
- `bootstrap.sh` - Quick bootstrap wrapper
- Automatic Node.js installation (if needed)
- Automatic Codex CLI installation
- Automatic Claude Code CLI installation
- Interactive authentication wizard (browser OAuth or API key)
- Cross-platform support (Linux, macOS)

#### Configuration
- `config/engines.yaml` - Engine configuration with presets
- `config/hivemind.yaml` - System-wide settings
- `config/routing.yaml` - Task routing rules
- `config/agents.yaml` - Agent definitions
- Environment variable support via `.env` files
- Four engine presets: recommended, full-codex, full-claude, inverse

#### Memory System
- Persistent long-term memory (learnings, decisions, preferences)
- Short-term working memory for sessions
- Episodic memory for event tracking
- Per-agent memory isolation
- Team-shared memory pools
- Automatic memory triggers ("remember that...", "we decided...")

#### CLI Interface
- Interactive mode with REPL
- Direct task execution mode
- `--config` flag for viewing configuration
- `--status` flag for system status
- `--setup` flag for authentication wizard
- `--preset` flag for quick engine switching
- `hm` shorthand command

#### Workflows
- Full SDLC workflow
- Security assessment workflow
- Incident response workflow
- Code review workflow
- Infrastructure deployment workflow
- Compliance audit workflow

#### Documentation
- Comprehensive README with quick start
- Detailed setup guide
- Agent reference documentation
- Workflow documentation
- Template library for outputs

### Security
- No credentials stored in repository
- `.gitignore` configured for security
- `.env.example` template provided
- API keys stored locally only
- Session data excluded from version control

---

## [0.1.0] - 2024-12-17

### Added
- Initial project structure
- Basic agent definitions
- Proof of concept orchestration
- Memory system prototype

---

## Version History Notes

### Versioning Scheme
- **Major (X.0.0)**: Breaking changes, major architecture updates
- **Minor (0.X.0)**: New features, new agents, new workflows
- **Patch (0.0.X)**: Bug fixes, documentation updates, minor improvements

### Upgrade Guide

#### From 1.x to 2.x
1. Backup your `memory/` directory
2. Backup your `.env` file
3. Pull the new version
4. Install Docker and Docker Compose (required for backend)
5. Run `make up` to start the full stack
6. Your CLI will continue to work as before
7. Optionally install the TUI: `cd tui && pip install -e .`

#### From 0.x to 1.x
1. Backup your `memory/` directory
2. Pull the new version
3. Run `./setup.sh` to update dependencies
4. Memory files are forward-compatible

---

## Migration Notes

### Memory System (1.x → 2.x)
- Existing JSON memory files remain compatible
- New vector search requires Qdrant (auto-started with Docker)
- Memory operations now go through the API when using backend

### Configuration (1.x → 2.x)
- YAML configs remain in `config/`
- New environment variables for Docker services
- Copy `.env.production` to `.env` for Docker deployment

---

[Unreleased]: https://github.com/Nerds489/HIVEMIND/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Nerds489/HIVEMIND/releases/tag/v2.0.0
[1.0.0]: https://github.com/Nerds489/HIVEMIND/releases/tag/v1.0.0
[0.1.0]: https://github.com/Nerds489/HIVEMIND/releases/tag/v0.1.0
