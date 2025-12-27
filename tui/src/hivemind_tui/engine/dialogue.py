# DESTINATION: tui/src/hivemind_tui/engine/dialogue.py
# CREATE THIS FILE AT THE EXACT PATH ABOVE
# DO NOT MODIFY THIS CODE

"""
HIVEMIND Dialogue System - Codex-Claude conversation for consensus.

Manages multi-turn dialogue between Codex and Claude until both agree on:
- What needs to be done
- How it should be done
- Which agents to involve
- Success criteria
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .codex_head import CodexHead
    from .claude_agent import ClaudeAgent


@dataclass
class DialogueTurn:
    """A single turn in the dialogue."""
    speaker: str  # "codex" or "claude"
    content: str
    turn_number: int


@dataclass
class ConsensusResult:
    """Result of reaching consensus."""
    agreed: bool
    plan: str
    agents_needed: List[str] = field(default_factory=list)
    needs_agents: bool = False
    response: Optional[str] = None  # For direct response (no agents)


@dataclass
class DialogueResult:
    """Final result of the dialogue."""
    success: bool
    plan: str
    turns: int
    agents_used: List[str] = field(default_factory=list)
    error: Optional[str] = None


CODEX_PROPOSAL_PROMPT = """You are Codex, coordinating with Claude on a user request.

User Request: {request}
{live_notes}

Propose an approach to handle this request. Consider:
1. Is this something that needs specialized agents, or can it be answered directly?
2. If agents are needed, which ones?
3. What's the success criteria?

Keep your proposal concise and actionable.
"""


CODEX_REFINE_PROMPT = """You are Codex, refining your proposal based on Claude's feedback.

User Request: {request}
{live_notes}

Your Previous Proposal:
{proposal}

Claude's Feedback:
{feedback}

Refine your proposal based on Claude's feedback. If you now agree with Claude's suggestions, incorporate them.
"""




class CodexClaudeDialogue:
    """Manages Codex-Claude dialogue until consensus."""
    
    def __init__(
        self,
        codex: "CodexHead",
        claude: "ClaudeAgent",
        max_turns: int = 10,
    ):
        """Initialize dialogue.
        
        Args:
            codex: CodexHead instance
            claude: ClaudeAgent instance
            max_turns: Maximum dialogue turns before forcing decision
        """
        self.codex = codex
        self.claude = claude
        self.max_turns = max_turns
        self.history: List[DialogueTurn] = []
        self.turn_count = 0
    
    def _log_turn(self, speaker: str, content: str) -> None:
        """Log a dialogue turn."""
        self.turn_count += 1
        self.history.append(DialogueTurn(
            speaker=speaker,
            content=content,
            turn_number=self.turn_count,
        ))
    
    def _get_history_for_context(self) -> List[Dict]:
        """Get history formatted for context."""
        return [
            {"speaker": t.speaker, "content": t.content}
            for t in self.history
        ]
    
    async def _codex_propose(self, request: str, live_notes: str) -> str:
        """Have Codex propose an approach.
        
        Args:
            request: User's request
            
        Returns:
            Codex's proposal
        """
        prompt = CODEX_PROPOSAL_PROMPT.format(
            request=request,
            live_notes=live_notes,
        )
        
        success, response = await self.codex._call_codex_cli(prompt)
        
        if success:
            return response
        else:
            return f"I'll work with Claude to determine the best approach for: {request}"
    
    async def _codex_refine(
        self,
        request: str,
        proposal: str,
        feedback: str,
        live_notes: str,
    ) -> str:
        """Have Codex refine proposal based on feedback.
        
        Args:
            request: Original request
            proposal: Previous proposal
            feedback: Claude's feedback
            
        Returns:
            Refined proposal
        """
        prompt = CODEX_REFINE_PROMPT.format(
            request=request,
            proposal=proposal,
            feedback=feedback,
            live_notes=live_notes,
        )
        
        success, response = await self.codex._call_codex_cli(prompt)
        
        if success:
            return response
        else:
            return f"Incorporating Claude's feedback: {feedback[:200]}..."
    
    async def _reach_consensus(self, request: str) -> ConsensusResult:
        """Dialogue until Codex and Claude agree.
        
        Args:
            request: User's request
            
        Returns:
            ConsensusResult with agreed plan
        """
        # Codex proposes initial approach
        self.codex._emit_status("Planning approach...")
        live_inputs = self.codex._consume_live_inputs()
        live_notes = self.codex._format_live_inputs(live_inputs)
        live_block = f"\nLive User Input:\n{live_notes}\n" if live_notes else ""
        codex_proposal = await self._codex_propose(request, live_block)
        self._log_turn("codex", codex_proposal)
        
        turn = 0
        while True:
            if self.max_turns and turn >= self.max_turns:
                return ConsensusResult(
                    agreed=False,
                    plan=codex_proposal,
                    agents_needed=claude_eval.suggested_agents if claude_eval else [],
                    needs_agents=bool(claude_eval and claude_eval.suggested_agents),
                    response=claude_eval.feedback if claude_eval else "Consensus not reached",
                )

            # Claude evaluates
            self.codex._emit_status(f"Consulting Claude (turn {turn + 1})...")
            
            new_inputs = self.codex._consume_live_inputs()
            new_notes = self.codex._format_live_inputs(new_inputs)
            live_block = f"\nLive User Input:\n{new_notes}\n" if new_notes else ""
            proposal_for_claude = codex_proposal
            if new_notes:
                proposal_for_claude = (
                    f"{codex_proposal}\n\nLive User Input:\n{new_notes}"
                )
            claude_eval = await self.claude.evaluate_proposal(
                request,
                proposal_for_claude,
                self._get_history_for_context(),
            )
            self._log_turn("claude", claude_eval.feedback)
            
            if claude_eval.agrees:
                # Consensus reached
                return ConsensusResult(
                    agreed=True,
                    plan=codex_proposal,
                    agents_needed=claude_eval.suggested_agents,
                    needs_agents=len(claude_eval.suggested_agents) > 0,
                )
            
            # Codex refines based on feedback
            self.codex._emit_status("Refining approach...")
            codex_proposal = await self._codex_refine(
                request,
                codex_proposal,
                claude_eval.feedback,
                live_block,
            )
            self._log_turn("codex", codex_proposal)
            turn += 1
    
    async def discuss(self, request: str) -> DialogueResult:
        """
        Main entry point - discuss until consensus and execute.
        
        Flow:
        1. Codex proposes approach
        2. Claude evaluates
        3. Iterate until agreement
        4. Return agreed plan and agents
        
        Args:
            request: User's request
            
        Returns:
            DialogueResult with agreed plan
        """
        try:
            # Phase 1: Reach consensus
            consensus = await self._reach_consensus(request)
            return DialogueResult(
                success=consensus.agreed,
                plan=consensus.plan,
                turns=self.turn_count,
                agents_used=consensus.agents_needed,
            )
        except Exception as e:
            return DialogueResult(
                success=False,
                plan=request,
                turns=self.turn_count,
                error=str(e),
            )
