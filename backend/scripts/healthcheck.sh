#!/bin/bash
# =============================================================================
# HIVEMIND Backend Health Check Script
# =============================================================================
# This script checks if the HIVEMIND backend is healthy by:
# 1. Checking if the HTTP API is responding
# 2. Optionally checking database connectivity
# 3. Optionally checking critical services

set -e

# Configuration
HEALTH_ENDPOINT="${HIVEMIND_HEALTH_ENDPOINT:-http://localhost:8000/health}"
TIMEOUT="${HIVEMIND_HEALTH_TIMEOUT:-5}"

# =============================================================================
# Check HTTP Health Endpoint
# =============================================================================
if ! curl --silent --fail --max-time "$TIMEOUT" "$HEALTH_ENDPOINT" > /dev/null 2>&1; then
    echo "Health check failed: API endpoint not responding"
    exit 1
fi

# =============================================================================
# Optional: Check Database Connectivity
# =============================================================================
if [ "${HIVEMIND_HEALTHCHECK_DB:-false}" = "true" ]; then
    if ! pg_isready -h "${HIVEMIND_POSTGRES_HOST:-localhost}" \
                     -p "${HIVEMIND_POSTGRES_PORT:-5432}" \
                     -U "${HIVEMIND_POSTGRES_USER:-hivemind}" \
                     -t "$TIMEOUT" > /dev/null 2>&1; then
        echo "Health check failed: Database not responding"
        exit 1
    fi
fi

# =============================================================================
# Optional: Check Redis Connectivity
# =============================================================================
if [ "${HIVEMIND_HEALTHCHECK_REDIS:-false}" = "true" ]; then
    if ! timeout "$TIMEOUT" redis-cli -h "${HIVEMIND_REDIS_HOST:-localhost}" \
                                       -p "${HIVEMIND_REDIS_PORT:-6379}" \
                                       ping > /dev/null 2>&1; then
        echo "Health check failed: Redis not responding"
        exit 1
    fi
fi

# All checks passed
exit 0
