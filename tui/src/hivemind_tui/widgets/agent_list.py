"""Agent List Widget - Display and manage 24 agents grouped by team."""

from dataclasses import dataclass
from typing import Optional

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, ListItem, ListView


@dataclass
class Agent:
    """Agent data structure."""

    id: str
    name: str
    role: str
    team: str
    status: str = "idle"  # idle, busy, error
    current_task: Optional[str] = None


class AgentListWidget(Widget):
    """Widget to display agents grouped by team."""

    selected_agent: reactive[Optional[str]] = reactive(None)

    # Define 24 agents across 6 teams (4 agents per team)
    AGENTS = [
        # Strategy Team
        Agent("strategy-001", "Strategist Alpha", "Lead Strategy", "Strategy", "idle"),
        Agent("strategy-002", "Planner Beta", "Planning", "Strategy", "idle"),
        Agent("strategy-003", "Analyst Gamma", "Analysis", "Strategy", "idle"),
        Agent("strategy-004", "Coordinator Delta", "Coordination", "Strategy", "idle"),

        # Engineering Team
        Agent("eng-001", "Architect Prime", "System Architecture", "Engineering", "idle"),
        Agent("eng-002", "Developer Apex", "Implementation", "Engineering", "idle"),
        Agent("eng-003", "DevOps Sigma", "Operations", "Engineering", "idle"),
        Agent("eng-004", "QA Validator", "Quality Assurance", "Engineering", "idle"),

        # Research Team
        Agent("research-001", "Researcher Omega", "Lead Research", "Research", "idle"),
        Agent("research-002", "Data Scientist", "Data Analysis", "Research", "idle"),
        Agent("research-003", "ML Specialist", "Machine Learning", "Research", "idle"),
        Agent("research-004", "Knowledge Curator", "Knowledge Management", "Research", "idle"),

        # Documentation Team
        Agent("docs-001", "Doc Master", "Lead Documentation", "Documentation", "idle"),
        Agent("docs-002", "Technical Writer", "Technical Writing", "Documentation", "idle"),
        Agent("docs-003", "API Documenter", "API Documentation", "Documentation", "idle"),
        Agent("docs-004", "Tutorial Creator", "Tutorial Creation", "Documentation", "idle"),

        # Security Team
        Agent("sec-001", "Security Chief", "Lead Security", "Security", "idle"),
        Agent("sec-002", "Penetration Tester", "Security Testing", "Security", "idle"),
        Agent("sec-003", "Code Auditor", "Code Security", "Security", "idle"),
        Agent("sec-004", "Compliance Officer", "Compliance", "Security", "idle"),

        # Communication Team
        Agent("comm-001", "Comm Director", "Lead Communication", "Communication", "idle"),
        Agent("comm-002", "UX Specialist", "User Experience", "Communication", "idle"),
        Agent("comm-003", "Support Agent", "User Support", "Communication", "idle"),
        Agent("comm-004", "Community Manager", "Community", "Communication", "idle"),
    ]

    class AgentSelected(Message):
        """Message sent when an agent is selected."""

        def __init__(self, agent: Agent) -> None:
            super().__init__()
            self.agent = agent

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with VerticalScroll(id="agent-scroll"):
            # Group agents by team
            teams = {}
            for agent in self.AGENTS:
                if agent.team not in teams:
                    teams[agent.team] = []
                teams[agent.team].append(agent)

            # Render each team
            for team_name, agents in teams.items():
                yield Static(f"[bold cyan]{team_name}[/bold cyan]", classes="team-header")

                for agent in agents:
                    yield AgentItem(agent)

    @on(ListView.Selected)
    def on_agent_selected(self, event: ListView.Selected) -> None:
        """Handle agent selection."""
        if isinstance(event.item, AgentItem):
            self.selected_agent = event.item.agent.id
            self.post_message(self.AgentSelected(event.item.agent))


class AgentItem(Static):
    """Individual agent item in the list."""

    def __init__(self, agent: Agent, **kwargs) -> None:
        super().__init__(**kwargs)
        self.agent = agent
        self.update(self._render_agent())

    def _render_agent(self) -> Text:
        """Render agent information."""
        status_icon = {
            "idle": "●",
            "busy": "◐",
            "error": "✗"
        }.get(self.agent.status, "○")

        status_color = {
            "idle": "green",
            "busy": "yellow",
            "error": "red"
        }.get(self.agent.status, "white")

        text = Text()
        text.append(f"{status_icon} ", style=status_color)
        text.append(f"{self.agent.name}", style="bold")
        text.append(f"\n   {self.agent.role}", style="dim")

        if self.agent.current_task:
            text.append(f"\n   → {self.agent.current_task}", style="italic cyan")

        return text

    def update_status(self, status: str, current_task: Optional[str] = None) -> None:
        """Update agent status.

        Args:
            status: New status (idle, busy, error)
            current_task: Optional current task description
        """
        self.agent.status = status
        self.agent.current_task = current_task
        self.update(self._render_agent())

    def on_click(self) -> None:
        """Handle click event."""
        self.add_class("selected")
        # Remove selected class from siblings
        for sibling in self.parent.query(AgentItem):
            if sibling != self:
                sibling.remove_class("selected")
