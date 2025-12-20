"""
HIVEMIND Configuration System

Pydantic-based configuration with environment variable and TOML file support.
Hierarchical configuration for all system components.
"""

from __future__ import annotations

import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

import toml
from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Deployment environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(str, Enum):
    """Log level options."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# =============================================================================
# Component Configurations
# =============================================================================

class ClaudeConfig(BaseSettings):
    """Claude CLI configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_CLAUDE_")

    enabled: bool = True
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 8192
    timeout_seconds: float = 300.0
    api_key: SecretStr | None = Field(default=None, alias="ANTHROPIC_API_KEY")

    # CLI-specific settings
    cli_path: str = "claude"
    output_format: str = "stream-json"
    allowed_tools: list[str] = Field(default_factory=lambda: [
        "Read", "Write", "Edit", "Bash", "Glob", "Grep"
    ])


class CodexConfig(BaseSettings):
    """OpenAI Codex CLI configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_CODEX_")

    enabled: bool = True
    model: str = "o4-mini"
    max_tokens: int = 8192
    timeout_seconds: float = 300.0
    api_key: SecretStr | None = Field(default=None, alias="OPENAI_API_KEY")

    # CLI-specific settings
    cli_path: str = "codex"


class PostgresConfig(BaseSettings):
    """PostgreSQL database configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_POSTGRES_")

    host: str = "localhost"
    port: int = 5432
    database: str = Field(default="hivemind", alias="db")
    user: str = "hivemind"
    password: SecretStr = Field(default=SecretStr("hivemind_secret"))

    # Connection pool settings
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: float = 30.0
    pool_recycle: int = 1800

    # SSL settings
    ssl_mode: str = "prefer"

    @property
    def async_url(self) -> str:
        """Get async database URL."""
        password = self.password.get_secret_value()
        return f"postgresql+asyncpg://{self.user}:{password}@{self.host}:{self.port}/{self.database}"

    @property
    def sync_url(self) -> str:
        """Get sync database URL (for Alembic)."""
        password = self.password.get_secret_value()
        return f"postgresql://{self.user}:{password}@{self.host}:{self.port}/{self.database}"


class QdrantConfig(BaseSettings):
    """Qdrant vector database configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_QDRANT_")

    host: str = "localhost"
    port: int = 6333
    grpc_port: int = 6334
    api_key: SecretStr | None = None
    https: bool = False

    # Collection settings
    default_vector_size: int = 1536  # OpenAI ada-002 dimensions
    distance_metric: str = "Cosine"

    # Collections
    conversations_collection: str = "hivemind_conversations"
    code_snippets_collection: str = "hivemind_code_snippets"
    documentation_collection: str = "hivemind_documentation"


class RedisConfig(BaseSettings):
    """Redis cache and pub/sub configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_REDIS_")

    host: str = "localhost"
    port: int = 6379
    password: SecretStr | None = None
    database: int = Field(default=0, alias="db")

    # Connection settings
    max_connections: int = 50
    socket_timeout: float = 5.0
    socket_connect_timeout: float = 5.0
    retry_on_timeout: bool = True

    # Cache settings
    default_ttl: int = 3600  # 1 hour
    session_ttl: int = 86400  # 24 hours

    # Key prefixes
    key_prefix: str = "hivemind:"

    @property
    def url(self) -> str:
        """Get Redis URL."""
        if self.password:
            return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"
        return f"redis://{self.host}:{self.port}/{self.database}"


class RabbitMQConfig(BaseSettings):
    """RabbitMQ message queue configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_RABBITMQ_")

    host: str = "localhost"
    port: int = 5672
    user: str = "hivemind"
    password: SecretStr = Field(default=SecretStr("hivemind_secret"))
    vhost: str = "hivemind"

    # Connection settings
    connection_timeout: float = 10.0
    heartbeat: int = 60

    # Queue settings
    task_queue: str = "hivemind.tasks"
    dlq_queue: str = "hivemind.tasks.dlq"
    event_exchange: str = "hivemind.events"

    # Message settings
    message_ttl: int = 86400000  # 24 hours in ms
    max_retries: int = 3

    @property
    def url(self) -> str:
        """Get RabbitMQ URL."""
        password = self.password.get_secret_value()
        return f"amqp://{self.user}:{password}@{self.host}:{self.port}/{self.vhost}"


class ZeroMQConfig(BaseSettings):
    """ZeroMQ IPC configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_ZMQ_")

    router_endpoint: str = "tcp://127.0.0.1:5555"
    dealer_endpoint: str = "tcp://127.0.0.1:5556"

    # Socket settings
    high_water_mark: int = 1000
    linger: int = 0
    recv_timeout: int = 5000  # ms
    send_timeout: int = 5000  # ms

    # Heartbeat settings
    heartbeat_interval: int = 1000  # ms
    heartbeat_timeout: int = 5000  # ms


class ConcurrencyConfig(BaseSettings):
    """Concurrency control configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_CONCURRENCY_")

    # Global limits
    max_global_concurrent: int = 10
    max_per_team: int = 5
    max_per_agent: int = 1

    # Queue settings
    task_queue_size: int = 1000
    priority_levels: int = 5

    # Timeout settings
    default_task_timeout: float = 300.0  # 5 minutes
    max_task_timeout: float = 1800.0  # 30 minutes


class ResilienceConfig(BaseSettings):
    """Resilience and fault tolerance configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_RESILIENCE_")

    # Retry settings
    max_retries: int = 3
    retry_base_delay: float = 1.0
    retry_max_delay: float = 60.0
    retry_exponential_base: float = 2.0
    retry_jitter: bool = True

    # Circuit breaker settings
    circuit_failure_threshold: int = 5
    circuit_recovery_timeout: float = 30.0
    circuit_expected_exception: str = "Exception"

    # Checkpoint settings
    checkpoint_enabled: bool = True
    checkpoint_interval: int = 60  # seconds
    checkpoint_retention: int = 86400  # 24 hours


class SecurityConfig(BaseSettings):
    """Security configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_SECURITY_")

    # JWT settings
    jwt_secret_key: SecretStr = Field(default=SecretStr("CHANGE_ME_IN_PRODUCTION"))
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds

    # Vault settings (optional)
    vault_enabled: bool = False
    vault_url: str = "http://localhost:8200"
    vault_token: SecretStr | None = None
    vault_mount_point: str = "secret"

    # API key settings
    api_key_header: str = "X-API-Key"
    api_keys_enabled: bool = False


class ObservabilityConfig(BaseSettings):
    """Observability and monitoring configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_OBSERVABILITY_")

    # Logging
    log_level: LogLevel = LogLevel.INFO
    log_format: str = "json"  # json or console
    log_file: str | None = None

    # Metrics
    metrics_enabled: bool = True
    metrics_port: int = 9090
    metrics_path: str = "/metrics"

    # Tracing
    tracing_enabled: bool = True
    tracing_exporter: str = "otlp"  # otlp, jaeger, zipkin
    tracing_endpoint: str = "http://localhost:4317"
    tracing_sample_rate: float = 1.0

    # Service info
    service_name: str = "hivemind"
    service_version: str = "2.0.0"


class APIConfig(BaseSettings):
    """API server configuration."""

    model_config = SettingsConfigDict(env_prefix="HIVEMIND_API_")

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # gRPC settings
    grpc_port: int = 50051
    grpc_max_workers: int = 10

    # CORS settings
    cors_enabled: bool = True
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])

    # Request settings
    max_request_size: int = 10 * 1024 * 1024  # 10MB
    request_timeout: float = 300.0


# =============================================================================
# Main Settings Class
# =============================================================================

class Settings(BaseSettings):
    """
    Main HIVEMIND settings.

    Configuration is loaded in the following order (later overrides earlier):
    1. Default values
    2. TOML configuration file
    3. Environment variables
    """

    model_config = SettingsConfigDict(
        env_prefix="HIVEMIND_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General settings
    env: Environment = Environment.DEVELOPMENT
    debug: bool = False
    config_file: Path | None = None

    # Component configurations
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)
    codex: CodexConfig = Field(default_factory=CodexConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    qdrant: QdrantConfig = Field(default_factory=QdrantConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    rabbitmq: RabbitMQConfig = Field(default_factory=RabbitMQConfig)
    zeromq: ZeroMQConfig = Field(default_factory=ZeroMQConfig)
    concurrency: ConcurrencyConfig = Field(default_factory=ConcurrencyConfig)
    resilience: ResilienceConfig = Field(default_factory=ResilienceConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)
    api: APIConfig = Field(default_factory=APIConfig)

    # Agent settings
    agents_config_path: Path = Field(
        default=Path("config/agents.json"),
        description="Path to agents configuration file"
    )
    routing_config_path: Path = Field(
        default=Path("config/routing.json"),
        description="Path to routing configuration file"
    )

    @field_validator("config_file", mode="before")
    @classmethod
    def resolve_config_file(cls, v: Any) -> Path | None:
        """Resolve config file path."""
        if v is None:
            # Check default locations
            default_paths = [
                Path("hivemind.toml"),
                Path("config/hivemind.toml"),
                Path.home() / ".config" / "hivemind" / "config.toml",
            ]
            for path in default_paths:
                if path.exists():
                    return path
            return None
        return Path(v) if isinstance(v, str) else v

    @model_validator(mode="after")
    def load_config_file(self) -> "Settings":
        """Load configuration from TOML file if specified."""
        if self.config_file and self.config_file.exists():
            config_data = toml.load(self.config_file)
            # Merge TOML config with current settings
            self._merge_config(config_data)
        return self

    def _merge_config(self, config_data: dict[str, Any]) -> None:
        """Merge TOML configuration with current settings."""
        for key, value in config_data.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(attr, BaseSettings) and isinstance(value, dict):
                    # Update nested config
                    for k, v in value.items():
                        if hasattr(attr, k):
                            setattr(attr, k, v)
                else:
                    setattr(self, key, value)

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.env == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.env == Environment.DEVELOPMENT

    def get_database_url(self, async_: bool = True) -> str:
        """Get database URL."""
        return self.postgres.async_url if async_ else self.postgres.sync_url


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses LRU cache to ensure settings are loaded only once.
    Clear cache with get_settings.cache_clear() if needed.
    """
    return Settings()


def reload_settings() -> Settings:
    """
    Reload settings, clearing the cache.

    Returns a fresh Settings instance.
    """
    get_settings.cache_clear()
    return get_settings()
