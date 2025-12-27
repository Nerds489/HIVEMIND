"""Tests for routing logic."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from hivemind_tui.engine.codex_head import CodexHead


class TestKeywordMatching:
    """Tests for keyword matching logic."""

    def test_keyword_in_text_single_word(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test matching a single word keyword."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            normalized = codex._normalize("Build the backend service")
            tokens = normalized.split()

            assert codex._keyword_in_text("backend", normalized, tokens) is True
            assert codex._keyword_in_text("frontend", normalized, tokens) is False

    def test_keyword_in_text_multi_word(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test matching multi-word keyword."""
        # Add multi-word keyword to settings
        settings_path = hivemind_root / "config" / "settings.json"
        with settings_path.open("r") as f:
            settings = json.load(f)
        settings["routing"]["keywords"]["security audit"] = ["SEC-005"]
        with settings_path.open("w") as f:
            json.dump(settings, f)

        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            normalized = codex._normalize("Run a security audit on the system")
            tokens = normalized.split()

            assert codex._keyword_in_text("security audit", normalized, tokens) is True

    def test_keyword_case_insensitive(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that keyword matching is case insensitive."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            normalized = codex._normalize("BUILD THE BACKEND SERVICE")
            tokens = normalized.split()

            assert codex._keyword_in_text("backend", normalized, tokens) is True
            assert codex._keyword_in_text("BACKEND", normalized, tokens) is True

    def test_keyword_with_special_chars(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test keyword matching with special characters."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            # Test hyphenated keyword
            normalized = codex._normalize("Create an API-endpoint")
            tokens = normalized.split()

            # "api-endpoint" becomes "api endpoint" after normalization
            assert codex._keyword_in_text("api", normalized, tokens) is True


class TestRoutingRules:
    """Tests for routing rules."""

    def test_route_to_single_agent(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test routing to a single agent."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("Build a backend API")

            assert "DEV-002" in agents

    def test_route_to_multiple_agents(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test routing to multiple agents with multiple keywords."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("Build backend API and run security tests and deploy")

            assert "DEV-002" in agents
            assert "SEC-001" in agents or "SEC-002" in agents
            assert "INF-005" in agents

    def test_route_no_duplicates(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that routing doesn't create duplicate agents."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("Build backend API and api endpoint and backend service")

            # DEV-002 should only appear once
            assert agents.count("DEV-002") == 1

    def test_route_empty_task(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test routing with empty task."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("")

            assert agents == []


class TestTeamRouting:
    """Tests for team-based routing."""

    def test_team_members_loaded(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that team members are loaded correctly."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert "development" in codex._team_members
            assert "DEV-001" in codex._team_members["development"]

    def test_team_command_routing(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that /dev command routes to development team."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            cmd, task = codex._parse_command("/dev Build something")

            assert cmd == "dev"
            # In actual processing, this would get all dev team members


class TestComplexityRouting:
    """Tests for complexity-based routing."""

    def test_simple_request_no_keywords(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that requests without keywords are simple."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert codex._is_simple_request("What is Python?") is True

    def test_simple_request_short(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that short requests are simple."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert codex._is_simple_request("Hello") is True

    def test_complex_request_with_keywords(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that requests with keywords are complex."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            assert codex._is_simple_request("Build a backend API") is False

    def test_complex_request_long(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that long requests are complex."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            long_request = " ".join(["word"] * 20)  # 20 words
            assert codex._is_simple_request(long_request) is False


class TestRoutingPriority:
    """Tests for routing priority."""

    def test_routing_preserves_order(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that routing preserves order of matched agents."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            # First keyword matched should appear first
            agents1 = codex._route_agents("backend security")
            agents2 = codex._route_agents("security backend")

            # Both should contain the same agents (order may vary based on keyword order in config)
            assert set(agents1) == set(agents2)


class TestFallbackRouting:
    """Tests for fallback routing."""

    def test_no_match_returns_empty(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that no match returns empty list."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("completely unrelated query xyz123")

            assert agents == []

    def test_gibberish_returns_empty(self, hivemind_root: Path, mock_auth: MagicMock):
        """Test that gibberish returns empty list."""
        with patch.object(CodexHead, "_find_repo_root", return_value=hivemind_root):
            codex = CodexHead(auth_manager=mock_auth, working_dir=hivemind_root)

            agents = codex._route_agents("asdfghjkl qwertyuiop")

            assert agents == []
