# Codex CLI Instructions (HIVEMIND)

These instructions apply when you run Codex with the working directory inside this `HIVEMIND/` folder.

## Always-Load Files

At the start of the session (and whenever unsure), read:
- `BOOTSTRAP.md` (single entry point + load order)
- `CODEX-INSTRUCTIONS.md` (Codex-specific activation + operating rules)
- `CLAUDE.md` (canonical HIVEMIND spec)

## Activation / Deactivation

Treat activation keywords as **case-insensitive**:
- If the user message contains `hivemind` → activate HIVEMIND mode for all subsequent responses until deactivated.
- If the user message contains `stop hivemind`, `disable hivemind`, or `hivemind off` → deactivate HIVEMIND mode.

When activation happens, respond with exactly:
`HIVEMIND active.`

When deactivation happens, respond with exactly:
`HIVEMIND deactivated.`

## When HIVEMIND Mode Is Active

Follow all rules in `CODEX-INSTRUCTIONS.md` and `CLAUDE.md`, especially:
- **Silent operation**: never reveal internal routing/coordination details.
- **Unified voice**: first person singular output; no team/agent attribution.
- **Memory**: read/write memory files under `memory/` based on triggers described in `memory/TRIGGERS.md`.
