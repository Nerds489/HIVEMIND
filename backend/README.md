# HIVEMIND Backend

Production-grade multi-agent AI orchestration system.

**24 Agents | 4 Teams | 1 Unified Intelligence**

## Overview

The HIVEMIND Backend is a Python-based orchestration layer that coordinates 24 specialized AI agents across 4 functional teams:

- **Development (DEV)**: Architecture, Backend, Frontend, Code Review, Documentation, DevOps
- **Security (SEC)**: Security Architecture, Pentesting, Malware Analysis, Wireless, Compliance, Incident Response
- **Infrastructure (INF)**: Cloud Architecture, Systems Admin, Networking, DBA, SRE, Automation
- **QA**: Test Strategy, Test Automation, Performance, Security Testing, Manual QA, Test Data

## Technology Stack

- **Runtime**: Python 3.11+
- **API**: FastAPI + WebSocket + gRPC
- **IPC**: ZeroMQ, Redis Pub/Sub, RabbitMQ
- **Databases**: PostgreSQL, Qdrant (Vector), Redis (Cache)
- **Resilience**: Tenacity, pybreaker, Dead Letter Queue
- **Observability**: structlog, Prometheus, OpenTelemetry

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Claude Code CLI (`claude`)
- OpenAI Codex CLI (`codex`) [optional]

### Installation

```bash
# Clone and navigate
cd hivemind/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Copy environment config
cp .env.example .env
# Edit .env with your API keys
```

### Start Infrastructure

```bash
# Start PostgreSQL, Qdrant, Redis, RabbitMQ
docker compose up -d postgres qdrant redis rabbitmq

# Run database migrations
alembic upgrade head
```

### Run the Server

```bash
# Development mode with auto-reload
uvicorn hivemind.api.server:app --reload --port 8000

# Or use the CLI
hivemind-server
```

### Using the CLI

```bash
# Check status
hivemind status

# List agents
hivemind agents

# View configuration
hivemind config
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |
| GET | `/metrics` | Prometheus metrics |
| POST | `/v1/sessions` | Create session |
| POST | `/v1/completions` | Send prompt |
| GET | `/v1/agents` | List agents |
| WS | `/v1/stream` | Streaming interface |

## Configuration

Configuration is loaded from (in order of priority):
1. Environment variables (`HIVEMIND_*`)
2. `.env` file
3. `hivemind.toml` config file
4. Default values

See `src/hivemind/config.py` for all options.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                               │
│  ┌─────────┐  ┌───────────┐  ┌──────┐                       │
│  │  REST   │  │ WebSocket │  │ gRPC │                       │
│  └────┬────┘  └─────┬─────┘  └──┬───┘                       │
├───────┴─────────────┴───────────┴───────────────────────────┤
│                    Orchestration Layer                       │
│  ┌─────────────┐  ┌────────┐  ┌────────────┐               │
│  │ Coordinator │──│ Router │──│ Dispatcher │               │
│  └──────┬──────┘  └────────┘  └─────┬──────┘               │
├─────────┴───────────────────────────┴───────────────────────┤
│                    Agent Execution Layer                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Agent Pool (24 Agents)                  │    │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                │    │
│  │  │ DEV │  │ SEC │  │ INF │  │ QA  │                │    │
│  │  │ (6) │  │ (6) │  │ (6) │  │ (6) │                │    │
│  │  └─────┘  └─────┘  └─────┘  └─────┘                │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                      IPC Layer                               │
│  ┌────────┐  ┌─────────────┐  ┌──────────┐                 │
│  │ ZeroMQ │  │ Redis PubSub│  │ RabbitMQ │                 │
│  └────────┘  └─────────────┘  └──────────┘                 │
├─────────────────────────────────────────────────────────────┤
│                    Persistence Layer                         │
│  ┌────────────┐  ┌────────┐  ┌───────┐                     │
│  │ PostgreSQL │  │ Qdrant │  │ Redis │                     │
│  │ (Relation) │  │(Vector)│  │(Cache)│                     │
│  └────────────┘  └────────┘  └───────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
ruff format src

# Lint
ruff check src

# Type check
mypy src
```

## License

MIT License - See LICENSE file
