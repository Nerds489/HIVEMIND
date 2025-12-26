# DESTINATION: tui/src/hivemind_tui/screens/auth_screen.py
# CREATE THIS FILE AT THE EXACT PATH ABOVE
# DO NOT MODIFY THIS CODE

"""
HIVEMIND Authentication Screen.

Handles authentication flow for both Codex and Claude.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Center
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, LoadingIndicator
from textual.binding import Binding

from ..engine.auth import AuthManager, AuthStatus


class AuthScreen(Screen):
    """Authentication screen for HIVEMIND."""
    
    BINDINGS = [
        Binding("escape", "app.quit", "Quit", show=True),
        Binding("r", "retry", "Retry", show=True),
    ]
    
    def __init__(self, auth_manager: AuthManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_manager = auth_manager
        self._checking = False
    
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
        self.run_worker(self._do_check_auth())
    
    async def _do_check_auth(self) -> None:
        """Perform auth check."""
        try:
            state = await self.auth_manager.check_all()
            
            # Update Codex status
            codex_widget = self.query_one("#codex-status", Static)
            if state.codex.status == AuthStatus.AUTHENTICATED:
                codex_widget.update(f"[green]✓ Codex: Authenticated ({state.codex.method.value})[/green]")
            elif state.codex.status == AuthStatus.PENDING:
                codex_widget.update("[yellow]○ Codex: Not authenticated[/yellow]")
            else:
                codex_widget.update(f"[red]✗ Codex: {state.codex.error}[/red]")
            
            # Update Claude status
            claude_widget = self.query_one("#claude-status", Static)
            if state.claude.status == AuthStatus.AUTHENTICATED:
                claude_widget.update(f"[green]✓ Claude: Authenticated ({state.claude.method.value})[/green]")
            elif state.claude.status == AuthStatus.PENDING:
                claude_widget.update("[yellow]○ Claude: Not authenticated[/yellow]")
            else:
                claude_widget.update(f"[red]✗ Claude: {state.claude.error}[/red]")
            
            # Update buttons
            codex_btn = self.query_one("#auth-codex-btn", Button)
            claude_btn = self.query_one("#auth-claude-btn", Button)
            continue_btn = self.query_one("#continue-btn", Button)
            
            codex_btn.disabled = state.codex.status == AuthStatus.AUTHENTICATED
            claude_btn.disabled = state.claude.status == AuthStatus.AUTHENTICATED
            continue_btn.disabled = not state.codex_ready  # At minimum need Codex
            
            # Update overall status
            status_widget = self.query_one("#auth-status", Static)
            if state.both_ready:
                status_widget.update("[green]All engines authenticated![/green]")
            elif state.codex_ready:
                status_widget.update("[yellow]Codex ready. Claude optional but recommended.[/yellow]")
            else:
                status_widget.update("[yellow]Please authenticate at least Codex to continue.[/yellow]")
                
        except Exception as e:
            self.query_one("#auth-status", Static).update(f"[red]Error: {str(e)}[/red]")
        finally:
            self.query_one("#auth-loading", LoadingIndicator).display = False
            self._checking = False
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "auth-codex-btn":
            await self._authenticate_codex()
        elif button_id == "auth-claude-btn":
            await self._authenticate_claude()
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
        self.app.switch_screen(MainScreen(self.auth_manager))
    
    def action_retry(self) -> None:
        """Retry auth check."""
        self._check_auth()
