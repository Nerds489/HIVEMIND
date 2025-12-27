"""Shared pytest fixtures for HIVEMIND tests."""

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest

# Add TUI src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tui" / "src"))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_auth() -> MagicMock:
    """Create a mock AuthManager."""
    auth = MagicMock()
    auth.codex_path = "/usr/bin/codex"
    auth.claude_path = "/usr/bin/claude"
    return auth


@pytest.fixture
def sample_settings(temp_dir: Path) -> Path:
    """Create sample settings.json."""
    config_dir = temp_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    settings = {
        "system": {"orchestrator": "HEAD_CODEX"},
        "routing": {
            "keywords": {
                "backend": ["DEV-002"],
                "api": ["DEV-002"],
                "security": ["SEC-001", "SEC-002"],
                "test": ["QA-001", "QA-002"],
                "deploy": ["INF-005"],
            }
        },
        "teams": {
            "development": {"members": ["DEV-001", "DEV-002", "DEV-003"]},
            "security": {"members": ["SEC-001", "SEC-002"]},
        },
        "quality_gates": {
            "G1_DESIGN": {"name": "Design Gate", "required_agents": ["DEV-001"]},
            "G2_SECURITY": {"name": "Security Gate", "required_agents": ["SEC-001"]},
        },
        "defaults": {
            "parallel_execution": True,
            "max_parallel_agents": 3,
        },
    }

    settings_path = config_dir / "settings.json"
    settings_path.write_text(json.dumps(settings, indent=2))
    return settings_path


@pytest.fixture
def sample_agents(temp_dir: Path) -> Path:
    """Create sample agents.json."""
    config_dir = temp_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    agents = {
        "agents": {
            "development": [
                {"id": "DEV-001", "name": "Architect", "role": "System Architecture"},
                {"id": "DEV-002", "name": "Backend Developer", "role": "Backend"},
            ],
            "security": [
                {"id": "SEC-001", "name": "Security Architect", "role": "Security Design"},
                {"id": "SEC-002", "name": "Penetration Tester", "role": "Security Testing"},
            ],
        }
    }

    agents_path = config_dir / "agents.json"
    agents_path.write_text(json.dumps(agents, indent=2))
    return agents_path


@pytest.fixture
def sample_memory_dir(temp_dir: Path) -> Path:
    """Create sample memory directory structure."""
    memory_dir = temp_dir / "memory"
    (memory_dir / "sessions" / "active").mkdir(parents=True, exist_ok=True)
    (memory_dir / "sessions" / "completed").mkdir(parents=True, exist_ok=True)
    (memory_dir / "working").mkdir(parents=True, exist_ok=True)
    return memory_dir


@pytest.fixture
def hivemind_root(temp_dir: Path, sample_settings: Path, sample_agents: Path, sample_memory_dir: Path) -> Path:
    """Create a complete HIVEMIND root directory for testing."""
    # Create VERSION file
    version_file = temp_dir / "VERSION"
    version_file.write_text("2.0.0-test")
    return temp_dir


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
