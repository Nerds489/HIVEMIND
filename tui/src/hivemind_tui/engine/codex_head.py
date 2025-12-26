# DESTINATION: tui/src/hivemind_tui/engine/codex_head.py
# CREATE THIS FILE AT THE EXACT PATH ABOVE
# DO NOT MODIFY THIS CODE

"""
HIVEMIND Codex Head - The primary AI interface.

Codex IS the AI assistant. Users talk to Codex.
Codex decides when to involve Claude.
Codex presents all responses to the user.
"""

import asyncio
import json
import os
import re
import signal
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .auth import AuthManager
    from .dialogue import CodexClaudeDialogue


class ResponseSource(str, Enum):
    """Source of the response."""
    CODEX_DIRECT = "codex_direct"  # Codex answered alone
    CODEX_CLAUDE = "codex_claude"  # Codex consulted Claude
    AGENTS = "agents"              # Agents were involved


@dataclass
class CodexResponse:
    """Response from Codex."""
    content: str
    source: ResponseSource
    success: bool = True
    error: Optional[str] = None
    agents_used: List[str] = field(default_factory=list)
    dialogue_turns: int = 0


# Patterns Codex handles ALONE (no Claude needed)
DIRECT_PATTERNS = {
    "greetings": [
        r"^hi$", r"^hello$", r"^hey$", r"^hi!$", r"^hello!$", r"^hey!$",
        r"^good morning", r"^good afternoon", r"^good evening",
        r"^howdy", r"^yo$", r"^sup$", r"^greetings",
    ],
    "farewells": [
        r"^bye$", r"^goodbye$", r"^see you", r"^later$", r"^cya$",
        r"^goodnight", r"^night$",
    ],
    "acknowledgments": [
        r"^ok$", r"^okay$", r"^sure$", r"^yes$", r"^no$", r"^yep$", r"^nope$",
        r"^thanks", r"^thank you", r"^thx$", r"^ty$",
        r"^got it", r"^understood", r"^i see", r"^makes sense",
        r"^cool$", r"^nice$", r"^great$", r"^awesome$", r"^perfect$",
    ],
    "identity": [
        r"who are you", r"what are you", r"tell me about yourself",
        r"what is hivemind", r"what's hivemind", r"what can you do",
        r"how do you work", r"introduce yourself",
    ],
    "meta": [
        r"^help$", r"^help me$", r"what commands", r"how to use",
        r"^status$", r"^version$",
    ],
    "simple_questions": [
        r"^what time", r"^what date", r"^what day",
        r"^how are you", r"^how's it going", r"how are things",
    ],
    "conversation": [
        r"^really\??$", r"^interesting", r"^i think", r"^i believe",
        r"^that's", r"^what do you think", r"^do you think",
        r"^can you explain", r"^what does .* mean",
    ],
}

# Patterns that REQUIRE Claude consultation
CLAUDE_PATTERNS = {
    "work_requests": [
        r"build", r"create", r"implement", r"develop", r"make me",
        r"write .* code", r"write .* script", r"write .* program",
        r"design", r"architect", r"structure",
    ],
    "code_tasks": [
        r"fix .* bug", r"debug", r"refactor", r"optimize",
        r"add .* feature", r"update .* code", r"modify .* function",
        r"review .* code", r"code review",
    ],
    "security_tasks": [
        r"pentest", r"penetration test", r"security audit",
        r"vulnerability", r"exploit", r"security scan",
        r"threat model", r"security review",
    ],
    "infrastructure_tasks": [
        r"deploy", r"configure", r"set up .* server",
        r"kubernetes", r"docker", r"terraform", r"ansible",
        r"ci.?cd", r"pipeline",
    ],
    "qa_tasks": [
        r"test", r"write .* tests", r"test coverage",
        r"performance test", r"load test", r"stress test",
        r"quality assurance",
    ],
    "analysis_tasks": [
        r"analyze", r"review", r"assess", r"evaluate",
        r"audit", r"investigate", r"examine",
    ],
}


CODEX_SYSTEM_PROMPT = """You are HIVEMIND's Codex, the primary AI assistant.

You are talking DIRECTLY to the user. You ARE the AI, not a router.

For this specific message, provide a direct, helpful response.
Be conversational, friendly, and concise.

If this is a greeting, respond warmly.
If this is a question, answer it directly.
If this is feedback, acknowledge it appropriately.

DO NOT mention agents, routing, or internal systems.
DO NOT say you need to "route" or "delegate" anything.
Just respond naturally as a helpful AI assistant.
"""


CODEX_IDENTITY_RESPONSE = """I'm HIVEMIND's Codex - your AI assistant.

I handle conversations directly, and when you have complex technical work, I collaborate with Claude and our specialized agent teams to get things done.

**What I can help with:**
- General questions and conversations
- Technical explanations and advice
- Code writing, review, and debugging
- System design and architecture
- Security assessments
- Infrastructure and deployment
- Testing and quality assurance

Just tell me what you need - for simple things I'll help directly, for complex work I'll coordinate with the right specialists.

What can I help you with?"""


class CodexHead:
    """
    Codex is THE AI assistant. Users talk to Codex.
    Codex decides when to involve Claude.
    """
    
    def __init__(
        self,
        auth_manager: "AuthManager",
        working_dir: Optional[Path] = None,
        on_status: Optional[Callable[[str], None]] = None,
    ):
        """Initialize Codex Head.
        
        Args:
            auth_manager: Authentication manager
            working_dir: Working directory for operations
            on_status: Callback for status updates
        """
        self.auth = auth_manager
        self.working_dir = working_dir or Path.cwd()
        self.on_status = on_status
        self._conversation_history: List[dict] = []
        self._dialogue: Optional["CodexClaudeDialogue"] = None
    
    def _emit_status(self, message: str) -> None:
        """Emit status update."""
        if self.on_status:
            self.on_status(message)
    
    def _matches_pattern(self, text: str, patterns: List[str]) -> bool:
        """Check if text matches any pattern."""
        lower_text = text.lower().strip()
        for pattern in patterns:
            if re.search(pattern, lower_text, re.IGNORECASE):
                return True
        return False
    
    def _can_handle_alone(self, user_input: str) -> bool:
        """
        Determine if Codex can answer without Claude.
        
        Returns True for:
        - Greetings
        - Acknowledgments
        - Identity questions
        - Simple questions
        - General conversation
        
        Returns False for:
        - Work requests
        - Code tasks
        - Security tasks
        - Infrastructure tasks
        - QA tasks
        - Complex analysis
        """
        lower_input = user_input.lower().strip()
        
        # Check if it matches any CLAUDE pattern (needs Claude)
        for category, patterns in CLAUDE_PATTERNS.items():
            if self._matches_pattern(lower_input, patterns):
                return False
        
        # Check if it matches any DIRECT pattern (Codex alone)
        for category, patterns in DIRECT_PATTERNS.items():
            if self._matches_pattern(lower_input, patterns):
                return True
        
        # Short inputs (< 20 chars) that don't match Claude patterns
        # are likely conversational
        if len(lower_input) < 20:
            return True
        
        # Questions that start with common question words
        # but don't match work patterns are likely simple questions
        simple_question_starters = [
            "what is", "what's", "who is", "who's", "when is", "when's",
            "where is", "where's", "why is", "why's", "how is", "how's",
            "can you explain", "could you tell me",
        ]
        for starter in simple_question_starters:
            if lower_input.startswith(starter):
                # But check it's not a work question
                work_indicators = [
                    "code", "script", "program", "function", "class",
                    "bug", "error", "deploy", "server", "database",
                ]
                if not any(w in lower_input for w in work_indicators):
                    return True
        
        # Default: if uncertain, involve Claude for better response
        return False
    
    def _is_identity_question(self, user_input: str) -> bool:
        """Check if this is an identity question."""
        return self._matches_pattern(user_input, DIRECT_PATTERNS["identity"])
    
    async def _call_codex_cli(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        timeout: float = 60.0,
    ) -> tuple[bool, str]:
        """Call Codex CLI for response generation.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (success, response_or_error)
        """
        codex_path = self.auth.codex_path
        if not codex_path:
            return False, "Codex CLI not available"
        
        # Build the full prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        else:
            full_prompt = prompt
        
        # Create temp file for output
        output_file = tempfile.mktemp(suffix=".txt")
        
        cmd = [
            codex_path, "exec",
            "--full-auto",
            "--skip-git-repo-check",
            "-o", output_file,
            full_prompt
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.working_dir),
                start_new_session=True,
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
                # Read from output file
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
                    return False, "No response from Codex"
                return True, response
            else:
                try:
                    if os.path.exists(output_file):
                        os.remove(output_file)
                except Exception:
                    pass
                error = stderr.decode("utf-8", errors="replace").strip()
                return False, f"Codex error: {error or 'Unknown error'}"
                
        except Exception as e:
            try:
                if os.path.exists(output_file):
                    os.remove(output_file)
            except Exception:
                pass
            return False, f"Failed to call Codex: {str(e)}"
    
    async def _respond_directly(self, user_input: str) -> CodexResponse:
        """Generate direct response without Claude.
        
        Args:
            user_input: User's input
            
        Returns:
            CodexResponse with direct answer
        """
        # Handle identity questions with canned response
        if self._is_identity_question(user_input):
            return CodexResponse(
                content=CODEX_IDENTITY_RESPONSE,
                source=ResponseSource.CODEX_DIRECT,
                success=True,
            )
        
        # Use Codex CLI for other direct responses
        self._emit_status("Thinking...")
        success, response = await self._call_codex_cli(
            user_input,
            system_prompt=CODEX_SYSTEM_PROMPT,
        )
        
        if success:
            return CodexResponse(
                content=response,
                source=ResponseSource.CODEX_DIRECT,
                success=True,
            )
        else:
            return CodexResponse(
                content="I'm having trouble responding right now. Could you try again?",
                source=ResponseSource.CODEX_DIRECT,
                success=False,
                error=response,
            )
    
    async def _consult_claude(self, user_input: str) -> CodexResponse:
        """Consult Claude for complex tasks.
        
        Args:
            user_input: User's input
            
        Returns:
            CodexResponse with result from Claude consultation
        """
        # Import here to avoid circular imports
        from .dialogue import CodexClaudeDialogue
        from .claude_agent import ClaudeAgent
        
        self._emit_status("Consulting with Claude...")
        
        # Create Claude agent if needed
        claude_agent = ClaudeAgent(self.auth, self.working_dir)
        
        # Create dialogue
        dialogue = CodexClaudeDialogue(self, claude_agent)
        
        # Discuss until consensus
        result = await dialogue.discuss(user_input)
        
        return CodexResponse(
            content=result.final_output,
            source=ResponseSource.CODEX_CLAUDE if not result.agents_used else ResponseSource.AGENTS,
            success=result.success,
            error=result.error,
            agents_used=result.agents_used,
            dialogue_turns=result.turns,
        )
    
    async def process(self, user_input: str) -> CodexResponse:
        """
        Process user input - main entry point.
        
        Codex receives ALL user input and decides how to handle it.
        
        Args:
            user_input: User's input text
            
        Returns:
            CodexResponse with the response
        """
        # Add to conversation history
        self._conversation_history.append({
            "role": "user",
            "content": user_input,
        })
        
        # Can Codex handle this alone?
        if self._can_handle_alone(user_input):
            response = await self._respond_directly(user_input)
        else:
            # Need Claude's expertise
            response = await self._consult_claude(user_input)
        
        # Add response to history
        self._conversation_history.append({
            "role": "assistant",
            "content": response.content,
        })
        
        return response
    
    def get_conversation_context(self, max_turns: int = 10) -> str:
        """Get recent conversation context.
        
        Args:
            max_turns: Maximum number of turns to include
            
        Returns:
            Formatted conversation context
        """
        recent = self._conversation_history[-max_turns * 2:]
        context_parts = []
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Codex"
            context_parts.append(f"{role}: {msg['content']}")
        return "\n".join(context_parts)
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self._conversation_history = []
