"""
HIVEMIND CLI Main Application

Typer-based CLI for HIVEMIND backend management and operations.
"""

import asyncio
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from hivemind.cli.manager import CLIManager
from hivemind.config import get_settings
from hivemind.observability import configure_logging, get_logger

app = typer.Typer(
    name="hivemind",
    help="HIVEMIND Backend CLI - Multi-agent AI orchestration system",
    add_completion=False,
)

console = Console()
logger = get_logger(__name__)


@app.command()
def run(
    agent_id: str = typer.Argument(..., help="Agent ID to execute (e.g., DEV-001)"),
    task: str = typer.Argument(..., help="Task description"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override model"),
    timeout: float = typer.Option(300.0, "--timeout", "-t", help="Execution timeout in seconds"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save output to file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Execute a task using a specific agent via Claude/Codex CLI.

    Examples:
        hivemind run DEV-001 "Design REST API for user authentication"
        hivemind run SEC-002 "Review code for security vulnerabilities" --model claude-opus-4
    """
    settings = get_settings()
    configure_logging(
        level="DEBUG" if verbose else settings.observability.log_level,
        format_type=settings.observability.log_format
    )

    console.print(f"[bold cyan]HIVEMIND[/bold cyan] Running agent [yellow]{agent_id}[/yellow]")
    console.print(f"[dim]Task: {task}[/dim]\n")

    async def _run():
        manager = CLIManager()
        try:
            result = await manager.execute_task(
                agent_id=agent_id,
                task=task,
                model=model,
                timeout=timeout
            )

            console.print("[bold green]✓[/bold green] Task completed successfully\n")
            console.print("[bold]Output:[/bold]")
            console.print(result.get("output", "No output"))

            if output_file:
                output_file.write_text(json.dumps(result, indent=2))
                console.print(f"\n[dim]Saved to {output_file}[/dim]")

            return result

        except Exception as e:
            console.print(f"[bold red]✗[/bold red] Error: {e}")
            logger.exception(f"Failed to execute task for agent {agent_id}")
            raise typer.Exit(1)

    asyncio.run(_run())


@app.command()
def status(
    agent_id: Optional[str] = typer.Argument(None, help="Specific agent ID to check"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """
    Check the status of HIVEMIND agents and services.

    Examples:
        hivemind status
        hivemind status DEV-001
        hivemind status --json
    """
    settings = get_settings()

    async def _status():
        manager = CLIManager()
        status_data = await manager.get_status(agent_id)

        if json_output:
            console.print_json(data=status_data)
        else:
            _display_status_table(status_data)

    asyncio.run(_status())


def _display_status_table(status_data: dict):
    """Display status information in a rich table."""
    table = Table(title="HIVEMIND Status", show_header=True, header_style="bold cyan")
    table.add_column("Component", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    # System status
    system_status = status_data.get("system", {})
    table.add_row(
        "System",
        "✓" if system_status.get("healthy") else "✗",
        f"Uptime: {system_status.get('uptime', 'N/A')}"
    )

    # Agents status
    agents_status = status_data.get("agents", {})
    for agent_id, agent_info in agents_status.items():
        table.add_row(
            agent_id,
            "✓" if agent_info.get("available") else "✗",
            f"Tasks: {agent_info.get('task_count', 0)}"
        )

    # Services status
    services_status = status_data.get("services", {})
    for service, service_info in services_status.items():
        table.add_row(
            service,
            "✓" if service_info.get("connected") else "✗",
            service_info.get("message", "")
        )

    console.print(table)


@app.command()
def agents(
    team: Optional[str] = typer.Option(None, "--team", "-t", help="Filter by team (DEV, SEC, INF, QA)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """
    List all available agents and their capabilities.

    Examples:
        hivemind agents
        hivemind agents --team DEV
        hivemind agents --json
    """
    settings = get_settings()

    agents_config_path = settings.agents_config_path
    if not agents_config_path.exists():
        console.print(f"[red]Error: Agents config not found at {agents_config_path}[/red]")
        raise typer.Exit(1)

    with open(agents_config_path) as f:
        agents_data = json.load(f)

    if team:
        agents_data = {
            aid: info for aid, info in agents_data.items()
            if aid.startswith(team.upper())
        }

    if json_output:
        console.print_json(data=agents_data)
    else:
        _display_agents_table(agents_data)


def _display_agents_table(agents_data: dict):
    """Display agents information in a rich table."""
    table = Table(title="HIVEMIND Agents", show_header=True, header_style="bold cyan")
    table.add_column("Agent ID", style="cyan")
    table.add_column("Name", style="yellow")
    table.add_column("Team", justify="center")
    table.add_column("Capabilities", style="dim")

    for agent_id, agent_info in agents_data.items():
        capabilities = ", ".join(agent_info.get("capabilities", [])[:3])
        if len(agent_info.get("capabilities", [])) > 3:
            capabilities += "..."

        table.add_row(
            agent_id,
            agent_info.get("name", "Unknown"),
            agent_info.get("team", "N/A"),
            capabilities
        )

    console.print(table)


@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    validate: bool = typer.Option(False, "--validate", help="Validate configuration"),
    component: Optional[str] = typer.Option(None, "--component", "-c", help="Show specific component config"),
):
    """
    Manage HIVEMIND configuration.

    Examples:
        hivemind config --show
        hivemind config --validate
        hivemind config --component claude
    """
    settings = get_settings()

    if validate:
        console.print("[bold cyan]Validating configuration...[/bold cyan]\n")
        issues = _validate_config(settings)

        if issues:
            console.print("[bold red]Configuration issues found:[/bold red]")
            for issue in issues:
                console.print(f"  [red]✗[/red] {issue}")
            raise typer.Exit(1)
        else:
            console.print("[bold green]✓[/bold green] Configuration is valid")

    elif show:
        if component:
            component_config = getattr(settings, component, None)
            if component_config is None:
                console.print(f"[red]Unknown component: {component}[/red]")
                raise typer.Exit(1)

            console.print(f"[bold cyan]{component.upper()} Configuration:[/bold cyan]")
            console.print_json(data=component_config.model_dump())
        else:
            console.print("[bold cyan]HIVEMIND Configuration:[/bold cyan]")
            # Redact sensitive information
            config_dict = settings.model_dump()
            _redact_secrets(config_dict)
            console.print_json(data=config_dict)

    else:
        console.print("Use --show to display configuration or --validate to check it")


def _validate_config(settings) -> list[str]:
    """Validate configuration and return list of issues."""
    issues = []

    # Check Claude configuration
    if settings.claude.enabled:
        if settings.claude.api_key is None:
            issues.append("Claude enabled but ANTHROPIC_API_KEY not set")

    # Check Codex configuration
    if settings.codex.enabled:
        if settings.codex.api_key is None:
            issues.append("Codex enabled but OPENAI_API_KEY not set")

    # Check database configuration
    if settings.env.value == "production":
        if "hivemind_secret" in settings.postgres.password.get_secret_value():
            issues.append("Using default database password in production")

        if "CHANGE_ME" in settings.security.jwt_secret_key.get_secret_value():
            issues.append("Using default JWT secret in production")

    # Check required paths
    if not settings.agents_config_path.exists():
        issues.append(f"Agents config not found: {settings.agents_config_path}")

    if not settings.routing_config_path.exists():
        issues.append(f"Routing config not found: {settings.routing_config_path}")

    return issues


def _redact_secrets(config_dict: dict, redacted: str = "***REDACTED***"):
    """Recursively redact secret values in configuration dictionary."""
    for key, value in config_dict.items():
        if isinstance(value, dict):
            _redact_secrets(value, redacted)
        elif "password" in key.lower() or "secret" in key.lower() or "key" in key.lower():
            config_dict[key] = redacted


@app.command()
def version():
    """Display HIVEMIND version information."""
    settings = get_settings()

    console.print(f"[bold cyan]HIVEMIND[/bold cyan] v{settings.observability.service_version}")
    console.print(f"Environment: [yellow]{settings.env.value}[/yellow]")
    console.print(f"Python: {__import__('sys').version.split()[0]}")


if __name__ == "__main__":
    app()
