# =============================================================================
# HIVEMIND Makefile
# =============================================================================
# Common deployment and development commands for HIVEMIND

.PHONY: help up down restart logs shell migrate build clean ps health status

# Default target
.DEFAULT_GOAL := help

# =============================================================================
# Help
# =============================================================================
help: ## Show this help message
	@echo "HIVEMIND Deployment Commands"
	@echo "============================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# Docker Compose Commands
# =============================================================================
up: ## Start all services
	docker-compose up -d
	@echo "Services started. Waiting for health checks..."
	@sleep 5
	@make status

up-build: ## Build and start all services
	docker-compose up -d --build
	@echo "Services built and started. Waiting for health checks..."
	@sleep 5
	@make status

down: ## Stop all services
	docker-compose down

down-volumes: ## Stop all services and remove volumes (WARNING: deletes data!)
	@echo "WARNING: This will delete all volumes and data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
	fi

restart: ## Restart all services
	docker-compose restart

restart-backend: ## Restart only the backend service
	docker-compose restart hivemind

# =============================================================================
# Logs
# =============================================================================
logs: ## Tail logs from all services
	docker-compose logs -f

logs-backend: ## Tail logs from backend only
	docker-compose logs -f hivemind

logs-postgres: ## Tail logs from PostgreSQL
	docker-compose logs -f postgres

logs-redis: ## Tail logs from Redis
	docker-compose logs -f redis

logs-rabbitmq: ## Tail logs from RabbitMQ
	docker-compose logs -f rabbitmq

logs-qdrant: ## Tail logs from Qdrant
	docker-compose logs -f qdrant

# =============================================================================
# Shell Access
# =============================================================================
shell: ## Open a shell in the backend container
	docker-compose exec hivemind /bin/bash

shell-postgres: ## Open psql in the PostgreSQL container
	docker-compose exec postgres psql -U hivemind -d hivemind

shell-redis: ## Open redis-cli in the Redis container
	docker-compose exec redis redis-cli

# =============================================================================
# Database Migrations
# =============================================================================
migrate: ## Run database migrations
	docker-compose exec hivemind alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MSG="description")
	@if [ -z "$(MSG)" ]; then \
		echo "Error: MSG is required. Usage: make migrate-create MSG=\"description\""; \
		exit 1; \
	fi
	docker-compose exec hivemind alembic revision --autogenerate -m "$(MSG)"

migrate-downgrade: ## Downgrade database by one revision
	docker-compose exec hivemind alembic downgrade -1

migrate-history: ## Show migration history
	docker-compose exec hivemind alembic history

migrate-current: ## Show current migration version
	docker-compose exec hivemind alembic current

# =============================================================================
# Build & Development
# =============================================================================
build: ## Build all Docker images
	docker-compose build

build-backend: ## Build only the backend image
	docker-compose build hivemind

build-no-cache: ## Build all images without cache
	docker-compose build --no-cache

# =============================================================================
# Status & Health
# =============================================================================
ps: ## Show running containers
	docker-compose ps

status: ## Show service health status
	@echo "Service Health Status:"
	@echo "====================="
	@docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

health: ## Check health of all services
	@echo "Checking service health..."
	@echo ""
	@echo "Backend API:"
	@curl -sf http://localhost:8000/health && echo "  ✓ Healthy" || echo "  ✗ Unhealthy"
	@echo ""
	@echo "PostgreSQL:"
	@docker-compose exec -T postgres pg_isready -U hivemind && echo "  ✓ Ready" || echo "  ✗ Not ready"
	@echo ""
	@echo "Redis:"
	@docker-compose exec -T redis redis-cli ping && echo "  ✓ Responding" || echo "  ✗ Not responding"
	@echo ""
	@echo "Qdrant:"
	@curl -sf http://localhost:6333/health && echo "  ✓ Healthy" || echo "  ✗ Unhealthy"
	@echo ""
	@echo "RabbitMQ:"
	@curl -sf -u hivemind:$${RABBITMQ_PASSWORD:-hivemind_secret} http://localhost:15672/api/healthchecks/node && echo "  ✓ Healthy" || echo "  ✗ Unhealthy"

# =============================================================================
# Cleanup
# =============================================================================
clean: ## Remove stopped containers and dangling images
	docker-compose down --remove-orphans
	docker system prune -f

clean-all: ## Remove all containers, images, and volumes (WARNING: deletes everything!)
	@echo "WARNING: This will delete all containers, images, and volumes!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v --rmi all --remove-orphans; \
		docker system prune -af; \
	fi

# =============================================================================
# Backup & Restore
# =============================================================================
backup-db: ## Backup PostgreSQL database
	@mkdir -p backups
	@echo "Creating database backup..."
	docker-compose exec -T postgres pg_dump -U hivemind hivemind | gzip > backups/hivemind_$$(date +%Y%m%d_%H%M%S).sql.gz
	@echo "Backup created in backups/"

restore-db: ## Restore PostgreSQL database (usage: make restore-db FILE=backups/hivemind_20231201_120000.sql.gz)
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE is required. Usage: make restore-db FILE=backups/hivemind_YYYYMMDD_HHMMSS.sql.gz"; \
		exit 1; \
	fi
	@echo "Restoring database from $(FILE)..."
	gunzip < $(FILE) | docker-compose exec -T postgres psql -U hivemind -d hivemind
	@echo "Database restored successfully!"

# =============================================================================
# Monitoring (requires monitoring profile)
# =============================================================================
monitoring-up: ## Start services with monitoring stack
	docker-compose --profile monitoring up -d
	@echo "Services started with monitoring. Access:"
	@echo "  Grafana:    http://localhost:3000 (admin/admin)"
	@echo "  Prometheus: http://localhost:9090"
	@echo "  Jaeger:     http://localhost:16686"

monitoring-down: ## Stop monitoring stack
	docker-compose --profile monitoring down

# =============================================================================
# Testing & Quality
# =============================================================================
test: ## Run backend tests in container
	docker-compose exec hivemind pytest

test-coverage: ## Run tests with coverage report
	docker-compose exec hivemind pytest --cov=hivemind --cov-report=html --cov-report=term

lint: ## Run linting checks
	docker-compose exec hivemind ruff check .

format: ## Format code
	docker-compose exec hivemind ruff format .

typecheck: ## Run type checking
	docker-compose exec hivemind mypy src/

# =============================================================================
# Production Deployment
# =============================================================================
deploy-prod: ## Deploy to production (loads .env.production)
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.production..."; \
		cp .env.production .env; \
		echo ""; \
		echo "IMPORTANT: Edit .env and set all required values before deploying!"; \
		echo ""; \
		exit 1; \
	fi
	docker-compose up -d --build
	@echo "Production deployment started!"

# =============================================================================
# Utilities
# =============================================================================
env-check: ## Check if required environment variables are set
	@echo "Checking environment configuration..."
	@if [ ! -f .env ]; then \
		echo "  ✗ .env file not found"; \
		echo "    Run: cp .env.production .env"; \
		exit 1; \
	else \
		echo "  ✓ .env file exists"; \
	fi
	@grep -q "CHANGE-ME" .env && echo "  ✗ .env contains placeholder values (CHANGE-ME)" || echo "  ✓ .env appears configured"
	@grep -q "your-.*-api-key" .env && echo "  ✗ .env contains placeholder API keys" || echo "  ✓ API keys appear configured"

stats: ## Show Docker resource usage
	docker stats --no-stream

volumes: ## List all volumes
	docker volume ls

networks: ## List all networks
	docker network ls

inspect-backend: ## Inspect backend container configuration
	docker-compose exec hivemind env | grep HIVEMIND
