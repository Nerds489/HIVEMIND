# HIVEMIND Deployment Guide

Phase 12 deployment configuration for production and development environments.

## Quick Start

### Development

```bash
# 1. Start all services
make up

# 2. View logs
make logs

# 3. Check health
make health
```

### Production

```bash
# 1. Configure environment
cp .env.production .env
# Edit .env and set all CHANGE-ME values

# 2. Deploy
make deploy-prod

# 3. Verify deployment
make status
make health
```

## Files Overview

### Root Directory

- **docker-compose.yml** - Full stack orchestration
  - Backend service (builds from backend/)
  - PostgreSQL (with persistent volume)
  - Redis (cache & pub/sub)
  - Qdrant (vector database)
  - RabbitMQ (message queue)
  - Prometheus/Grafana/Jaeger (optional monitoring)

- **.env.production** - Production environment template
  - All HIVEMIND_* configuration variables
  - Database credentials
  - API keys (must be set!)
  - Security settings
  - Feature flags

- **Makefile** - Deployment commands
  - `make up/down/restart` - Service management
  - `make logs` - View logs
  - `make shell` - Container access
  - `make migrate` - Database migrations
  - `make health` - Health checks
  - `make backup-db/restore-db` - Backup operations

### Backend Directory

- **backend/Dockerfile** - Multi-stage production build
  - Stage 1: Builder (dependencies)
  - Stage 2: Production (minimal runtime)
  - Stage 3: Development (dev tools)

- **backend/scripts/start.sh** - Startup orchestration
  - Waits for PostgreSQL
  - Waits for Redis
  - Waits for RabbitMQ
  - Runs Alembic migrations
  - Starts Uvicorn server

- **backend/scripts/healthcheck.sh** - Health check script
  - HTTP endpoint check
  - Optional database check
  - Optional Redis check

- **backend/alembic.ini** - Alembic migration config (already exists)

- **backend/migrations/env.py** - Alembic environment (already exists)

## Common Commands

### Service Management

```bash
make up              # Start all services
make up-build        # Build and start
make down            # Stop all services
make restart         # Restart all services
make restart-backend # Restart only backend
make ps              # Show running containers
make status          # Show service health
```

### Logs

```bash
make logs            # All services
make logs-backend    # Backend only
make logs-postgres   # PostgreSQL only
make logs-redis      # Redis only
make logs-rabbitmq   # RabbitMQ only
make logs-qdrant     # Qdrant only
```

### Shell Access

```bash
make shell           # Backend bash shell
make shell-postgres  # PostgreSQL psql
make shell-redis     # Redis CLI
```

### Database Migrations

```bash
make migrate                        # Run pending migrations
make migrate-create MSG="add users" # Create new migration
make migrate-history                # Show migration history
make migrate-current                # Show current version
make migrate-downgrade              # Downgrade one version
```

### Development

```bash
make test            # Run tests
make test-coverage   # Run with coverage
make lint            # Run linting
make format          # Format code
make typecheck       # Type checking
```

### Monitoring

```bash
make monitoring-up   # Start with monitoring stack
make monitoring-down # Stop monitoring

# Access monitoring tools:
# Grafana:    http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
# Jaeger:     http://localhost:16686
```

### Backup & Restore

```bash
make backup-db       # Backup database to backups/
make restore-db FILE=backups/hivemind_20231201_120000.sql.gz
```

### Health Checks

```bash
make health          # Check all services
make env-check       # Validate environment config
```

### Cleanup

```bash
make clean           # Remove stopped containers
make clean-all       # Remove everything (WARNING!)
make down-volumes    # Stop and remove volumes (WARNING!)
```

## Environment Configuration

### Required Variables

Must be set before deployment:

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Database Password
POSTGRES_PASSWORD=strong-random-password

# RabbitMQ Password
RABBITMQ_PASSWORD=strong-random-password

# JWT Secret (min 64 chars)
HIVEMIND_SECURITY_JWT_SECRET_KEY=... (use: openssl rand -base64 64)

# Grafana Password
GRAFANA_PASSWORD=strong-password
```

### Optional Tuning

```bash
# Workers
HIVEMIND_WORKERS=4

# Database Pool
HIVEMIND_DB_POOL_SIZE=20
HIVEMIND_DB_MAX_OVERFLOW=10

# Redis Pool
HIVEMIND_REDIS_POOL_SIZE=10

# Rate Limiting
HIVEMIND_SECURITY_RATE_LIMIT_REQUESTS=100
HIVEMIND_SECURITY_RATE_LIMIT_WINDOW=60

# CORS Origins
HIVEMIND_SECURITY_CORS_ORIGINS=https://yourdomain.com
```

## Service Ports

- **8000** - Backend HTTP API
- **50051** - Backend gRPC API
- **5432** - PostgreSQL
- **6333** - Qdrant HTTP API
- **6334** - Qdrant gRPC API
- **6379** - Redis
- **5672** - RabbitMQ AMQP
- **15672** - RabbitMQ Management UI
- **9090** - Prometheus (monitoring profile)
- **3000** - Grafana (monitoring profile)
- **16686** - Jaeger UI (monitoring profile)

## Docker Volumes

Persistent data stored in:

- **postgres_data** - PostgreSQL database
- **qdrant_data** - Vector database storage
- **qdrant_snapshots** - Vector database snapshots
- **redis_data** - Redis persistence
- **rabbitmq_data** - RabbitMQ data
- **hivemind_logs** - Application logs
- **prometheus_data** - Metrics (monitoring)
- **grafana_data** - Dashboards (monitoring)

## Production Checklist

Before deploying to production:

1. Environment Configuration
   - [ ] Copy `.env.production` to `.env`
   - [ ] Set all API keys
   - [ ] Generate strong passwords
   - [ ] Generate JWT secret (min 64 chars)
   - [ ] Configure CORS origins
   - [ ] Review feature flags

2. Security
   - [ ] Change all default passwords
   - [ ] Enable HTTPS/TLS (use reverse proxy)
   - [ ] Configure firewall rules
   - [ ] Set up backup strategy
   - [ ] Review rate limits

3. Monitoring
   - [ ] Enable observability (tracing/metrics)
   - [ ] Configure alerting
   - [ ] Set up log aggregation
   - [ ] Test health checks

4. Database
   - [ ] Review connection pool settings
   - [ ] Configure backup schedule
   - [ ] Test restore procedure
   - [ ] Review retention policies

5. Deployment
   - [ ] Test in staging environment
   - [ ] Run smoke tests
   - [ ] Verify all services healthy
   - [ ] Monitor logs for errors

## Troubleshooting

### Services won't start

```bash
# Check logs
make logs

# Check specific service
make logs-backend
make logs-postgres

# Verify environment
make env-check

# Check service status
make status
```

### Database connection errors

```bash
# Check PostgreSQL is ready
make shell-postgres

# Verify migrations
make migrate-current
make migrate-history

# Check connection pool
make inspect-backend | grep POSTGRES
```

### Health checks failing

```bash
# Manual health check
curl http://localhost:8000/health

# Check all services
make health

# Inspect container
docker-compose exec hivemind ps aux
```

### Migration errors

```bash
# Check current version
make migrate-current

# View migration history
make migrate-history

# Downgrade if needed
make migrate-downgrade

# Re-run migrations
make migrate
```

### Performance issues

```bash
# Check resource usage
make stats

# Review logs
make logs-backend

# Increase workers (in .env)
HIVEMIND_WORKERS=8

# Tune database pool (in .env)
HIVEMIND_DB_POOL_SIZE=30
HIVEMIND_DB_MAX_OVERFLOW=20
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   HIVEMIND Backend                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Uvicorn Workers (4)                                   │   │
│  │ - HTTP API (8000)                                     │   │
│  │ - gRPC API (50051)                                    │   │
│  │ - WebSocket Support                                   │   │
│  └──────────────────────────────────────────────────────┘   │
└──────┬──────┬──────┬──────┬──────────────────────────────────┘
       │      │      │      │
       │      │      │      └──────────────┐
       │      │      │                     │
┌──────▼──────▼──────▼──────┐    ┌─────────▼─────────┐
│     PostgreSQL (5432)      │    │  Qdrant (6333)    │
│  - Relational Data         │    │  - Vector Memory  │
│  - Persistent Volume       │    │  - Embeddings     │
└────────────────────────────┘    └───────────────────┘
       │                                   │
┌──────▼──────────────┐          ┌────────▼──────────┐
│   Redis (6379)      │          │ RabbitMQ (5672)   │
│  - Cache            │          │ - Message Queue   │
│  - Pub/Sub          │          │ - Agent Comms     │
└─────────────────────┘          └───────────────────┘
```

## Next Steps

1. Review `.env.production` and customize for your environment
2. Set up CI/CD pipeline (GitHub Actions recommended)
3. Configure monitoring and alerting
4. Set up automated backups
5. Document runbook for incident response
6. Implement zero-downtime deployment strategy
7. Set up staging environment

For more information, see:
- Backend API: `backend/README.md`
- Configuration: `backend/hivemind.toml`
- Development: `CONTRIBUTING.md`
