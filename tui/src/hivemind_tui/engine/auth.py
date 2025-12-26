"""
HIVEMIND Authentication Module.

Handles authentication checking for Codex and Claude CLIs.
All I/O operations are made non-blocking to avoid freezing the UI.
"""

import asyncio
import json
import os
import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple


class AuthMethod(str, Enum):
    """Authentication method."""
    BROWSER = "browser"
    API_KEY = "api_key"
    NONE = "none"


class AuthStatus(str, Enum):
    """Authentication status."""
    AUTHENTICATED = "authenticated"
    PENDING = "pending"
    FAILED = "failed"
    NOT_CHECKED = "not_checked"


@dataclass
class EngineAuth:
    """Authentication state for an engine."""
    engine: str  # "codex" or "claude"
    status: AuthStatus
    method: AuthMethod
    username: Optional[str] = None
    error: Optional[str] = None


@dataclass
class AuthState:
    """Combined authentication state."""
    codex: EngineAuth
    claude: EngineAuth

    @property
    def both_ready(self) -> bool:
        """Check if both engines are authenticated."""
        return (
            self.codex.status == AuthStatus.AUTHENTICATED and
            self.claude.status == AuthStatus.AUTHENTICATED
        )

    @property
    def codex_ready(self) -> bool:
        """Check if Codex is authenticated."""
        return self.codex.status == AuthStatus.AUTHENTICATED

    @property
    def claude_ready(self) -> bool:
        """Check if Claude is authenticated."""
        return self.claude.status == AuthStatus.AUTHENTICATED


class AuthManager:
    """Manages authentication for Codex and Claude.

    All public methods that perform I/O are async to avoid blocking the UI.
    """

    def __init__(self):
        self._codex_path: Optional[str] = None
        self._claude_path: Optional[str] = None
        self._state: Optional[AuthState] = None
        self._config_dir = Path.home() / ".config" / "hivemind"
        self._pending_processes: list[asyncio.subprocess.Process] = []
        # Create config dir synchronously in init (one-time, fast operation)
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass  # Ignore if we can't create the config dir

    def _find_codex_sync(self) -> Optional[str]:
        """Find Codex CLI executable (synchronous helper)."""
        if self._codex_path:
            return self._codex_path

        # Check PATH first
        codex_path = shutil.which("codex")
        if codex_path:
            self._codex_path = codex_path
            return codex_path

        # Check common locations
        candidates = [
            Path.home() / ".local" / "bin" / "codex",
            Path.home() / ".volta" / "bin" / "codex",
            Path.home() / ".bun" / "bin" / "codex",
            Path("/usr/local/bin/codex"),
            Path("/usr/bin/codex"),
        ]

        # Check NVM locations
        nvm_dir = Path.home() / ".nvm" / "versions" / "node"
        try:
            if nvm_dir.exists():
                for version_dir in sorted(nvm_dir.iterdir(), reverse=True):
                    candidate = version_dir / "bin" / "codex"
                    if candidate.exists():
                        candidates.insert(0, candidate)
                        break
        except OSError:
            pass  # Ignore permission errors

        for path in candidates:
            try:
                if path.exists() and os.access(path, os.X_OK):
                    self._codex_path = str(path)
                    return self._codex_path
            except OSError:
                continue

        return None

    def _find_claude_sync(self) -> Optional[str]:
        """Find Claude CLI executable (synchronous helper)."""
        if self._claude_path:
            return self._claude_path

        # Check PATH first
        claude_path = shutil.which("claude")
        if claude_path:
            self._claude_path = claude_path
            return claude_path

        # Check common locations
        candidates = [
            Path.home() / ".local" / "bin" / "claude",
            Path("/usr/local/bin/claude"),
            Path("/usr/bin/claude"),
        ]

        for path in candidates:
            try:
                if path.exists() and os.access(path, os.X_OK):
                    self._claude_path = str(path)
                    return self._claude_path
            except OSError:
                continue

        return None

    async def find_codex(self) -> Optional[str]:
        """Find Codex CLI executable (async, non-blocking)."""
        if self._codex_path:
            return self._codex_path
        return await asyncio.to_thread(self._find_codex_sync)

    async def find_claude(self) -> Optional[str]:
        """Find Claude CLI executable (async, non-blocking)."""
        if self._claude_path:
            return self._claude_path
        return await asyncio.to_thread(self._find_claude_sync)

    async def check_codex_auth(self) -> EngineAuth:
        """Check Codex authentication status (async, non-blocking)."""
        try:
            codex_path = await self.find_codex()
        except Exception as e:
            return EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error=f"Error finding Codex: {e}"
            )

        if not codex_path:
            return EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error="Codex CLI not found"
            )

        # Check for API key in environment (fast, no I/O)
        if os.environ.get("OPENAI_API_KEY"):
            return EngineAuth(
                engine="codex",
                status=AuthStatus.AUTHENTICATED,
                method=AuthMethod.API_KEY,
                username="api_key"
            )

        # Check browser auth via `codex login status`
        proc = None
        try:
            proc = await asyncio.create_subprocess_exec(
                codex_path, "login", "status",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self._pending_processes.append(proc)

            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)

            if proc.returncode == 0:
                output = stdout.decode("utf-8", errors="replace").strip()
                return EngineAuth(
                    engine="codex",
                    status=AuthStatus.AUTHENTICATED,
                    method=AuthMethod.BROWSER,
                    username=output if output else "browser"
                )
            else:
                return EngineAuth(
                    engine="codex",
                    status=AuthStatus.PENDING,
                    method=AuthMethod.NONE,
                    error="Not logged in"
                )
        except asyncio.TimeoutError:
            if proc and proc.returncode is None:
                try:
                    proc.kill()
                    await proc.wait()
                except ProcessLookupError:
                    pass
            return EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error="Auth check timed out"
            )
        except asyncio.CancelledError:
            if proc and proc.returncode is None:
                try:
                    proc.kill()
                    await proc.wait()
                except ProcessLookupError:
                    pass
            raise
        except Exception as e:
            return EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error=str(e)
            )
        finally:
            if proc in self._pending_processes:
                self._pending_processes.remove(proc)

    def _read_claude_credentials_sync(self) -> Optional[dict]:
        """Read Claude credentials file (synchronous helper)."""
        cred_file = Path.home() / ".claude" / ".credentials.json"
        try:
            if cred_file.exists():
                with open(cred_file) as f:
                    return json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
        return None

    async def check_claude_auth(self) -> EngineAuth:
        """Check Claude authentication status (async, non-blocking)."""
        try:
            claude_path = await self.find_claude()
        except Exception as e:
            return EngineAuth(
                engine="claude",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error=f"Error finding Claude: {e}"
            )

        if not claude_path:
            return EngineAuth(
                engine="claude",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error="Claude CLI not found"
            )

        # Check for API key in environment (fast, no I/O)
        if os.environ.get("ANTHROPIC_API_KEY"):
            return EngineAuth(
                engine="claude",
                status=AuthStatus.AUTHENTICATED,
                method=AuthMethod.API_KEY,
                username="api_key"
            )

        # Check for Claude credentials file (async file I/O)
        try:
            creds = await asyncio.to_thread(self._read_claude_credentials_sync)
            if creds:
                # Claude CLI uses claudeAiOauth.accessToken
                oauth = creds.get("claudeAiOauth", {})
                if oauth.get("accessToken"):
                    sub_type = oauth.get("subscriptionType", "authenticated")
                    return EngineAuth(
                        engine="claude",
                        status=AuthStatus.AUTHENTICATED,
                        method=AuthMethod.BROWSER,
                        username=sub_type
                    )
        except asyncio.CancelledError:
            raise
        except Exception:
            pass

        return EngineAuth(
            engine="claude",
            status=AuthStatus.PENDING,
            method=AuthMethod.NONE,
            error="Run 'claude' in terminal to authenticate"
        )

    async def check_all(self) -> AuthState:
        """Check authentication for both engines (async, non-blocking).

        This runs both auth checks in parallel for better performance.
        """
        try:
            codex_auth, claude_auth = await asyncio.gather(
                self.check_codex_auth(),
                self.check_claude_auth(),
                return_exceptions=False
            )
        except asyncio.CancelledError:
            raise
        except Exception as e:
            # If gather fails, return failed state for both
            codex_auth = EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error=str(e)
            )
            claude_auth = EngineAuth(
                engine="claude",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error=str(e)
            )

        self._state = AuthState(codex=codex_auth, claude=claude_auth)
        return self._state

    async def authenticate_codex_browser(self) -> Tuple[bool, str]:
        """Authenticate Codex via browser OAuth (async, non-blocking).

        Launches the Codex login process which opens a browser for OAuth.
        """
        try:
            codex_path = await self.find_codex()
        except Exception as e:
            return False, f"Error finding Codex: {e}"

        if not codex_path:
            return False, "Codex CLI not found"

        proc = None
        try:
            # Use device auth which is non-interactive after opening browser
            proc = await asyncio.create_subprocess_exec(
                codex_path, "login", "--device-auth",
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self._pending_processes.append(proc)

            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)

            if proc.returncode == 0:
                return True, "Codex authenticated successfully"
            else:
                error_msg = stderr.decode("utf-8", errors="replace").strip()
                stdout_msg = stdout.decode("utf-8", errors="replace").strip()
                return False, error_msg or stdout_msg or "Authentication failed"
        except asyncio.TimeoutError:
            if proc and proc.returncode is None:
                try:
                    proc.kill()
                    await proc.wait()
                except ProcessLookupError:
                    pass
            return False, "Authentication timed out after 2 minutes"
        except asyncio.CancelledError:
            if proc and proc.returncode is None:
                try:
                    proc.kill()
                    await proc.wait()
                except ProcessLookupError:
                    pass
            raise
        except Exception as e:
            return False, str(e)
        finally:
            if proc in self._pending_processes:
                self._pending_processes.remove(proc)

    async def authenticate_claude_browser(self) -> Tuple[bool, str]:
        """Check if Claude is authenticated or guide user (async, non-blocking).

        Claude CLI requires interactive terminal login, so this method
        guides the user rather than performing the authentication directly.
        """
        try:
            # First check if already authenticated
            auth_state = await self.check_claude_auth()
            if auth_state.status == AuthStatus.AUTHENTICATED:
                return True, "Claude is already authenticated!"

            # Claude CLI doesn't have a non-interactive login command
            # User needs to run `claude` in a terminal to authenticate
            return False, "Run 'claude' in a terminal to authenticate, then press R to retry"
        except asyncio.CancelledError:
            raise
        except Exception as e:
            return False, f"Error checking Claude auth: {e}"

    async def cancel_pending(self) -> None:
        """Cancel all pending authentication processes.

        Call this when the auth screen is being closed to clean up.
        """
        for proc in list(self._pending_processes):
            if proc.returncode is None:
                try:
                    proc.kill()
                    await proc.wait()
                except ProcessLookupError:
                    pass
                except Exception:
                    pass
        self._pending_processes.clear()

    @property
    def state(self) -> Optional[AuthState]:
        """Get current auth state (cached from last check_all call)."""
        return self._state

    @property
    def codex_path(self) -> Optional[str]:
        """Get cached Codex executable path.

        Returns the cached path if available. Use find_codex() for fresh lookup.
        """
        return self._codex_path

    @property
    def claude_path(self) -> Optional[str]:
        """Get cached Claude executable path.

        Returns the cached path if available. Use find_claude() for fresh lookup.
        """
        return self._claude_path
