"""Tests for MemoryStore."""

import json
from pathlib import Path

import pytest

from hivemind_tui.engine.memory import MemoryStore


class TestMemoryStoreInit:
    """Tests for MemoryStore initialization."""

    def test_init_creates_directories(self, temp_dir: Path):
        """Test that initialization creates required directories."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        assert store.sessions_dir.exists()
        assert store.completed_dir.exists()
        assert store.working_dir.exists()

    def test_init_sets_paths(self, temp_dir: Path):
        """Test that paths are set correctly."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        assert store.root == memory_root
        assert store.sessions_dir == memory_root / "sessions" / "active"
        assert store.completed_dir == memory_root / "sessions" / "completed"


class TestSessionManagement:
    """Tests for session management."""

    def test_start_session_creates_file(self, temp_dir: Path):
        """Test that starting a session creates a session file."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        session_id = store.start_session()

        assert session_id.startswith("SESSION-")
        assert store.session_path.exists()

    def test_start_session_returns_same_id(self, temp_dir: Path):
        """Test that starting a session twice returns the same ID."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        session_id_1 = store.start_session()
        session_id_2 = store.start_session()

        assert session_id_1 == session_id_2

    def test_session_file_structure(self, temp_dir: Path):
        """Test the structure of the session file."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)
        store.start_session()

        with store.session_path.open("r") as f:
            data = json.load(f)

        assert "session_id" in data
        assert "started_at" in data
        assert "updated_at" in data
        assert "entries" in data
        assert isinstance(data["entries"], list)


class TestRecordTask:
    """Tests for task recording."""

    def test_record_task_adds_entry(self, temp_dir: Path):
        """Test that recording a task adds an entry."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        store.record_task(
            task="Build API",
            agents=["DEV-001", "DEV-002"],
            gates={"G1-DESIGN": "PASSED"},
            report="Task complete",
            status_lines=["[DEV-001] Complete"],
        )

        with store.session_path.open("r") as f:
            data = json.load(f)

        assert len(data["entries"]) == 1
        entry = data["entries"][0]
        assert entry["task"] == "Build API"
        assert entry["agents"] == ["DEV-001", "DEV-002"]

    def test_record_task_multiple_entries(self, temp_dir: Path):
        """Test recording multiple tasks."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        for i in range(3):
            store.record_task(
                task=f"Task {i}",
                agents=["DEV-001"],
                gates={},
                report=f"Report {i}",
                status_lines=[],
            )

        with store.session_path.open("r") as f:
            data = json.load(f)

        assert len(data["entries"]) == 3

    def test_record_task_updates_current_task(self, temp_dir: Path):
        """Test that recording updates current-task.json."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        store.record_task(
            task="Build API",
            agents=["DEV-001"],
            gates={"G1-DESIGN": "PASSED"},
            report="Done",
            status_lines=[],
        )

        current_task_path = store.working_dir / "current-task.json"
        assert current_task_path.exists()

        with current_task_path.open("r") as f:
            data = json.load(f)

        assert data["task"] == "Build API"
        assert data["agents"] == ["DEV-001"]


class TestRecall:
    """Tests for memory recall."""

    def test_recall_empty_session(self, temp_dir: Path):
        """Test recall with no session."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        results = store.recall("test")

        assert results == []

    def test_recall_no_query(self, temp_dir: Path):
        """Test recall without query returns recent entries."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        for i in range(3):
            store.record_task(
                task=f"Task {i}",
                agents=["DEV-001"],
                gates={},
                report=f"Report {i}",
                status_lines=[],
            )

        results = store.recall("", limit=2)

        assert len(results) == 2

    def test_recall_with_query(self, temp_dir: Path):
        """Test recall with search query."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        store.record_task(task="Build API", agents=["DEV-002"], gates={}, report="API done", status_lines=[])
        store.record_task(task="Write tests", agents=["QA-001"], gates={}, report="Tests done", status_lines=[])
        store.record_task(task="Deploy API", agents=["INF-005"], gates={}, report="Deployed", status_lines=[])

        results = store.recall("API")

        assert len(results) == 2  # "Build API" and "Deploy API"

    def test_recall_case_insensitive(self, temp_dir: Path):
        """Test that recall is case insensitive."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        store.record_task(task="Build API", agents=["DEV-002"], gates={}, report="Done", status_lines=[])

        results_lower = store.recall("api")
        results_upper = store.recall("API")

        assert len(results_lower) == 1
        assert len(results_upper) == 1

    def test_recall_limit(self, temp_dir: Path):
        """Test that recall respects limit."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        for i in range(10):
            store.record_task(task=f"API task {i}", agents=["DEV-002"], gates={}, report="Done", status_lines=[])

        results = store.recall("API", limit=3)

        assert len(results) == 3

    def test_recall_searches_agents(self, temp_dir: Path):
        """Test that recall searches in agent IDs."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        store.record_task(task="Some task", agents=["SEC-002"], gates={}, report="Done", status_lines=[])

        results = store.recall("SEC-002")

        assert len(results) == 1

    def test_recall_searches_report(self, temp_dir: Path):
        """Test that recall searches in report text."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        store.record_task(task="Task", agents=["DEV-001"], gates={}, report="Vulnerability found", status_lines=[])

        results = store.recall("vulnerability")

        assert len(results) == 1


class TestReadWrite:
    """Tests for internal read/write methods."""

    def test_read_nonexistent_file(self, temp_dir: Path):
        """Test reading a file that doesn't exist."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        result = store._read(temp_dir / "nonexistent.json")

        assert result == {}

    def test_read_invalid_json(self, temp_dir: Path):
        """Test reading invalid JSON."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        invalid_file = temp_dir / "invalid.json"
        invalid_file.write_text("not valid json {{{")

        result = store._read(invalid_file)

        assert result == {}

    def test_write_creates_file(self, temp_dir: Path):
        """Test that write creates a new file."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        test_path = temp_dir / "test.json"
        store._write(test_path, {"key": "value"})

        assert test_path.exists()
        with test_path.open("r") as f:
            data = json.load(f)
        assert data["key"] == "value"

    def test_write_atomic(self, temp_dir: Path):
        """Test that write is atomic (uses temp file)."""
        memory_root = temp_dir / "memory"
        store = MemoryStore(memory_root)

        test_path = temp_dir / "test.json"
        store._write(test_path, {"version": 1})
        store._write(test_path, {"version": 2})

        # No .tmp file should remain
        assert not (temp_dir / "test.tmp").exists()

        with test_path.open("r") as f:
            data = json.load(f)
        assert data["version"] == 2
