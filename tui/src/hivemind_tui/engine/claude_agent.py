# DESTINATION: tui/src/hivemind_tui/engine/claude_agent.py
# CREATE THIS FILE AT THE EXACT PATH ABOVE
# DO NOT MODIFY THIS CODE

"""
HIVEMIND Claude Agent - Expert consultant and agent executor.

Claude is consulted by Codex for complex tasks.
Claude supervises agent execution.
Claude never talks directly to the user - only through Codex.
"""

import asyncio
import os
import signal
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any, TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .auth import AuthManager


# Agent definitions
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


CLAUDE_EVALUATOR_PROMPT = """You are Claude, an expert AI consultant working with Codex in HIVEMIND.

You are evaluating a proposed approach for a user task. Your job is to:
1. Assess if the approach is sound
2. Suggest improvements if needed
3. Identify which specialized agents (if any) should be involved
4. Help reach consensus with Codex on the best approach

Available agents:
- DEV-001 to DEV-006: Development (architecture, backend, frontend, code review, docs, devops)
- SEC-001 to SEC-006: Security (architecture, pentest, malware, wireless, compliance, incident)
- INF-001 to INF-006: Infrastructure (cloud, sysadmin, network, database, SRE, automation)
- QA-001 to QA-006: QA (strategy, automation, performance, security testing, manual, test data)

Respond with your evaluation and whether you agree with the approach.
If you agree, state "AGREED" clearly.
If you disagree, explain why and propose modifications.
"""


CLAUDE_EXECUTOR_PROMPT = """You are Claude, executing a task in HIVEMIND.

You are acting as {agent_name} ({agent_role}).
Team: {team}

Execute the assigned task with expertise in your domain.
Provide a complete, professional response.
Focus on your area of specialization.
"""


CLAUDE_VERIFIER_PROMPT = """You are Claude, verifying task completion in HIVEMIND.

Review the output against the original requirements.
Check for:
1. Completeness - Does it address all requirements?
2. Correctness - Is the approach/solution correct?
3. Quality - Does it meet professional standards?

If the output is acceptable, state "VERIFIED" clearly.
If issues exist, describe what needs to be fixed.
"""


@dataclass
class AgentResult:
    """Result from agent execution."""
    agent_id: str
    agent_name: str
    status: str  # "complete", "error", "pending"
    output: Optional[str] = None
    error: Optional[str] = None


@dataclass
class EvaluationResult:
    """Result from Claude's evaluation."""
    agrees: bool
    feedback: str
    suggested_agents: List[str] = field(default_factory=list)
    modifications: Optional[str] = None


@dataclass
class VerificationResult:
    """Result from Claude's verification."""
    verified: bool
    issues: Optional[str] = None
    suggestions: Optional[str] = None


class ClaudeAgent:
    """Claude as expert consultant and agent executor."""

    def __init__(
        self,
        auth_manager: "AuthManager",
        working_dir: Optional[Path] = None,
        timeout: Optional[float] = None,
        progress_interval: float = 5.0,
        on_status: Optional[Callable[[str], None]] = None,
    ):
        """Initialize Claude Agent.

        Args:
            auth_manager: Authentication manager
            working_dir: Working directory for operations
            timeout: Timeout in seconds
            progress_interval: Seconds between progress updates
            on_status: Optional status callback
        """
        self.auth = auth_manager
        self.working_dir = working_dir or Path.cwd()
        self.timeout = timeout or float(os.environ.get("HIVEMIND_CLAUDE_TIMEOUT", "45"))
        self.progress_interval = progress_interval
        self.on_status = on_status
    
    async def _call_claude_cli(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        timeout: Optional[float] = None,
        status_label: Optional[str] = None,
    ) -> tuple[bool, str]:
        """Call Claude CLI.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (success, response_or_error)
        """
        claude_path = self.auth.claude_path
        if not claude_path:
            return False, "Claude CLI not available"
        
        cmd = [claude_path, "--dangerously-skip-permissions", "--print"]
        
        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])
        
        cmd.append(prompt)
        
        process = None
        progress_task = None
        stop_event = asyncio.Event()
        effective_timeout = timeout or self.timeout

        async def _tick() -> None:
            while not stop_event.is_set():
                await asyncio.sleep(self.progress_interval)
                if not stop_event.is_set() and self.on_status and status_label:
                    self.on_status(status_label)

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.working_dir),
                start_new_session=True,
            )

            if status_label and self.on_status:
                progress_task = asyncio.create_task(_tick())

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=effective_timeout
                )
            except asyncio.TimeoutError:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except (ProcessLookupError, OSError):
                    if process:
                        process.kill()
                if process:
                    await process.wait()
                return False, f"Request timed out after {effective_timeout}s"

            if process.returncode == 0:
                response = stdout.decode("utf-8", errors="replace").strip()
                if not response:
                    return False, "No response from Claude"
                return True, response
            else:
                error = stderr.decode("utf-8", errors="replace").strip()
                return False, f"Claude error: {error or 'Unknown error'}"

        except asyncio.CancelledError:
            if process and process.returncode is None:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except (ProcessLookupError, OSError):
                    process.kill()
                await process.wait()
            raise
        except Exception as e:
            return False, f"Failed to call Claude: {str(e)}"
        finally:
            stop_event.set()
            if progress_task:
                progress_task.cancel()
    
    async def evaluate_proposal(
        self,
        user_request: str,
        codex_proposal: str,
        dialogue_history: Optional[List[Dict]] = None,
    ) -> EvaluationResult:
        """Evaluate Codex's proposed approach.
        
        Args:
            user_request: Original user request
            codex_proposal: Codex's proposed approach
            dialogue_history: Previous dialogue turns
            
        Returns:
            EvaluationResult with agreement status and feedback
        """
        history_text = ""
        if dialogue_history:
            history_parts = []
            for turn in dialogue_history:
                history_parts.append(f"{turn['speaker']}: {turn['content']}")
            history_text = "\n\n".join(history_parts)
        
        prompt = f"""User Request: {user_request}

{f"Previous Discussion:{chr(10)}{history_text}{chr(10)}{chr(10)}" if history_text else ""}Codex's Proposal:
{codex_proposal}

Evaluate this proposal. Do you agree with the approach?
If agents are needed, list them by ID (e.g., DEV-001, SEC-002).
"""
        
        success, response = await self._call_claude_cli(
            prompt,
            system_prompt=CLAUDE_EVALUATOR_PROMPT,
            status_label="Waiting on Claude evaluation...",
        )
        
        if not success:
            return EvaluationResult(
                agrees=False,
                feedback=f"Failed to evaluate: {response}",
            )
        
        # Parse response
        agrees = "AGREED" in response.upper() or "I AGREE" in response.upper()
        
        # Extract suggested agents
        suggested_agents = []
        for agent_id in AGENTS.keys():
            if agent_id in response:
                suggested_agents.append(agent_id)
        
        return EvaluationResult(
            agrees=agrees,
            feedback=response,
            suggested_agents=suggested_agents,
        )
    
    async def execute_agent_task(
        self,
        agent_id: str,
        task: str,
        context: Optional[str] = None,
    ) -> AgentResult:
        """Execute task as specific agent.
        
        Args:
            agent_id: Agent ID (e.g., "DEV-001")
            task: Task to execute
            context: Optional additional context
            
        Returns:
            AgentResult with output
        """
        agent_info = AGENTS.get(agent_id, {
            "name": "Unknown",
            "role": "Unknown",
            "team": "Unknown"
        })
        
        system_prompt = CLAUDE_EXECUTOR_PROMPT.format(
            agent_name=agent_info["name"],
            agent_role=agent_info["role"],
            team=agent_info["team"],
        )
        
        full_task = task
        if context:
            full_task = f"Context:\n{context}\n\nTask:\n{task}"
        
        success, response = await self._call_claude_cli(
            full_task,
            system_prompt=system_prompt,
            status_label=f"Executing {agent_id}...",
        )
        
        if success:
            return AgentResult(
                agent_id=agent_id,
                agent_name=agent_info["name"],
                status="complete",
                output=response,
            )
        else:
            return AgentResult(
                agent_id=agent_id,
                agent_name=agent_info["name"],
                status="error",
                error=response,
            )
    
    async def execute_agents(
        self,
        agents: List[str],
        task: str,
        context: Optional[str] = None,
    ) -> List[AgentResult]:
        """Execute task with multiple agents.
        
        Args:
            agents: List of agent IDs
            task: Task to execute
            context: Optional context
            
        Returns:
            List of AgentResult
        """
        results = []
        for agent_id in agents:
            result = await self.execute_agent_task(agent_id, task, context)
            results.append(result)
        return results
    
    async def verify_output(
        self,
        original_request: str,
        output: str,
    ) -> VerificationResult:
        """Verify that output meets requirements.
        
        Args:
            original_request: Original user request
            output: Output to verify
            
        Returns:
            VerificationResult
        """
        prompt = f"""Original Request:
{original_request}

Output to Verify:
{output}

Is this output complete and correct? Review against the original requirements.
"""
        
        success, response = await self._call_claude_cli(
            prompt,
            system_prompt=CLAUDE_VERIFIER_PROMPT,
            status_label="Waiting on Claude verification...",
        )
        
        if not success:
            return VerificationResult(
                verified=False,
                issues=f"Verification failed: {response}",
            )
        
        verified = "VERIFIED" in response.upper()
        
        return VerificationResult(
            verified=verified,
            issues=None if verified else response,
            suggestions=response if not verified else None,
        )
    
    async def synthesize_results(
        self,
        results: List[AgentResult],
        original_request: str,
    ) -> str:
        """Synthesize multiple agent results into cohesive output.
        
        Args:
            results: List of agent results
            original_request: Original user request
            
        Returns:
            Synthesized output
        """
        if len(results) == 1:
            return results[0].output or results[0].error or "No output"
        
        results_text = []
        for r in results:
            if r.status == "complete" and r.output:
                results_text.append(f"## {r.agent_name} ({r.agent_id})\n{r.output}")
        
        prompt = f"""Original Request:
{original_request}

Agent Outputs:
{chr(10).join(results_text)}

Synthesize these outputs into a single, cohesive response for the user.
Remove redundancy, organize logically, and present as one unified answer.
"""
        
        success, response = await self._call_claude_cli(prompt, status_label="Synthesizing agent outputs...")
        
        if success:
            return response
        else:
            # Fallback: just concatenate
            return "\n\n".join(results_text)
