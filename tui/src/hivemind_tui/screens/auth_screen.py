"""
HIVEMIND Authentication Screen.

Handles authentication flow for both Codex and Claude.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Center
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, LoadingIndicator
from textual.binding import Binding
from textual.worker import Worker, WorkerState

from ..engine.auth import AuthManager, AuthStatus


class AuthScreen(Screen):
    """Authentication screen for HIVEMIND."""
    
    BINDINGS = [
        Binding("escape", "app.quit", "Quit", show=True),
        Binding("r", "retry", "Retry", show=True),
        Binding("s", "skip", "Skip Auth", show=True),
        Binding("enter", "continue_if_ready", "Continue", show=False),
    ]
    
    def __init__(self, auth_manager: AuthManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_manager = auth_manager
        self._checking = False
        self._auth_worker: Worker | None = None
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header(show_clock=True)
        
        with Container(id="auth-container"):
            with Center():
                with Vertical(id="auth-panel"):
                    yield Static("HIVEMIND Authentication", id="auth-title")
                    yield Static("", id="auth-status")
                    yield Static("", id="codex-status")
                    yield Static("", id="claude-status")
                    yield LoadingIndicator(id="auth-loading")
                    
                    with Container(id="auth-buttons"):
                        yield Button("Authenticate Codex", id="auth-codex-btn", variant="primary")
                        yield Button("Authenticate Claude", id="auth-claude-btn", variant="primary")
                        yield Button("Continue", id="continue-btn", variant="success", disabled=True)
                        yield Button("Quit", id="quit-btn", variant="error")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Handle screen mount."""
        self.query_one("#auth-loading", LoadingIndicator).display = False
        self._check_auth()
    
    def _check_auth(self) -> None:
        """Check authentication status."""
        if self._checking:
            return

        self._checking = True
        self.query_one("#auth-loading", LoadingIndicator).display = True
        self.query_one("#auth-status", Static).update("Checking authentication...")
        self._auth_worker = self.run_worker(self._do_check_auth(), name="auth_check")
    
    async def _do_check_auth(self):
        """Perform auth check and return the state."""
        return await self.auth_manager.check_all()

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handle worker completion for auth checks."""
        if event.worker.name == "auth_check":
            if event.state == WorkerState.SUCCESS:
                self._update_auth_display(event.worker.result)
            elif event.state == WorkerState.ERROR:
                self.query_one("#auth-status", Static).update(f"[red]Error: {event.worker.error}[/red]")

            if event.state in (WorkerState.SUCCESS, WorkerState.ERROR, WorkerState.CANCELLED):
                self.query_one("#auth-loading", LoadingIndicator).display = False
                self._checking = False

    def _update_auth_display(self, state) -> None:
        """Update the auth display with the given state."""
        # Update Codex status
        codex_widget = self.query_one("#codex-status", Static)
        if state.codex.status == AuthStatus.AUTHENTICATED:
            codex_widget.update(f"[green]* Codex: Authenticated ({state.codex.method.value})[/green]")
        elif state.codex.status == AuthStatus.PENDING:
            codex_widget.update("[yellow]o Codex: Not authenticated[/yellow]")
        else:
            codex_widget.update(f"[red]x Codex: {state.codex.error}[/red]")

        # Update Claude status
        claude_widget = self.query_one("#claude-status", Static)
        if state.claude.status == AuthStatus.AUTHENTICATED:
            claude_widget.update(f"[green]* Claude: Authenticated ({state.claude.method.value})[/green]")
        elif state.claude.status == AuthStatus.PENDING:
            claude_widget.update("[yellow]o Claude: Not authenticated[/yellow]")
        else:
            claude_widget.update(f"[red]x Claude: {state.claude.error}[/red]")

        # Update buttons
        codex_btn = self.query_one("#auth-codex-btn", Button)
        claude_btn = self.query_one("#auth-claude-btn", Button)
        continue_btn = self.query_one("#continue-btn", Button)

        codex_btn.disabled = state.codex.status == AuthStatus.AUTHENTICATED
        claude_btn.disabled = state.claude.status == AuthStatus.AUTHENTICATED

        # Require both engines when not in local mode
        can_continue = state.both_ready
        continue_btn.disabled = not can_continue

        # Update overall status
        status_widget = self.query_one("#auth-status", Static)
        if state.both_ready:
            status_widget.update("[green]All engines authenticated![/green]")
        elif state.codex_ready:
            status_widget.update("[yellow]Codex ready. Claude required to continue.[/yellow]")
        elif state.claude_ready:
            status_widget.update("[yellow]Claude ready. Codex required to continue.[/yellow]")
        else:
            status_widget.update("[red]No authentication available. Install codex or claude CLI.[/red]")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "auth-codex-btn":
            self.run_worker(self._authenticate_codex(), name="codex_auth")
        elif button_id == "auth-claude-btn":
            self.run_worker(self._authenticate_claude(), name="claude_auth")
        elif button_id == "continue-btn":
            self._continue_to_main()
        elif button_id == "quit-btn":
            self.app.exit()
    
    async def _authenticate_codex(self) -> None:
        """Authenticate Codex via browser."""
        self.query_one("#auth-status", Static).update("Opening browser for Codex authentication...")
        self.query_one("#auth-loading", LoadingIndicator).display = True
        
        success, message = await self.auth_manager.authenticate_codex_browser()
        
        self.query_one("#auth-loading", LoadingIndicator).display = False
        
        if success:
            self.query_one("#auth-status", Static).update("[green]Codex authenticated![/green]")
        else:
            self.query_one("#auth-status", Static).update(f"[red]Codex auth failed: {message}[/red]")
        
        self._check_auth()
    
    async def _authenticate_claude(self) -> None:
        """Authenticate Claude via browser."""
        self.query_one("#auth-status", Static).update("Opening browser for Claude authentication...")
        self.query_one("#auth-loading", LoadingIndicator).display = True
        
        success, message = await self.auth_manager.authenticate_claude_browser()
        
        self.query_one("#auth-loading", LoadingIndicator).display = False
        
        if success:
            self.query_one("#auth-status", Static).update("[green]Claude authenticated![/green]")
        else:
            self.query_one("#auth-status", Static).update(f"[red]Claude auth failed: {message}[/red]")
        
        self._check_auth()
    
    def _continue_to_main(self) -> None:
        """Continue to main screen."""
        from .main import MainScreen
        # Switch to main screen (replaces current screen)
        self.app.switch_screen(MainScreen(self.auth_manager))
    
    def action_retry(self) -> None:
        """Retry auth check."""
        self._check_auth()

    def action_skip(self) -> None:
        """Skip authentication and proceed to main screen."""
        self.query_one("#auth-status", Static).update(
            "[red]Skip disabled. Both engines must be authenticated.[/red]"
        )

    def action_continue_if_ready(self) -> None:
        """Continue if authentication is ready (Enter key handler)."""
        continue_btn = self.query_one("#continue-btn", Button)
        if not continue_btn.disabled:
            self._continue_to_main()

    async def on_unmount(self) -> None:
        """Clean up when screen is unmounted."""
        # Cancel any pending auth processes to prevent orphaned processes
        await self.auth_manager.cancel_pending()
