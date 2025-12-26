# DESTINATION: tui/src/hivemind_tui/engine/auth.py
# CREATE THIS FILE AT THE EXACT PATH ABOVE
# DO NOT MODIFY THIS CODE

"""
HIVEMIND Authentication Module.

Handles browser OAuth (primary) and API key fallback for both Codex and Claude.
"""

import asyncio
import json
import os
import shutil
import subprocess
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
    """Manages authentication for Codex and Claude."""
    
    def __init__(self):
        self._codex_path: Optional[str] = None
        self._claude_path: Optional[str] = None
        self._state: Optional[AuthState] = None
        self._config_dir = Path.home() / ".config" / "hivemind"
        self._config_dir.mkdir(parents=True, exist_ok=True)
    
    def find_codex(self) -> Optional[str]:
        """Find Codex CLI executable."""
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
        if nvm_dir.exists():
            for version_dir in sorted(nvm_dir.iterdir(), reverse=True):
                candidate = version_dir / "bin" / "codex"
                if candidate.exists():
                    candidates.insert(0, candidate)
                    break
        
        for path in candidates:
            if path.exists() and os.access(path, os.X_OK):
                self._codex_path = str(path)
                return self._codex_path
        
        return None
    
    def find_claude(self) -> Optional[str]:
        """Find Claude CLI executable."""
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
            if path.exists() and os.access(path, os.X_OK):
                self._claude_path = str(path)
                return self._claude_path
        
        return None
    
    async def check_codex_auth(self) -> EngineAuth:
        """Check Codex authentication status."""
        codex_path = self.find_codex()
        
        if not codex_path:
            return EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error="Codex CLI not found. Install with: npm install -g @openai/codex"
            )
        
        # Check for API key in environment
        if os.environ.get("OPENAI_API_KEY"):
            return EngineAuth(
                engine="codex",
                status=AuthStatus.AUTHENTICATED,
                method=AuthMethod.API_KEY,
                username="api_key_user"
            )
        
        # Check browser auth via `codex login status`
        try:
            proc = await asyncio.create_subprocess_exec(
                codex_path, "login", "status",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
            
            if proc.returncode == 0:
                return EngineAuth(
                    engine="codex",
                    status=AuthStatus.AUTHENTICATED,
                    method=AuthMethod.BROWSER,
                    username="browser_user"
                )
            else:
                return EngineAuth(
                    engine="codex",
                    status=AuthStatus.PENDING,
                    method=AuthMethod.NONE,
                    error="Not logged in"
                )
        except asyncio.TimeoutError:
            return EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error="Auth check timed out"
            )
        except Exception as e:
            return EngineAuth(
                engine="codex",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error=str(e)
            )
    
    async def check_claude_auth(self) -> EngineAuth:
        """Check Claude authentication status."""
        claude_path = self.find_claude()
        
        if not claude_path:
            return EngineAuth(
                engine="claude",
                status=AuthStatus.FAILED,
                method=AuthMethod.NONE,
                error="Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"
            )
        
        # Check for API key in environment
        if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY"):
            return EngineAuth(
                engine="claude",
                status=AuthStatus.AUTHENTICATED,
                method=AuthMethod.API_KEY,
                username="api_key_user"
            )
        
        # Check for credentials file
        cred_file = Path.home() / ".claude" / ".credentials.json"
        if cred_file.exists():
            try:
                with open(cred_file) as f:
                    creds = json.load(f)
                if creds.get("token") or creds.get("access_token"):
                    return EngineAuth(
                        engine="claude",
                        status=AuthStatus.AUTHENTICATED,
                        method=AuthMethod.BROWSER,
                        username=creds.get("email", "browser_user")
                    )
            except Exception:
                pass
        
        return EngineAuth(
            engine="claude",
            status=AuthStatus.PENDING,
            method=AuthMethod.NONE,
            error="Not logged in"
        )
    
    async def check_all(self) -> AuthState:
        """Check authentication for both engines."""
        codex_auth, claude_auth = await asyncio.gather(
            self.check_codex_auth(),
            self.check_claude_auth()
        )
        
        self._state = AuthState(codex=codex_auth, claude=claude_auth)
        return self._state
    
    async def authenticate_codex_browser(self) -> Tuple[bool, str]:
        """Authenticate Codex via browser OAuth."""
        codex_path = self.find_codex()
        if not codex_path:
            return False, "Codex CLI not found"
        
        try:
            proc = await asyncio.create_subprocess_exec(
                codex_path, "login", "--device-auth",
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            
            if proc.returncode == 0:
                return True, "Codex authenticated successfully"
            else:
                return False, stderr.decode("utf-8", errors="replace")
        except asyncio.TimeoutError:
            return False, "Authentication timed out"
        except Exception as e:
            return False, str(e)
    
    async def authenticate_claude_browser(self) -> Tuple[bool, str]:
        """Authenticate Claude via browser OAuth."""
        claude_path = self.find_claude()
        if not claude_path:
            return False, "Claude CLI not found"
        
        try:
            proc = await asyncio.create_subprocess_exec(
                claude_path, "login",
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            
            if proc.returncode == 0:
                return True, "Claude authenticated successfully"
            else:
                return False, stderr.decode("utf-8", errors="replace")
        except asyncio.TimeoutError:
            return False, "Authentication timed out"
        except Exception as e:
            return False, str(e)
    
    @property
    def state(self) -> Optional[AuthState]:
        """Get current auth state."""
        return self._state
    
    @property
    def codex_path(self) -> Optional[str]:
        """Get Codex executable path."""
        return self._codex_path or self.find_codex()
    
    @property
    def claude_path(self) -> Optional[str]:
        """Get Claude executable path."""
        return self._claude_path or self.find_claude()
