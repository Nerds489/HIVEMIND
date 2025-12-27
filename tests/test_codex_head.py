"""Tests for CodexHead orchestrator."""

import asyncio
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hivemind_tui.engine.codex_head import CodexHead, CodexResponse, ResponseSource


class TestCodexHeadInit:
    """Tests for CodexHead initialization."""

    def test_init_with_defaults(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test initialization with default values."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert codex.working_dir == hivemind_root
            assert codex.auth == mock_auth
            assert len(codex._agents) > 0
            assert len(codex._gates) > 0

    def test_loads_routing_keywords(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that routing keywords are loaded from settings."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert "backend" in codex._routing_keywords
            assert "DEV-002" in codex._routing_keywords["backend"]


class TestRouting:
    """Tests for agent routing logic."""

    def test_route_agents_single_keyword(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test routing with a single keyword match."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("Build a backend API")

            assert "DEV-002" in agents

    def test_route_agents_multiple_keywords(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test routing with multiple keyword matches."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("Build backend API with security")

            assert "DEV-002" in agents
            assert "SEC-001" in agents or "SEC-002" in agents

    def test_route_agents_no_match(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test routing with no keyword matches."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("Hello world")

            assert agents == []

    def test_normalize_text(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test text normalization for routing."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert codex._normalize("Hello World!") == "hello world"
            assert codex._normalize("API-endpoint") == "api endpoint"
            assert codex._normalize("test_123") == "test 123"


class TestSimpleRequestDetection:
    """Tests for simple request detection."""

    def test_is_simple_request_short(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that short requests without keywords are simple."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert codex._is_simple_request("What is Python?") is True
            assert codex._is_simple_request("Hello") is True

    def test_is_simple_request_with_keywords(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that requests with routing keywords are not simple."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert codex._is_simple_request("Build a backend API") is False
            assert codex._is_simple_request("Run security tests") is False


class TestCommandParsing:
    """Tests for command parsing."""

    def test_parse_command_with_slash(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test parsing slash commands."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            cmd, task = codex._parse_command("/dev Build something")
            assert cmd == "dev"
            assert task == "Build something"

    def test_parse_command_without_slash(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test parsing regular input."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            cmd, task = codex._parse_command("Build something")
            assert cmd is None
            assert task == "Build something"

    def test_parse_command_help(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test parsing help command."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            cmd, task = codex._parse_command("/help")
            assert cmd == "help"
            assert task == ""


class TestReportBuilding:
    """Tests for report generation."""

    def test_summarize_task_short(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test task summarization for short tasks."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            summary = codex._summarize_task("Build API")
            assert summary == "Build API"

    def test_summarize_task_long(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test task summarization for long tasks."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            long_task = "Build a very complex API with authentication and authorization and logging and monitoring and everything else"
            summary = codex._summarize_task(long_task, max_len=30)

            assert len(summary) <= 30
            assert summary.endswith("...")

    def test_enforce_status_words(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test status word enforcement (2-4 words max)."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            # Single word gets padded
            assert len(codex._enforce_status_words("Working").split()) == 2

            # Long status gets truncated
            result = codex._enforce_status_words("This is a very long status message")
            assert len(result.split()) == 4

    def test_format_status_line(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test status line formatting."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            line = codex._format_status_line("DEV-001", "Designing architecture")

            assert line.startswith("[DEV-001]")
            assert "Designing architecture" in line


class TestGateStatus:
    """Tests for quality gate status."""

    def test_build_gate_status_passed(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test gate status when required agents are present."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            from hivemind_tui.engine.claude_agent import AgentResult

            agent_ids = ["DEV-001", "SEC-001"]
            agent_results = {
                "DEV-001": AgentResult("DEV-001", "Architect", "complete", "Done"),
                "SEC-001": AgentResult("SEC-001", "Security", "complete", "Done"),
            }

            status = codex._build_gate_status(agent_ids, agent_results)

            assert status.get("G1-DESIGN") == "PASSED"
            assert status.get("G2-SECURITY") == "PASSED"

    def test_build_gate_status_skipped(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test gate status when required agents are not present."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agent_ids = []
            agent_results = {}

            status = codex._build_gate_status(agent_ids, agent_results)

            assert status.get("G1-DESIGN") == "SKIPPED"


class TestProcessHelp:
    """Tests for help command processing."""

    @pytest.mark.asyncio
    async def test_process_help_command(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test processing /help command."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            response = await codex.process("/help")

            assert response.success is True
            assert response.source == ResponseSource.CODEX_DIRECT
            assert "/hivemind" in response.content
            assert "/dev" in response.content

    @pytest.mark.asyncio
    async def test_process_status_command(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test processing /status command."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            response = await codex.process("/status")

            assert response.success is True
            assert "HIVEMIND STATUS" in response.content
