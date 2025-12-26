"""
HIVEMIND Codex Head - Codex CLI orchestrator.

Codex (HEAD_CODEX) coordinates Claude agents, emits minimal status lines,
quality gates, and a final consolidated report.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import signal
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from .memory import MemoryStore
from .claude_agent import ClaudeAgent, AgentResult
from .dialogue import CodexClaudeDialogue, DialogueResult


class ResponseSource(str, Enum):
    """Source of the response."""

    CODEX_DIRECT = "codex_direct"
    AGENTS = "agents"


@dataclass
class CodexResponse:
    """Response from Codex."""

    content: str
    source: ResponseSource
    success: bool = True
    error: Optional[str] = None
    agents_used: List[str] = field(default_factory=list)
    dialogue_turns: int = 0


REPORT_WIDTH = 62

BOX_TOP = "╔" + "═" * REPORT_WIDTH + "╗"
BOX_DIVIDER = "╠" + "═" * REPORT_WIDTH + "╣"
BOX_BOTTOM = "╚" + "═" * REPORT_WIDTH + "╝"

TEAM_COMMANDS = {
    "dev": "development",
    "sec": "security",
    "infra": "infrastructure",
    "qa": "qa",
}

SINGLE_AGENT_COMMANDS = {
    "architect": "DEV-001",
    "pentest": "SEC-002",
    "sre": "INF-005",
    "reviewer": "DEV-004",
}

HELP_TEXT = """HIVEMIND Commands:
  /hivemind [task]   Full multi-agent orchestration
  /dev [task]        Development team
  /sec [task]        Security team
  /infra [task]      Infrastructure team
  /qa [task]         QA team
  /architect [task]  DEV-001 Architect
  /pentest [task]    SEC-002 Penetration Tester
  /sre [task]        INF-005 SRE
  /reviewer [task]   DEV-004 Code Reviewer
  /status            Show system status
  /recall [query]    Recall recent session memory
  /debug [task]      Debug routing details
""".strip()


class CodexHead:
    """Codex CLI orchestrator."""

    def __init__(
        self,
        auth_manager: Optional["AuthManager"] = None,
        working_dir: Optional[Path] = None,
        on_status: Optional[Callable[[str], None]] = None,
        on_agent_update: Optional[Callable[[str, str, str], None]] = None,
        on_gate_update: Optional[Callable[[str, str], None]] = None,
        on_orchestration_start: Optional[Callable[[str, List[str]], None]] = None,
    ) -> None:
        self.auth = auth_manager
        self.working_dir = working_dir or Path.cwd()
        self.on_status = on_status
        self.on_agent_update = on_agent_update
        self.on_gate_update = on_gate_update
        self.on_orchestration_start = on_orchestration_start
        self._conversation_history: List[dict] = []
        self._pending_processes: List[asyncio.subprocess.Process] = []

        self._repo_root = self._find_repo_root(Path(__file__).resolve())
        self._settings = self._load_json(self._repo_root / "config" / "settings.json")
        self._agents = self._load_agents(self._repo_root / "config" / "agents.json")
        self._routing_keywords = self._settings.get("routing", {}).get("keywords", {})
        self._team_members = self._build_team_members()
        self._gates = self._build_gates()
        self._memory = MemoryStore(self._repo_root / "memory")

        self._codex_timeout = float(os.environ.get("HIVEMIND_CODEX_TIMEOUT", "20"))
        self._claude_timeout = float(os.environ.get("HIVEMIND_CLAUDE_TIMEOUT", "45"))
        self._dialogue_turns = int(os.environ.get("HIVEMIND_DIALOGUE_TURNS", "3"))
        self._progress_interval = float(os.environ.get("HIVEMIND_PROGRESS_INTERVAL", "5"))

    def _emit_status(self, message: str) -> None:
        if self.on_status:
            self.on_status(message)

    def _emit_agent_update(self, agent_id: str, status: str, message: str) -> None:
        if self.on_agent_update:
            self.on_agent_update(agent_id, status, message)

    def _emit_gate_update(self, gate_id: str, status: str) -> None:
        if self.on_gate_update:
            self.on_gate_update(gate_id, status)

    def _emit_orchestration_start(self, task: str, agents: List[str]) -> None:
        if self.on_orchestration_start:
            self.on_orchestration_start(task, agents)

    def _find_repo_root(self, start: Path) -> Path:
        for parent in [start] + list(start.parents):
            if (parent / "config" / "settings.json").exists():
                return parent
        return start

    def _load_json(self, path: Path) -> Dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

    def _load_agents(self, path: Path) -> Dict[str, Dict[str, Any]]:
        payload = self._load_json(path)
        agents: Dict[str, Dict[str, Any]] = {}
        for team_name, team_agents in payload.get("agents", {}).items():
            for agent in team_agents:
                agent_id = agent.get("id")
                if not agent_id:
                    continue
                agent_copy = dict(agent)
                agent_copy["team"] = team_name
                agents[agent_id] = agent_copy
        return agents

    def _build_team_members(self) -> Dict[str, List[str]]:
        teams = {}
        settings_teams = self._settings.get("teams", {})
        if settings_teams:
            for team_name, info in settings_teams.items():
                teams[team_name] = list(info.get("members", []))
        if not teams:
            for agent_id, agent in self._agents.items():
                team = agent.get("team", "unknown")
                teams.setdefault(team, []).append(agent_id)
        return teams

    def _build_gates(self) -> Dict[str, Dict[str, Any]]:
        gates = {}
        for key, info in self._settings.get("quality_gates", {}).items():
            gate_id = key.replace("_", "-")
            required = []
            if "required_agent" in info:
                required.append(info["required_agent"])
            required.extend(info.get("required_agents", []))
            gates[gate_id] = {
                "name": info.get("name", gate_id),
                "required_agents": required,
            }
        if not gates:
            gates = {
                "G1-DESIGN": {"name": "Design Gate", "required_agents": ["DEV-001"]},
                "G2-SECURITY": {"name": "Security Gate", "required_agents": ["SEC-001", "SEC-002"]},
                "G3-CODE": {"name": "Code Gate", "required_agents": ["DEV-004"]},
                "G4-TEST": {"name": "Test Gate", "required_agents": ["QA-001", "QA-002"]},
                "G5-DEPLOY": {"name": "Deploy Gate", "required_agents": ["INF-005"]},
            }
        return gates

    def _normalize(self, text: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

    def _keyword_in_text(self, keyword: str, normalized_text: str, tokens: List[str]) -> bool:
        normalized_keyword = self._normalize(keyword.replace("-", " "))
        if not normalized_keyword:
            return False
        if " " in normalized_keyword:
            return normalized_keyword in normalized_text
        return normalized_keyword in tokens

    def _route_agents(self, task: str) -> List[str]:
        normalized_text = self._normalize(task)
        tokens = normalized_text.split()
        routed: List[str] = []
        for keyword, agents in self._routing_keywords.items():
            if self._keyword_in_text(keyword, normalized_text, tokens):
                for agent in agents:
                    if agent not in routed:
                        routed.append(agent)
        return routed

    def _select_status_templates(self, agent_id: str) -> Tuple[str, str]:
        agent = self._agents.get(agent_id, {})
        templates = agent.get("status_templates", [])
        working = templates[0] if templates else "Working now"
        complete = templates[-1] if templates else "Work complete"
        return working, complete

    def _enforce_status_words(self, status: str) -> str:
        words = status.split()
        if not words:
            words = ["Working", "now"]
        if len(words) == 1:
            words.append("ready")
        if len(words) > 4:
            words = words[:4]
        return " ".join(words)

    def _format_status_line(self, agent_id: str, status: str) -> str:
        return f"[{agent_id}] {self._enforce_status_words(status)}"

    def _summarize_task(self, task: str, max_len: int = 54) -> str:
        cleaned = " ".join(task.split())
        if len(cleaned) <= max_len:
            return cleaned
        trimmed = cleaned[: max_len - 3].rstrip()
        return f"{trimmed}..."

    def _format_box_line(self, text: str) -> str:
        if len(text) > REPORT_WIDTH:
            text = self._summarize_task(text, REPORT_WIDTH)
        return f"║{text:<{REPORT_WIDTH}}║"

    def _wrap_lines(self, text: str, width: int) -> List[str]:
        words = text.split()
        if not words:
            return ["".ljust(width)]
        lines: List[str] = []
        current = words[0]
        for word in words[1:]:
            if len(current) + 1 + len(word) <= width:
                current = f"{current} {word}"
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def _build_deliverables(self, agent_ids: List[str], failures: List[str]) -> List[str]:
        deliverable_map = {
            "DEV-001": "Architecture plan drafted",
            "DEV-002": "Backend implementation plan",
            "DEV-003": "UI implementation plan",
            "DEV-004": "Code review checklist",
            "DEV-005": "Documentation outline",
            "DEV-006": "CI/CD workflow notes",
            "SEC-001": "Threat model summary",
            "SEC-002": "Security test plan",
            "SEC-003": "Malware analysis notes",
            "SEC-004": "Wireless audit outline",
            "SEC-005": "Compliance gap list",
            "SEC-006": "Incident response plan",
            "INF-001": "Infrastructure design outline",
            "INF-002": "System configuration plan",
            "INF-003": "Network configuration plan",
            "INF-004": "Database readiness notes",
            "INF-005": "Deployment readiness checks",
            "INF-006": "Automation runbook",
            "QA-001": "QA strategy checklist",
            "QA-002": "Test automation plan",
            "QA-003": "Performance test plan",
            "QA-004": "Security testing checklist",
            "QA-005": "Manual test plan",
            "QA-006": "Test data plan",
        }
        deliverables: List[str] = []
        for agent_id in agent_ids:
            item = deliverable_map.get(agent_id)
            if item and item not in deliverables:
                deliverables.append(item)
        if failures:
            deliverables.append("Errors detected - review needed")
        if not deliverables:
            deliverables = ["Task plan completed", "Quality gates checked"]
        return deliverables[:4]

    def _build_gate_status(
        self,
        agent_ids: List[str],
        agent_results: Dict[str, AgentResult],
    ) -> Dict[str, str]:
        status: Dict[str, str] = {}
        for gate_id, gate_info in self._gates.items():
            required_agents = gate_info.get("required_agents", [])
            if not required_agents:
                status[gate_id] = "SKIPPED"
                continue
            if any(
                agent_results.get(agent) and agent_results[agent].status == "error"
                for agent in required_agents
            ):
                status[gate_id] = "BLOCKED"
            elif any(agent in agent_ids for agent in required_agents):
                status[gate_id] = "PASSED"
            else:
                status[gate_id] = "SKIPPED"
        return status

    def _build_report(
        self,
        task: str,
        agent_ids: List[str],
        gate_status: Dict[str, str],
        started_at: datetime,
        failures: List[str],
    ) -> str:
        duration_seconds = max(1, int((datetime.utcnow() - started_at).total_seconds()))
        duration = f"{duration_seconds}s"
        task_summary = self._summarize_task(task)
        deliverables = self._build_deliverables(agent_ids, failures)
        total_gates = len(self._gates)
        passed_gates = sum(1 for status in gate_status.values() if status == "PASSED")

        summary_text = (
            f"Coordinated {len(agent_ids)} agents for: {task_summary}. "
            f"Quality gates passed {passed_gates}/{total_gates}."
        )
        if failures:
            summary_text += " Some agents failed; review required."

        lines = [
            BOX_TOP,
            self._format_box_line(" HIVEMIND EXECUTION REPORT".ljust(REPORT_WIDTH - 1)),
            BOX_DIVIDER,
            self._format_box_line(f" Task: {task_summary}"),
            self._format_box_line(" Status: COMPLETE" if not failures else " Status: BLOCKED"),
            self._format_box_line(f" Duration: {duration}"),
            BOX_DIVIDER,
            self._format_box_line(" AGENTS ENGAGED:"),
        ]

        for agent_id in agent_ids:
            agent = self._agents.get(agent_id, {})
            role = agent.get("name") or agent.get("role") or "Agent"
            label = f" {agent_id} {role}".strip()
            suffix = " Complete" if agent_id not in failures else " Error"
            dots_needed = max(1, REPORT_WIDTH - len(label) - len(suffix) - 4)
            dot_fill = "." * dots_needed
            line = f" • {label} {dot_fill} {suffix}"
            lines.append(self._format_box_line(line))

        lines.append(BOX_DIVIDER)
        lines.append(self._format_box_line(" QUALITY GATES:"))
        for gate_id, status in gate_status.items():
            lines.append(self._format_box_line(f" • {gate_id}: {status}"))

        lines.append(BOX_DIVIDER)
        lines.append(self._format_box_line(" DELIVERABLES:"))
        for item in deliverables:
            lines.append(self._format_box_line(f" • {item}"))

        lines.append(BOX_DIVIDER)
        lines.append(self._format_box_line(" SUMMARY:"))
        for wrapped in self._wrap_lines(summary_text, REPORT_WIDTH - 2):
            lines.append(self._format_box_line(f" {wrapped}"))
        lines.append(BOX_BOTTOM)
        return "\n".join(lines)

    def _render_status(self) -> str:
        version_file = self._repo_root / "VERSION"
        version = version_file.read_text(encoding="utf-8").strip() if version_file.exists() else "2.0.0"
        orchestrator = self._settings.get("system", {}).get("orchestrator", "HEAD_CODEX")
        session_id = self._memory.session_id or "None"
        return "\n".join(
            [
                "HIVEMIND STATUS",
                f"Version: {version}",
                f"Orchestrator: {orchestrator}",
                f"Agents loaded: {len(self._agents)}",
                f"Teams loaded: {len(self._team_members)}",
                f"Session: {session_id}",
            ]
        )

    def _render_recall(self, query: str) -> str:
        entries = self._memory.recall(query, limit=5)
        if not entries:
            return "No matching session memory found."
        lines = ["Session Recall:"]
        for entry in entries:
            timestamp = entry.get("timestamp", "unknown")
            task = entry.get("task", "")
            lines.append(f"- {timestamp}: {task}")
        return "\n".join(lines)

    def _parse_command(self, user_input: str) -> Tuple[Optional[str], str]:
        text = user_input.strip()
        if not text.startswith("/"):
            return None, text
        parts = text.split(maxsplit=1)
        command = parts[0][1:].lower()
        task = parts[1].strip() if len(parts) > 1 else ""
        return command, task

    async def _progress_ticker(self, label: str, stop: asyncio.Event) -> None:
        while not stop.is_set():
            await asyncio.sleep(self._progress_interval)
            if not stop.is_set():
                self._emit_status(label)

    async def _run_subprocess(
        self,
        cmd: List[str],
        timeout: float,
        status_label: Optional[str] = None,
    ) -> Tuple[int, str, str]:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.working_dir),
            start_new_session=True,
        )
        self._pending_processes.append(process)

        stop_event = asyncio.Event()
        ticker_task = None
        if status_label:
            ticker_task = asyncio.create_task(self._progress_ticker(status_label, stop_event))

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            return process.returncode or 0, stdout.decode("utf-8", errors="replace"), stderr.decode("utf-8", errors="replace")
        except asyncio.TimeoutError:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except (ProcessLookupError, OSError):
                process.kill()
            await process.wait()
            return 124, "", f"Request timed out after {timeout}s"
        except asyncio.CancelledError:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except (ProcessLookupError, OSError):
                process.kill()
            await process.wait()
            raise
        finally:
            stop_event.set()
            if ticker_task:
                ticker_task.cancel()
            if process in self._pending_processes:
                self._pending_processes.remove(process)

    async def _call_codex_cli(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[bool, str]:
        codex_path = self.auth.codex_path if self.auth else None
        if not codex_path:
            return False, "Codex CLI not available"

        if system_prompt:
            full_prompt = f"SYSTEM PROMPT:\n{system_prompt}\n\nTASK:\n{prompt}"
        else:
            full_prompt = prompt

        fd, output_file = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        cmd = [
            codex_path,
            "exec",
            "--full-auto",
            "--skip-git-repo-check",
            "-o",
            output_file,
            full_prompt,
        ]

        code, stdout, stderr = await self._run_subprocess(
            cmd,
            timeout=timeout or self._codex_timeout,
            status_label="Waiting on Codex...",
        )

        response = ""
        try:
            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as handle:
                    response = handle.read().strip()
        finally:
            try:
                os.remove(output_file)
            except OSError:
                pass

        if code == 0 and response:
            return True, response
        if code == 0 and not response:
            response = stdout.strip() or "No response from Codex"
        error = stderr.strip() or response or "Codex error"
        return False, error

    async def _run_agents(
        self,
        agent_ids: List[str],
        claude_agent: ClaudeAgent,
        plan: str,
        request: str,
    ) -> Tuple[List[str], Dict[str, AgentResult]]:
        status_lines: List[str] = []
        results: Dict[str, AgentResult] = {}

        for agent_id in agent_ids:
            working, complete = self._select_status_templates(agent_id)
            working_status = self._enforce_status_words(working)
            complete_status = self._enforce_status_words(complete)

            self._emit_agent_update(agent_id, "working", working_status)

            result = await claude_agent.execute_agent_task(
                agent_id,
                plan,
                context=request,
            )
            results[agent_id] = result

            if result.status == "complete":
                final_status = complete_status
                self._emit_agent_update(agent_id, "complete", final_status)
            else:
                final_status = "ERROR agent failed"
                self._emit_agent_update(agent_id, "error", final_status)

            status_lines.append(self._format_status_line(agent_id, final_status))

        return status_lines, results

    async def process(self, user_input: str) -> CodexResponse:
        self._conversation_history.append({"role": "user", "content": user_input})

        try:
            command, task = self._parse_command(user_input)
            debug_mode = command == "debug"

            if command in ("help", "?"):
                return CodexResponse(content=HELP_TEXT, source=ResponseSource.CODEX_DIRECT)
            if command == "status":
                return CodexResponse(content=self._render_status(), source=ResponseSource.CODEX_DIRECT)
            if command == "recall":
                return CodexResponse(content=self._render_recall(task), source=ResponseSource.CODEX_DIRECT)

            if command and command not in TEAM_COMMANDS and command not in SINGLE_AGENT_COMMANDS and command not in (
                "hivemind",
                "debug",
            ):
                return CodexResponse(
                    content=f"Unknown command '{command}'. Use /help for available commands.",
                    source=ResponseSource.CODEX_DIRECT,
                    success=False,
                )

            if command and not task and command not in ("help", "?"):
                return CodexResponse(
                    content="Command requires a task description.",
                    source=ResponseSource.CODEX_DIRECT,
                    success=False,
                )

            task_text = task or user_input
            forced_agents: List[str] = []
            debug_lines: List[str] = []

            if command in TEAM_COMMANDS:
                team = TEAM_COMMANDS[command]
                forced_agents = self._team_members.get(team, [])
                debug_lines.append(f"Debug: team={team}")
            elif command in SINGLE_AGENT_COMMANDS:
                forced_agents = [SINGLE_AGENT_COMMANDS[command]]
                debug_lines.append(f"Debug: agent={forced_agents[0]}")
            elif command in ("hivemind", "debug"):
                debug_lines.append("Debug: scope=all")

            if not self.auth or not self.auth.codex_path or not self.auth.claude_path:
                return CodexResponse(
                    content="Codex and Claude CLIs must be installed and authenticated.",
                    source=ResponseSource.CODEX_DIRECT,
                    success=False,
                )

            self._emit_status("Parsing request...")
            claude_agent = ClaudeAgent(
                self.auth,
                working_dir=self.working_dir,
                timeout=self._claude_timeout,
                progress_interval=self._progress_interval,
                on_status=self._emit_status,
            )
            dialogue = CodexClaudeDialogue(
                self,
                claude_agent,
                max_turns=self._dialogue_turns,
            )
            consensus: DialogueResult = await dialogue.discuss(task_text)
            if not consensus.success:
                return CodexResponse(
                    content=consensus.error or "Failed to reach consensus.",
                    source=ResponseSource.CODEX_DIRECT,
                    success=False,
                )

            agents = consensus.agents_used
            if forced_agents:
                agents = forced_agents
            if not agents:
                agents = self._route_agents(task_text)
            if not agents:
                agents = ["DEV-001"]

            self._emit_orchestration_start(task_text, agents)
            self._emit_status("Executing agents...")

            started_at = datetime.utcnow()
            status_lines, agent_results = await self._run_agents(
                agents,
                claude_agent,
                consensus.plan or task_text,
                task_text,
            )

            failures = [agent_id for agent_id, result in agent_results.items() if result.status == "error"]

            self._emit_status("Evaluating quality gates...")
            gate_status = self._build_gate_status(agents, agent_results)
            for gate_id, status in gate_status.items():
                self._emit_gate_update(gate_id, status)

            gate_lines = [f"[GATE] {gate_id}: {status}" for gate_id, status in gate_status.items()]

            self._emit_status("Compiling report...")
            report = self._build_report(task_text, agents, gate_status, started_at, failures)

            output_sections: List[str] = []
            output_sections.extend(status_lines)
            output_sections.append("")
            output_sections.extend(gate_lines)
            output_sections.append("")
            output_sections.append(report)

            if debug_mode:
                output_sections.append("")
                output_sections.append("DEBUG")
                output_sections.extend(debug_lines)
                output_sections.append(f"Debug: routed_agents={', '.join(agents)}")
                output_sections.append(f"Debug: plan={consensus.plan}")

            content = "\n".join(output_sections).strip()

            self._memory.record_task(task_text, agents, gate_status, report, status_lines)

            response = CodexResponse(
                content=content,
                source=ResponseSource.AGENTS,
                success=not failures,
                error="Agent errors detected" if failures else None,
                agents_used=agents,
                dialogue_turns=consensus.turns,
            )

            self._conversation_history.append({"role": "assistant", "content": response.content})
            return response

        except asyncio.CancelledError:
            raise
        except Exception as e:
            return CodexResponse(
                content=f"Error: {str(e)}",
                source=ResponseSource.CODEX_DIRECT,
                success=False,
                error=str(e),
            )

    def clear_history(self) -> None:
        self._conversation_history = []

    def _can_handle_alone(self, user_input: str) -> bool:
        command, _ = self._parse_command(user_input)
        return command in ("help", "status", "recall")
