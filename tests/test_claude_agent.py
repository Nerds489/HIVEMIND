"""Tests for ClaudeAgent."""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hivemind_tui.engine.claude_agent import (
    AGENTS,
    AgentResult,
    ClaudeAgent,
    EvaluationResult,
    VerificationResult,
)


class TestAgentDefinitions:
    """Tests for agent definitions."""

    def test_all_agents_defined(self):
        """Test that all 24 agents are defined."""
        assert len(AGENTS) == 24

    def test_dev_team_agents(self):
        """Test DEV team agents."""
        dev_agents = [k for k in AGENTS.keys() if k.startswith("DEV-")]
        assert len(dev_agents) == 6
        assert "DEV-001" in AGENTS
        assert AGENTS["DEV-001"]["name"] == "Architect"

    def test_sec_team_agents(self):
        """Test SEC team agents."""
        sec_agents = [k for k in AGENTS.keys() if k.startswith("SEC-")]
        assert len(sec_agents) == 6
        assert "SEC-002" in AGENTS
        assert AGENTS["SEC-002"]["name"] == "Penetration Tester"

    def test_inf_team_agents(self):
        """Test INF team agents."""
        inf_agents = [k for k in AGENTS.keys() if k.startswith("INF-")]
        assert len(inf_agents) == 6
        assert "INF-005" in AGENTS
        assert AGENTS["INF-005"]["name"] == "Site Reliability Engineer"

    def test_qa_team_agents(self):
        """Test QA team agents."""
        qa_agents = [k for k in AGENTS.keys() if k.startswith("QA-")]
        assert len(qa_agents) == 6
        assert "QA-001" in AGENTS
        assert AGENTS["QA-001"]["name"] == "QA Architect"

    def test_agent_structure(self):
        """Test that all agents have required fields."""
        for agent_id, agent in AGENTS.items():
            assert "name" in agent, f"{agent_id} missing 'name'"
            assert "role" in agent, f"{agent_id} missing 'role'"
            assert "team" in agent, f"{agent_id} missing 'team'"


class TestClaudeAgentInit:
    """Tests for ClaudeAgent initialization."""

    def test_init_with_defaults(self, mock_auth: MagicMock, temp_dir: Path):
        """Test initialization with default values."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        assert agent.working_dir == temp_dir
        assert agent.auth == mock_auth
        assert agent.timeout == 30.0  # Default from env or hardcoded

    def test_init_with_custom_timeout(self, mock_auth: MagicMock, temp_dir: Path):
        """Test initialization with custom timeout."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir, timeout=60.0)

        assert agent.timeout == 60.0


class TestAgentResult:
    """Tests for AgentResult dataclass."""

    def test_create_success_result(self):
        """Test creating a successful result."""
        result = AgentResult(
            agent_id="DEV-001",
            agent_name="Architect",
            status="complete",
            output="Design complete",
        )

        assert result.agent_id == "DEV-001"
        assert result.status == "complete"
        assert result.output == "Design complete"
        assert result.error is None

    def test_create_error_result(self):
        """Test creating an error result."""
        result = AgentResult(
            agent_id="DEV-001",
            agent_name="Architect",
            status="error",
            error="Failed to connect",
        )

        assert result.status == "error"
        assert result.error == "Failed to connect"
        assert result.output is None


class TestEvaluationResult:
    """Tests for EvaluationResult dataclass."""

    def test_create_agreed_result(self):
        """Test creating an agreed evaluation."""
        result = EvaluationResult(
            agrees=True,
            feedback="AGREED - Approach is sound",
            suggested_agents=["DEV-001", "SEC-001"],
        )

        assert result.agrees is True
        assert len(result.suggested_agents) == 2

    def test_create_disagreed_result(self):
        """Test creating a disagreed evaluation."""
        result = EvaluationResult(
            agrees=False,
            feedback="Need to reconsider approach",
            modifications="Use different architecture",
        )

        assert result.agrees is False
        assert result.modifications is not None


class TestVerificationResult:
    """Tests for VerificationResult dataclass."""

    def test_create_verified_result(self):
        """Test creating a verified result."""
        result = VerificationResult(verified=True)

        assert result.verified is True
        assert result.issues is None

    def test_create_unverified_result(self):
        """Test creating an unverified result."""
        result = VerificationResult(
            verified=False,
            issues="Missing test coverage",
            suggestions="Add unit tests",
        )

        assert result.verified is False
        assert result.issues is not None


class TestClaudeAgentCLI:
    """Tests for Claude CLI interaction."""

    @pytest.mark.asyncio
    async def test_call_claude_cli_not_available(self, temp_dir: Path):
        """Test handling when Claude CLI is not available."""
        mock_auth = MagicMock()
        mock_auth.claude_path = None

        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)
        success, response = await agent._call_claude_cli("test prompt")

        assert success is False
        assert "not available" in response

    @pytest.mark.asyncio
    async def test_execute_agent_task_structure(self, mock_auth: MagicMock, temp_dir: Path):
        """Test that execute_agent_task returns proper structure."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        # Mock the CLI call
        with patch.object(agent, "_call_claude_cli", new_callable=AsyncMock) as mock_cli:
            mock_cli.return_value = (True, "Task completed successfully")

            result = await agent.execute_agent_task("DEV-001", "Design system")

            assert isinstance(result, AgentResult)
            assert result.agent_id == "DEV-001"
            assert result.agent_name == "Architect"
            assert result.status == "complete"

    @pytest.mark.asyncio
    async def test_execute_agent_task_error(self, mock_auth: MagicMock, temp_dir: Path):
        """Test handling errors in agent task execution."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        with patch.object(agent, "_call_claude_cli", new_callable=AsyncMock) as mock_cli:
            mock_cli.return_value = (False, "Connection failed")

            result = await agent.execute_agent_task("DEV-001", "Design system")

            assert result.status == "error"
            assert result.error == "Connection failed"


class TestClaudeAgentEvaluation:
    """Tests for proposal evaluation."""

    @pytest.mark.asyncio
    async def test_evaluate_proposal_agreed(self, mock_auth: MagicMock, temp_dir: Path):
        """Test evaluating a proposal that gets agreed."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        with patch.object(agent, "_call_claude_cli", new_callable=AsyncMock) as mock_cli:
            mock_cli.return_value = (True, "AGREED - This approach is sound. DEV-001 should handle architecture.")

            result = await agent.evaluate_proposal(
                user_request="Build an API",
                codex_proposal="Use REST with JWT auth",
            )

            assert result.agrees is True
            assert "DEV-001" in result.suggested_agents

    @pytest.mark.asyncio
    async def test_evaluate_proposal_disagreed(self, mock_auth: MagicMock, temp_dir: Path):
        """Test evaluating a proposal that gets disagreed."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        with patch.object(agent, "_call_claude_cli", new_callable=AsyncMock) as mock_cli:
            mock_cli.return_value = (True, "I disagree. We should use GraphQL instead.")

            result = await agent.evaluate_proposal(
                user_request="Build an API",
                codex_proposal="Use SOAP",
            )

            assert result.agrees is False


class TestClaudeAgentVerification:
    """Tests for output verification."""

    @pytest.mark.asyncio
    async def test_verify_output_verified(self, mock_auth: MagicMock, temp_dir: Path):
        """Test verifying output that passes."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        with patch.object(agent, "_call_claude_cli", new_callable=AsyncMock) as mock_cli:
            mock_cli.return_value = (True, "VERIFIED - Output meets all requirements.")

            result = await agent.verify_output(
                original_request="Build login form",
                output="<form>...</form>",
            )

            assert result.verified is True

    @pytest.mark.asyncio
    async def test_verify_output_failed(self, mock_auth: MagicMock, temp_dir: Path):
        """Test verifying output that fails."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        with patch.object(agent, "_call_claude_cli", new_callable=AsyncMock) as mock_cli:
            mock_cli.return_value = (True, "Missing password validation")

            result = await agent.verify_output(
                original_request="Build login form with validation",
                output="<form>...</form>",
            )

            assert result.verified is False
            assert result.issues is not None


class TestClaudeAgentSynthesis:
    """Tests for result synthesis."""

    @pytest.mark.asyncio
    async def test_synthesize_single_result(self, mock_auth: MagicMock, temp_dir: Path):
        """Test synthesizing a single result (no synthesis needed)."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        results = [
            AgentResult("DEV-001", "Architect", "complete", "Architecture design complete"),
        ]

        output = await agent.synthesize_results(results, "Design system")

        assert output == "Architecture design complete"

    @pytest.mark.asyncio
    async def test_synthesize_multiple_results(self, mock_auth: MagicMock, temp_dir: Path):
        """Test synthesizing multiple results."""
        agent = ClaudeAgent(mock_auth, working_dir=temp_dir)

        with patch.object(agent, "_call_claude_cli", new_callable=AsyncMock) as mock_cli:
            mock_cli.return_value = (True, "Combined output from all agents")

            results = [
                AgentResult("DEV-001", "Architect", "complete", "Architecture done"),
                AgentResult("SEC-001", "Security", "complete", "Security review done"),
            ]

            output = await agent.synthesize_results(results, "Build secure system")

            assert "Combined output" in output or "Architecture" in output
