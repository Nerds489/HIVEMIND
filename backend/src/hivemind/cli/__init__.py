"""
HIVEMIND CLI Module

Command-line interface for HIVEMIND backend operations.
Includes subprocess wrappers for claude and codex CLI tools.
"""

from hivemind.cli.claude import ClaudeCLI
from hivemind.cli.codex import CodexCLI
from hivemind.cli.main import app
from hivemind.cli.manager import CLIManager, CLIOutput, OutputType

__all__ = [
    "app",
    "ClaudeCLI",
    "CodexCLI",
    "CLIManager",
    "CLIOutput",
    "OutputType",
]
