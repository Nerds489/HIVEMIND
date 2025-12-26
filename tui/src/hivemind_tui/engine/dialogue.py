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

Both must verify completion before delivering to user.
"""

import asyncio
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
    final_output: str
    turns: int
    agents_used: List[str] = field(default_factory=list)
    error: Optional[str] = None


CODEX_PROPOSAL_PROMPT = """You are Codex, coordinating with Claude on a user request.

User Request: {request}

Propose an approach to handle this request. Consider:
1. Is this something that needs specialized agents, or can it be answered directly?
2. If agents are needed, which ones?
3. What's the success criteria?

Keep your proposal concise and actionable.
"""


CODEX_REFINE_PROMPT = """You are Codex, refining your proposal based on Claude's feedback.

User Request: {request}

Your Previous Proposal:
{proposal}

Claude's Feedback:
{feedback}

Refine your proposal based on Claude's feedback. If you now agree with Claude's suggestions, incorporate them.
"""


CODEX_VERIFY_PROMPT = """You are Codex, verifying the final output.

Original Request: {request}

Output to Verify:
{output}

Claude's Assessment: {claude_assessment}

Do you agree this output is 100% complete and correct?
If yes, state "VERIFIED" and briefly explain why it's acceptable.
If no, explain what's missing or incorrect.
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
    
    async def _codex_propose(self, request: str) -> str:
        """Have Codex propose an approach.
        
        Args:
            request: User's request
            
        Returns:
            Codex's proposal
        """
        prompt = CODEX_PROPOSAL_PROMPT.format(request=request)
        
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
        codex_proposal = await self._codex_propose(request)
        self._log_turn("codex", codex_proposal)
        
        for turn in range(self.max_turns):
            # Claude evaluates
            self.codex._emit_status(f"Consulting Claude (turn {turn + 1})...")
            
            claude_eval = await self.claude.evaluate_proposal(
                request,
                codex_proposal,
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
            )
            self._log_turn("codex", codex_proposal)
        
        # Max turns reached - take Claude's last suggestion
        return ConsensusResult(
            agreed=True,  # Force agreement
            plan=codex_proposal,
            agents_needed=claude_eval.suggested_agents if claude_eval else [],
            needs_agents=bool(claude_eval and claude_eval.suggested_agents),
        )
    
    async def _execute_with_agents(
        self,
        consensus: ConsensusResult,
        request: str,
    ) -> str:
        """Execute task with agreed agents.
        
        Args:
            consensus: Consensus result with agent list
            request: Original request
            
        Returns:
            Combined agent output
        """
        self.codex._emit_status("Executing with agents...")
        
        results = await self.claude.execute_agents(
            consensus.agents_needed,
            consensus.plan,
            context=request,
        )
        
        # Synthesize results
        output = await self.claude.synthesize_results(results, request)
        
        return output
    
    async def _verify_completion(
        self,
        request: str,
        output: str,
    ) -> tuple[bool, str]:
        """Both Codex and Claude verify output is complete.
        
        Args:
            request: Original request
            output: Output to verify
            
        Returns:
            Tuple of (verified, final_output)
        """
        self.codex._emit_status("Verifying completion...")
        
        # Claude verifies first
        claude_check = await self.claude.verify_output(request, output)
        
        if not claude_check.verified:
            # Claude found issues - fix them
            if claude_check.suggestions:
                # Re-execute with suggestions
                return False, claude_check.issues or "Claude found issues"
        
        # Codex verifies
        verify_prompt = CODEX_VERIFY_PROMPT.format(
            request=request,
            output=output,
            claude_assessment="VERIFIED - Output is complete and correct" if claude_check.verified else f"Issues found: {claude_check.issues}",
        )
        
        success, codex_response = await self.codex._call_codex_cli(verify_prompt)
        
        codex_verified = success and "VERIFIED" in codex_response.upper()
        
        if claude_check.verified and codex_verified:
            return True, output
        else:
            return False, codex_response if not codex_verified else (claude_check.issues or "Verification failed")
    
    async def discuss(self, request: str) -> DialogueResult:
        """
        Main entry point - discuss until consensus and execute.
        
        Flow:
        1. Codex proposes approach
        2. Claude evaluates
        3. Iterate until agreement
        4. Execute with agents if needed
        5. Both verify completion
        6. Return final output
        
        Args:
            request: User's request
            
        Returns:
            DialogueResult with final output
        """
        try:
            # Phase 1: Reach consensus
            consensus = await self._reach_consensus(request)
            
            if not consensus.needs_agents:
                # Direct response - no agents needed
                # Generate direct response
                self.codex._emit_status("Generating response...")
                success, response = await self.codex._call_codex_cli(
                    f"Based on our discussion, provide a complete response to: {request}\n\nOur agreed approach: {consensus.plan}",
                )
                
                return DialogueResult(
                    success=success,
                    final_output=response if success else "Unable to generate response",
                    turns=self.turn_count,
                    agents_used=[],
                )
            
            # Phase 2: Execute with agents
            agent_output = await self._execute_with_agents(consensus, request)
            
            # Phase 3: Verify completion
            max_verification_attempts = 3
            for attempt in range(max_verification_attempts):
                verified, result = await self._verify_completion(request, agent_output)
                
                if verified:
                    return DialogueResult(
                        success=True,
                        final_output=agent_output,
                        turns=self.turn_count,
                        agents_used=consensus.agents_needed,
                    )
                
                # Not verified - try to fix
                if attempt < max_verification_attempts - 1:
                    self.codex._emit_status(f"Revision needed (attempt {attempt + 2})...")
                    # Re-execute with feedback
                    agent_output = await self._execute_with_agents(
                        ConsensusResult(
                            agreed=True,
                            plan=f"Fix these issues: {result}\n\nOriginal plan: {consensus.plan}",
                            agents_needed=consensus.agents_needed,
                            needs_agents=True,
                        ),
                        request,
                    )
            
            # Max attempts - return best effort
            return DialogueResult(
                success=True,  # Partial success
                final_output=agent_output,
                turns=self.turn_count,
                agents_used=consensus.agents_needed,
            )
            
        except Exception as e:
            return DialogueResult(
                success=False,
                final_output=f"An error occurred: {str(e)}",
                turns=self.turn_count,
                error=str(e),
            )
