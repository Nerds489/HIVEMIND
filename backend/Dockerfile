# =============================================================================
# HIVEMIND Backend - Production Dockerfile
# =============================================================================
# Multi-stage build for minimal production image

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS builder

# Prevent Python from writing bytecode and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
WORKDIR /build
COPY pyproject.toml ./
RUN pip install --upgrade pip setuptools wheel && \
    pip install .

# -----------------------------------------------------------------------------
# Stage 2: Production
# -----------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS production

# Labels
LABEL org.opencontainers.image.title="HIVEMIND Backend" \
      org.opencontainers.image.description="Multi-agent AI orchestration system" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="HIVEMIND Contributors" \
      org.opencontainers.image.licenses="MIT"

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/opt/venv/bin:$PATH" \
    HIVEMIND_ENV=production \
    HIVEMIND_LOG_LEVEL=INFO

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 hivemind \
    && useradd --uid 1000 --gid hivemind --shell /bin/bash --create-home hivemind

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=hivemind:hivemind src/ ./src/
COPY --chown=hivemind:hivemind proto/ ./proto/
COPY --chown=hivemind:hivemind alembic.ini ./
COPY --chown=hivemind:hivemind migrations/ ./migrations/
COPY --chown=hivemind:hivemind scripts/ ./scripts/

# Create directories for logs and runtime data
RUN mkdir -p /app/logs /app/data && \
    chown -R hivemind:hivemind /app && \
    chmod +x /app/scripts/*.sh

# Switch to non-root user
USER hivemind

# Expose ports
EXPOSE 8000 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD /app/scripts/healthcheck.sh

# Default command (use startup script)
CMD ["/app/scripts/start.sh"]

# -----------------------------------------------------------------------------
# Stage 3: Development
# -----------------------------------------------------------------------------
FROM production AS development

USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install dev dependencies
RUN pip install pytest pytest-asyncio pytest-cov ruff mypy

USER hivemind

# Override command for development
CMD ["uvicorn", "hivemind.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
