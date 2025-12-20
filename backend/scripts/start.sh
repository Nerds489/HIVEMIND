#!/bin/bash
# =============================================================================
# HIVEMIND Backend Startup Script
# =============================================================================
# This script:
# 1. Waits for all required services (postgres, redis, rabbitmq)
# 2. Runs database migrations
# 3. Starts the uvicorn server

set -e

echo "============================================================================="
echo "HIVEMIND Backend Starting..."
echo "============================================================================="

# Configuration
MAX_RETRIES=30
RETRY_INTERVAL=2

# =============================================================================
# Wait for PostgreSQL
# =============================================================================
echo "Waiting for PostgreSQL..."
for i in $(seq 1 $MAX_RETRIES); do
    if pg_isready -h "${HIVEMIND_POSTGRES_HOST:-localhost}" \
                   -p "${HIVEMIND_POSTGRES_PORT:-5432}" \
                   -U "${HIVEMIND_POSTGRES_USER:-hivemind}" > /dev/null 2>&1; then
        echo "PostgreSQL is ready!"
        break
    fi

    if [ "$i" -eq "$MAX_RETRIES" ]; then
        echo "ERROR: PostgreSQL failed to become ready after $MAX_RETRIES attempts"
        exit 1
    fi

    echo "PostgreSQL not ready yet (attempt $i/$MAX_RETRIES)..."
    sleep $RETRY_INTERVAL
done

# =============================================================================
# Wait for Redis
# =============================================================================
echo "Waiting for Redis..."
for i in $(seq 1 $MAX_RETRIES); do
    if redis-cli -h "${HIVEMIND_REDIS_HOST:-localhost}" \
                 -p "${HIVEMIND_REDIS_PORT:-6379}" \
                 ping > /dev/null 2>&1; then
        echo "Redis is ready!"
        break
    fi

    if [ "$i" -eq "$MAX_RETRIES" ]; then
        echo "ERROR: Redis failed to become ready after $MAX_RETRIES attempts"
        exit 1
    fi

    echo "Redis not ready yet (attempt $i/$MAX_RETRIES)..."
    sleep $RETRY_INTERVAL
done

# =============================================================================
# Wait for RabbitMQ
# =============================================================================
echo "Waiting for RabbitMQ..."
for i in $(seq 1 $MAX_RETRIES); do
    if rabbitmq-diagnostics -q ping > /dev/null 2>&1; then
        echo "RabbitMQ is ready!"
        break
    fi

    if [ "$i" -eq "$MAX_RETRIES" ]; then
        echo "ERROR: RabbitMQ failed to become ready after $MAX_RETRIES attempts"
        exit 1
    fi

    echo "RabbitMQ not ready yet (attempt $i/$MAX_RETRIES)..."
    sleep $RETRY_INTERVAL
done

# =============================================================================
# Run Database Migrations
# =============================================================================
echo "Running database migrations..."
if ! alembic upgrade head; then
    echo "ERROR: Database migration failed"
    exit 1
fi
echo "Database migrations completed successfully!"

# =============================================================================
# Start Uvicorn Server
# =============================================================================
echo "Starting Uvicorn server..."
echo "Environment: ${HIVEMIND_ENV:-production}"
echo "Log Level: ${HIVEMIND_LOG_LEVEL:-INFO}"
echo "Workers: ${HIVEMIND_WORKERS:-4}"
echo "============================================================================="

exec uvicorn hivemind.api.server:app \
    --host 0.0.0.0 \
    --port "${HIVEMIND_PORT:-8000}" \
    --workers "${HIVEMIND_WORKERS:-4}" \
    --log-level "${HIVEMIND_LOG_LEVEL:-info}" \
    --no-access-log
