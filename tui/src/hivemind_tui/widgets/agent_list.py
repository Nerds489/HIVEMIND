"""Agent List Widget - Display HIVEMIND v2.0 agents grouped by team."""

from dataclasses import dataclass
from typing import Optional, Dict

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static


@dataclass
class Agent:
    """Agent data structure."""
    id: str
    name: str
    role: str
    team: str
    status: str = "idle"  # idle, working, complete, error
    current_task: Optional[str] = None


# HIVEMIND v2.0 Agent Registry - 24 Agents across 4 Teams
HIVEMIND_AGENTS = [
    # Development Team (DEV-001 to DEV-006)
    Agent("DEV-001", "Architect", "System Architecture", "Development"),
    Agent("DEV-002", "Backend Dev", "Backend Implementation", "Development"),
    Agent("DEV-003", "Frontend Dev", "Frontend Implementation", "Development"),
    Agent("DEV-004", "Code Reviewer", "Code Review", "Development"),
    Agent("DEV-005", "Tech Writer", "Documentation", "Development"),
    Agent("DEV-006", "DevOps", "CI/CD & Deployment", "Development"),

    # Security Team (SEC-001 to SEC-006)
    Agent("SEC-001", "Sec Architect", "Security Design", "Security"),
    Agent("SEC-002", "Pentester", "Penetration Testing", "Security"),
    Agent("SEC-003", "Malware Analyst", "Threat Analysis", "Security"),
    Agent("SEC-004", "Wireless Sec", "Wireless/IoT Security", "Security"),
    Agent("SEC-005", "Compliance", "Compliance Auditing", "Security"),
    Agent("SEC-006", "Incident Resp", "Incident Response", "Security"),

    # Infrastructure Team (INF-001 to INF-006)
    Agent("INF-001", "Infra Architect", "Cloud Architecture", "Infrastructure"),
    Agent("INF-002", "SysAdmin", "System Administration", "Infrastructure"),
    Agent("INF-003", "Network Eng", "Networking", "Infrastructure"),
    Agent("INF-004", "DBA", "Database Management", "Infrastructure"),
    Agent("INF-005", "SRE", "Site Reliability", "Infrastructure"),
    Agent("INF-006", "Automation Eng", "IaC & Automation", "Infrastructure"),

    # QA Team (QA-001 to QA-006)
    Agent("QA-001", "QA Architect", "Test Strategy", "QA"),
    Agent("QA-002", "Test Auto", "Test Automation", "QA"),
    Agent("QA-003", "Perf Tester", "Performance Testing", "QA"),
    Agent("QA-004", "Sec Tester", "Security Testing", "QA"),
    Agent("QA-005", "Manual QA", "Manual Testing", "QA"),
    Agent("QA-006", "Test Data", "Test Data Management", "QA"),
]


class AgentListWidget(Widget):
    """Widget to display HIVEMIND agents grouped by team."""

    selected_agent: reactive[Optional[str]] = reactive(None)

    class AgentSelected(Message):
        """Message sent when an agent is selected."""
        def __init__(self, agent: Agent) -> None:
            super().__init__()
            self.agent = agent

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create a mutable copy of agents
        self._agents: Dict[str, Agent] = {
            agent.id: Agent(
                id=agent.id,
                name=agent.name,
                role=agent.role,
                team=agent.team,
                status=agent.status,
                current_task=agent.current_task,
            )
            for agent in HIVEMIND_AGENTS
        }
        self._agent_items: Dict[str, "AgentItem"] = {}

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with VerticalScroll(id="agent-scroll"):
            # Group agents by team
            teams: Dict[str, list] = {}
            for agent_id, agent in self._agents.items():
                if agent.team not in teams:
                    teams[agent.team] = []
                teams[agent.team].append(agent)

            # Render each team in order
            team_order = ["Development", "Security", "Infrastructure", "QA"]
            for team_name in team_order:
                if team_name in teams:
                    yield Static(f"[bold cyan]{team_name}[/bold cyan]", classes="team-header")

                    for agent in teams[team_name]:
                        item = AgentItem(agent)
                        self._agent_items[agent.id] = item
                        yield item

    def update_agent_status(
        self,
        agent_id: str,
        status: str,
        message: Optional[str] = None,
    ) -> None:
        """Update an agent's status.

        Args:
            agent_id: Agent ID (e.g., "DEV-001")
            status: New status (idle, working, complete, error)
            message: Optional status message / current task
        """
        if agent_id in self._agents:
            self._agents[agent_id].status = status
            self._agents[agent_id].current_task = message

            if agent_id in self._agent_items:
                self._agent_items[agent_id].update_status(status, message)

    def reset_all_agents(self) -> None:
        """Reset all agents to idle status."""
        for agent_id in self._agents:
            self._agents[agent_id].status = "idle"
            self._agents[agent_id].current_task = None

            if agent_id in self._agent_items:
                self._agent_items[agent_id].update_status("idle", None)

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID.

        Args:
            agent_id: Agent ID

        Returns:
            Agent object or None
        """
        return self._agents.get(agent_id)

    def get_active_agents(self) -> list:
        """Get list of currently active (working) agents.

        Returns:
            List of Agent objects with working status
        """
        return [
            agent for agent in self._agents.values()
            if agent.status == "working"
        ]


class AgentItem(Static):
    """Individual agent item in the list."""

    def __init__(self, agent: Agent, **kwargs) -> None:
        super().__init__(**kwargs)
        self.agent = agent
        self.update(self._render_agent())

    def _render_agent(self) -> Text:
        """Render agent information."""
        status_icons = {
            "idle": "○",
            "working": "◐",
            "complete": "✓",
            "error": "✗",
        }
        status_colors = {
            "idle": "dim",
            "working": "yellow",
            "complete": "green",
            "error": "red",
        }

        status_icon = status_icons.get(self.agent.status, "○")
        status_color = status_colors.get(self.agent.status, "white")

        text = Text()
        text.append(f"{status_icon} ", style=status_color)
        text.append(f"[{self.agent.id}] ", style="dim cyan")
        text.append(f"{self.agent.name}", style="bold" if self.agent.status == "working" else "")

        if self.agent.current_task:
            # Truncate long tasks
            task = self.agent.current_task[:25] + "..." if len(self.agent.current_task) > 25 else self.agent.current_task
            text.append(f"\n   → {task}", style="italic cyan")

        return text

    def update_status(self, status: str, current_task: Optional[str] = None) -> None:
        """Update agent status.

        Args:
            status: New status (idle, working, complete, error)
            current_task: Optional current task description
        """
        self.agent.status = status
        self.agent.current_task = current_task
        self.update(self._render_agent())

        # Add/remove visual emphasis
        if status == "working":
            self.add_class("agent-active")
        else:
            self.remove_class("agent-active")

    def on_click(self) -> None:
        """Handle click event."""
        self.add_class("selected")
        # Remove selected class from siblings
        if self.parent:
            for sibling in self.parent.query(AgentItem):
                if sibling != self:
                    sibling.remove_class("selected")
