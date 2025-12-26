"""
HIVEMIND Coordinator - Intelligent input routing via Claude CLI.

This module implements HEAD_CODEX - the master orchestration intelligence
that decides whether to route to agents or respond directly.
"""

import asyncio
import json
import os
import shutil
import signal
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
import re


class RouteType(str, Enum):
    """Type of route decision."""
    DIRECT = "direct"       # Respond directly, no agents
    AGENT = "agent"         # Route to single agent
    WORKFLOW = "workflow"   # Route to multi-agent workflow


@dataclass
class RouteDecision:
    """Result of coordinator's routing decision."""
    route_type: RouteType
    response: Optional[str] = None      # For direct responses
    agent_id: Optional[str] = None      # For agent routing
    agent_name: Optional[str] = None    # Human-readable agent name
    workflow: Optional[str] = None      # For workflow routing
    task: Optional[str] = None          # Processed task description
    error: Optional[str] = None         # Error message if routing failed
    raw_response: Optional[str] = None  # Raw response from Claude


@dataclass
class AgentResult:
    """Result from agent execution."""
    agent_id: str
    agent_name: str
    status: str  # working, complete, error
    output: Optional[str] = None
    error: Optional[str] = None
    gate_status: Optional[str] = None  # PASSED, BLOCKED, PENDING, SKIPPED


@dataclass
class ExecutionResult:
    """Full execution result."""
    success: bool
    response: str
    route_decision: RouteDecision
    agent_results: List[AgentResult] = field(default_factory=list)
    gates_passed: List[str] = field(default_factory=list)
    gates_blocked: List[str] = field(default_factory=list)
    error: Optional[str] = None


# Agent definitions matching HIVEMIND v2.0
AGENTS = {
    # Development Team
    "DEV-001": {"name": "Architect", "role": "System Architecture", "team": "Development"},
    "DEV-002": {"name": "Backend Developer", "role": "Backend Implementation", "team": "Development"},
    "DEV-003": {"name": "Frontend Developer", "role": "Frontend Implementation", "team": "Development"},
    "DEV-004": {"name": "Code Reviewer", "role": "Code Review", "team": "Development"},
    "DEV-005": {"name": "Technical Writer", "role": "Documentation", "team": "Development"},
    "DEV-006": {"name": "DevOps Liaison", "role": "CI/CD & Deployment", "team": "Development"},

    # Security Team
    "SEC-001": {"name": "Security Architect", "role": "Security Design", "team": "Security"},
    "SEC-002": {"name": "Penetration Tester", "role": "Security Testing", "team": "Security"},
    "SEC-003": {"name": "Malware Analyst", "role": "Threat Analysis", "team": "Security"},
    "SEC-004": {"name": "Wireless Security", "role": "Wireless/IoT Security", "team": "Security"},
    "SEC-005": {"name": "Compliance Auditor", "role": "Compliance", "team": "Security"},
    "SEC-006": {"name": "Incident Responder", "role": "Incident Response", "team": "Security"},

    # Infrastructure Team
    "INF-001": {"name": "Infrastructure Architect", "role": "Cloud Architecture", "team": "Infrastructure"},
    "INF-002": {"name": "Systems Administrator", "role": "System Admin", "team": "Infrastructure"},
    "INF-003": {"name": "Network Engineer", "role": "Networking", "team": "Infrastructure"},
    "INF-004": {"name": "Database Administrator", "role": "Database Management", "team": "Infrastructure"},
    "INF-005": {"name": "Site Reliability Engineer", "role": "SRE & Monitoring", "team": "Infrastructure"},
    "INF-006": {"name": "Automation Engineer", "role": "IaC & Automation", "team": "Infrastructure"},

    # QA Team
    "QA-001": {"name": "QA Architect", "role": "Test Strategy", "team": "QA"},
    "QA-002": {"name": "Test Automation Engineer", "role": "Test Automation", "team": "QA"},
    "QA-003": {"name": "Performance Tester", "role": "Performance Testing", "team": "QA"},
    "QA-004": {"name": "Security Tester", "role": "DAST/SAST", "team": "QA"},
    "QA-005": {"name": "Manual QA Tester", "role": "Manual Testing", "team": "QA"},
    "QA-006": {"name": "Test Data Manager", "role": "Test Data", "team": "QA"},
}


# Quality gates
GATES = {
    "G1-DESIGN": {"name": "Design Gate", "required_agents": ["DEV-001"]},
    "G2-SECURITY": {"name": "Security Gate", "required_agents": ["SEC-001", "SEC-002"]},
    "G3-CODE": {"name": "Code Gate", "required_agents": ["DEV-004"]},
    "G4-TEST": {"name": "Test Gate", "required_agents": ["QA-001", "QA-002"]},
    "G5-DEPLOY": {"name": "Deploy Gate", "required_agents": ["INF-005"]},
}


COORDINATOR_SYSTEM_PROMPT = """You are HEAD_CODEX, the HIVEMIND coordinator. Analyze user input and decide routing.

RESPOND DIRECTLY (no agents) for:
- Questions about yourself (who are you, what are you, tell me about yourself)
- Greetings (hi, hello, hey, good morning)
- Conversation (how are you, thanks, ok, sure, yes, no)
- Complaints or feedback
- Meta questions about HIVEMIND
- Simple factual questions you can answer
- Anything that isn't a work task

ROUTE TO AGENTS only for:
- Explicit work requests (build X, design Y, implement Z)
- Code tasks (write, create, fix, debug code)
- Security tasks (pentest, audit, assess vulnerabilities)
- Infrastructure tasks (deploy, configure, optimize systems)
- QA tasks (test, validate, review)

Available agents:
DEV-001: Architect (architecture, design, system, patterns)
DEV-002: Backend Developer (backend, api, server, database)
DEV-003: Frontend Developer (frontend, ui, react, vue)
DEV-004: Code Reviewer (review, code quality, pr)
DEV-005: Technical Writer (documentation, docs, readme)
DEV-006: DevOps Liaison (ci, cd, pipeline, deploy)
SEC-001: Security Architect (security design, threat model)
SEC-002: Penetration Tester (pentest, vulnerability, exploit)
SEC-003: Malware Analyst (malware, reverse engineering)
SEC-004: Wireless Security (wireless, wifi, bluetooth)
SEC-005: Compliance Auditor (compliance, audit, gdpr, soc2)
SEC-006: Incident Responder (incident, breach, forensics)
INF-001: Infrastructure Architect (cloud, aws, gcp, azure)
INF-002: Systems Administrator (server, linux, windows)
INF-003: Network Engineer (network, firewall, dns)
INF-004: Database Administrator (database, sql, postgres)
INF-005: SRE (sre, monitoring, kubernetes, reliability)
INF-006: Automation Engineer (terraform, ansible, automation)
QA-001: QA Architect (test strategy, quality, coverage)
QA-002: Test Automation (selenium, cypress, pytest)
QA-003: Performance Tester (load, performance, stress)
QA-004: Security Tester (dast, sast, security scan)
QA-005: Manual QA (manual, uat, exploratory)
QA-006: Test Data Manager (test data, fixtures)

IMPORTANT: For direct responses, YOU must answer the question fully. Do not defer to agents.

Response format (JSON only, no markdown):
{"route": "direct", "response": "your complete answer here"}
OR
{"route": "agent", "agent_id": "DEV-001", "task": "processed task description"}
OR
{"route": "workflow", "workflow": "full-sdlc", "agents": ["DEV-001", "DEV-002", "QA-002"], "task": "description"}
"""


class Coordinator:
    """HEAD_CODEX - Master orchestration intelligence."""

    def __init__(
        self,
        working_dir: Optional[Path] = None,
        on_status_update: Optional[Callable[[str, str], None]] = None,
        on_agent_update: Optional[Callable[[str, str, str], None]] = None,
    ):
        """Initialize coordinator.

        Args:
            working_dir: Working directory for Claude execution
            on_status_update: Callback for status updates (status, message)
            on_agent_update: Callback for agent updates (agent_id, status, message)
        """
        self.working_dir = working_dir or Path.cwd()
        self.on_status_update = on_status_update
        self.on_agent_update = on_agent_update
        self._codex_path: Optional[str] = None
        self._claude_path: Optional[str] = None

    def _find_codex(self) -> Optional[str]:
        """Find Codex CLI executable (main coordinator)."""
        if self._codex_path:
            return self._codex_path

        codex_path = shutil.which("codex")
        if codex_path:
            self._codex_path = codex_path
            return codex_path

        for path in [
            Path.home() / ".nvm/versions/node/v24.12.0/bin/codex",
            Path.home() / ".local/bin/codex",
            Path("/usr/local/bin/codex"),
        ]:
            if path.exists():
                self._codex_path = str(path)
                return self._codex_path

        return None

    def _find_claude(self) -> Optional[str]:
        """Find Claude CLI executable (agents)."""
        if self._claude_path:
            return self._claude_path

        claude_path = shutil.which("claude")
        if claude_path:
            self._claude_path = claude_path
            return claude_path

        for path in [
            Path.home() / ".local/bin/claude",
            Path("/usr/local/bin/claude"),
        ]:
            if path.exists():
                self._claude_path = str(path)
                return self._claude_path

        return None

    def _emit_status(self, status: str, message: str) -> None:
        """Emit status update."""
        if self.on_status_update:
            self.on_status_update(status, message)

    def _emit_agent(self, agent_id: str, status: str, message: str) -> None:
        """Emit agent update."""
        if self.on_agent_update:
            self.on_agent_update(agent_id, status, message)

    async def _call_codex(
        self,
        prompt: str,
        timeout: float = 60.0,
    ) -> tuple[bool, str]:
        """Call Codex CLI for coordinator decisions.

        Args:
            prompt: User prompt
            timeout: Timeout in seconds

        Returns:
            Tuple of (success, response_or_error)
        """
        codex_path = self._find_codex()
        if not codex_path:
            return False, "Codex CLI not found. Install with: npm install -g @openai/codex"

        # Build command - codex exec for non-interactive mode
        output_file = tempfile.mktemp(suffix=".txt")
        cmd = [codex_path, "exec", "--full-auto", "--skip-git-repo-check", "-o", output_file, prompt]

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.DEVNULL,  # Prevent stdin blocking
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.working_dir),
                start_new_session=True,  # Allow killing entire process group
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except (ProcessLookupError, OSError):
                    process.kill()
                await process.wait()
                return False, f"Request timed out after {timeout}s"

            if process.returncode == 0:
                # Read response from output file
                try:
                    if os.path.exists(output_file):
                        with open(output_file, 'r') as f:
                            response = f.read().strip()
                        os.remove(output_file)
                    else:
                        response = stdout.decode("utf-8", errors="replace").strip()
                except Exception:
                    response = stdout.decode("utf-8", errors="replace").strip()

                if not response:
                    return False, "No response received from Codex"
                return True, response
            else:
                # Clean up output file on error
                try:
                    if os.path.exists(output_file):
                        os.remove(output_file)
                except Exception:
                    pass
                error = stderr.decode("utf-8", errors="replace").strip()
                return False, f"Codex error: {error or 'Unknown error'}"

        except Exception as e:
            # Clean up output file on exception
            try:
                if os.path.exists(output_file):
                    os.remove(output_file)
            except Exception:
                pass
            return False, f"Failed to call Codex: {str(e)}"

    async def _call_claude(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        timeout: float = 60.0,
    ) -> tuple[bool, str]:
        """Call Claude CLI for agent execution.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            timeout: Timeout in seconds

        Returns:
            Tuple of (success, response_or_error)
        """
        claude_path = self._find_claude()
        if not claude_path:
            return False, "Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"

        # Build command
        cmd = [claude_path, "--dangerously-skip-permissions", "--print"]

        # Add system prompt if provided
        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])

        cmd.append(prompt)

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.DEVNULL,  # Prevent stdin blocking
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.working_dir),
                start_new_session=True,  # Allow killing entire process group
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except (ProcessLookupError, OSError):
                    process.kill()
                await process.wait()
                return False, f"Request timed out after {timeout}s"

            if process.returncode == 0:
                response = stdout.decode("utf-8", errors="replace").strip()
                if not response:
                    return False, "No response received from Claude"
                return True, response
            else:
                error = stderr.decode("utf-8", errors="replace").strip()
                return False, f"Claude error: {error or 'Unknown error'}"

        except Exception as e:
            return False, f"Failed to call Claude: {str(e)}"

    def _parse_route_decision(self, response: str) -> RouteDecision:
        """Parse routing decision from Claude response.

        Args:
            response: Raw response from Claude

        Returns:
            RouteDecision object
        """
        # Try to extract JSON from response
        try:
            # Look for JSON in the response
            json_match = re.search(r'\{[^{}]*"route"[^{}]*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                # Try parsing entire response as JSON
                data = json.loads(response)

            route = data.get("route", "direct")

            if route == "direct":
                return RouteDecision(
                    route_type=RouteType.DIRECT,
                    response=data.get("response", response),
                    raw_response=response,
                )
            elif route == "agent":
                agent_id = data.get("agent_id", "DEV-001")
                agent_info = AGENTS.get(agent_id, {"name": "Unknown", "role": "Unknown"})
                return RouteDecision(
                    route_type=RouteType.AGENT,
                    agent_id=agent_id,
                    agent_name=agent_info["name"],
                    task=data.get("task", ""),
                    raw_response=response,
                )
            elif route == "workflow":
                return RouteDecision(
                    route_type=RouteType.WORKFLOW,
                    workflow=data.get("workflow", "custom"),
                    task=data.get("task", ""),
                    raw_response=response,
                )
            else:
                # Unknown route, treat as direct
                return RouteDecision(
                    route_type=RouteType.DIRECT,
                    response=response,
                    raw_response=response,
                )

        except json.JSONDecodeError:
            # If no valid JSON, treat response as direct answer
            return RouteDecision(
                route_type=RouteType.DIRECT,
                response=response,
                raw_response=response,
            )

    async def classify_input(self, user_input: str) -> RouteDecision:
        """Classify user input and decide routing.

        Args:
            user_input: User's input text

        Returns:
            RouteDecision indicating how to handle the input
        """
        self._emit_status("analyzing", "Analyzing input...")

        # Quick pattern matching for obvious cases (optimization)
        lower_input = user_input.lower().strip()

        # Obvious greetings - respond directly without calling Claude
        greetings = ["hi", "hello", "hey", "hi!", "hello!", "hey!"]
        if lower_input in greetings:
            return RouteDecision(
                route_type=RouteType.DIRECT,
                response="Hello! I'm HIVEMIND, a multi-agent AI orchestration system. How can I help you today?",
            )

        # Obvious identity questions
        identity_patterns = [
            "who are you",
            "what are you",
            "tell me about yourself",
            "what is hivemind",
            "what's hivemind",
        ]
        if any(pattern in lower_input for pattern in identity_patterns):
            return RouteDecision(
                route_type=RouteType.DIRECT,
                response="""I am HIVEMIND, a multi-agent AI orchestration system powered by HEAD_CODEX.

I coordinate 24 specialized AI agents across 4 teams:
- **Development** (DEV-001 to DEV-006): Architecture, Backend, Frontend, Code Review, Documentation, DevOps
- **Security** (SEC-001 to SEC-006): Security Architecture, Pentesting, Malware Analysis, Wireless, Compliance, Incident Response
- **Infrastructure** (INF-001 to INF-006): Cloud Architecture, SysAdmin, Networking, DBA, SRE, Automation
- **QA** (QA-001 to QA-006): Test Strategy, Automation, Performance, Security Testing, Manual QA, Test Data

For simple questions and conversation, I respond directly. For complex technical tasks, I route to the appropriate specialized agents.

What would you like help with?""",
            )

        # Call Codex for classification (Codex = main coordinator)
        routing_prompt = f"{COORDINATOR_SYSTEM_PROMPT}\n\nUser input: {user_input}"
        success, response = await self._call_codex(routing_prompt)

        if not success:
            return RouteDecision(
                route_type=RouteType.DIRECT,
                error=response,
            )

        return self._parse_route_decision(response)

    async def execute_agent(
        self,
        agent_id: str,
        task: str,
        context: Optional[str] = None,
    ) -> AgentResult:
        """Execute task with specific agent.

        Args:
            agent_id: Agent ID (e.g., "DEV-001")
            task: Task to execute
            context: Optional additional context

        Returns:
            AgentResult with output
        """
        agent_info = AGENTS.get(agent_id, {"name": "Unknown", "role": "Unknown", "team": "Unknown"})
        agent_name = agent_info["name"]

        self._emit_agent(agent_id, "working", f"{agent_name} processing...")

        # Build agent-specific system prompt
        agent_prompt = f"""You are {agent_name}, a specialized AI agent in the HIVEMIND system.
Your role: {agent_info['role']}
Team: {agent_info['team']}

You are executing the following task. Provide a complete, professional response.
Focus on your area of expertise. Be concise but thorough.
"""

        if context:
            full_task = f"{context}\n\nTask: {task}"
        else:
            full_task = task

        success, response = await self._call_claude(full_task, system_prompt=agent_prompt)

        if success:
            self._emit_agent(agent_id, "complete", f"{agent_name} complete")
            return AgentResult(
                agent_id=agent_id,
                agent_name=agent_name,
                status="complete",
                output=response,
            )
        else:
            self._emit_agent(agent_id, "error", f"{agent_name} error")
            return AgentResult(
                agent_id=agent_id,
                agent_name=agent_name,
                status="error",
                error=response,
            )

    async def process_input(self, user_input: str) -> ExecutionResult:
        """Process user input end-to-end.

        This is the main entry point. It:
        1. Classifies the input
        2. Routes appropriately (direct response or agent execution)
        3. Returns the complete result

        Args:
            user_input: User's input text

        Returns:
            ExecutionResult with complete response
        """
        # Step 1: Classify input
        decision = await self.classify_input(user_input)

        if decision.error:
            return ExecutionResult(
                success=False,
                response=decision.error,
                route_decision=decision,
                error=decision.error,
            )

        # Step 2: Handle based on route type
        if decision.route_type == RouteType.DIRECT:
            # Direct response - no agents needed
            return ExecutionResult(
                success=True,
                response=decision.response or "No response",
                route_decision=decision,
            )

        elif decision.route_type == RouteType.AGENT:
            # Single agent execution
            agent_result = await self.execute_agent(
                decision.agent_id,
                decision.task or user_input,
            )

            # Determine gates
            gates_passed = []
            gates_blocked = []

            for gate_id, gate_info in GATES.items():
                if decision.agent_id in gate_info["required_agents"]:
                    if agent_result.status == "complete":
                        gates_passed.append(gate_id)
                    else:
                        gates_blocked.append(gate_id)

            return ExecutionResult(
                success=agent_result.status == "complete",
                response=agent_result.output or agent_result.error or "No response",
                route_decision=decision,
                agent_results=[agent_result],
                gates_passed=gates_passed,
                gates_blocked=gates_blocked,
                error=agent_result.error,
            )

        elif decision.route_type == RouteType.WORKFLOW:
            # Multi-agent workflow (simplified for now - just use primary agent)
            self._emit_status("workflow", f"Starting {decision.workflow} workflow")

            # For now, just execute with DEV-001 as coordinator
            agent_result = await self.execute_agent(
                "DEV-001",
                decision.task or user_input,
            )

            return ExecutionResult(
                success=agent_result.status == "complete",
                response=agent_result.output or agent_result.error or "No response",
                route_decision=decision,
                agent_results=[agent_result],
                error=agent_result.error,
            )

        else:
            return ExecutionResult(
                success=False,
                response="Unknown route type",
                route_decision=decision,
                error="Unknown route type",
            )


# Convenience function for simple usage
async def process_message(
    message: str,
    working_dir: Optional[Path] = None,
) -> tuple[bool, str, Optional[str]]:
    """Simple interface to process a message.

    Args:
        message: User message
        working_dir: Optional working directory

    Returns:
        Tuple of (success, response, agent_id or None)
    """
    coordinator = Coordinator(working_dir=working_dir)
    result = await coordinator.process_input(message)

    agent_id = None
    if result.agent_results:
        agent_id = result.agent_results[0].agent_id

    return result.success, result.response, agent_id
