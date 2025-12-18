# HIVEMIND TRIGGER FOR CODEX

This file documents the expected trigger behavior for Codex sessions operating inside `HIVEMIND/`.

## On Any Mention of "HIVEMIND" (Case-Insensitive)

1. Read `CODEX-INSTRUCTIONS.md` and `CLAUDE.md`
2. Load memory from `memory/long-term/` (and any other relevant memory under `memory/` per `memory/TRIGGERS.md`)
3. Activate HIVEMIND mode
4. Respond exactly: `HIVEMIND active.`
5. Process subsequent requests with silent orchestration rules

## On "stop HIVEMIND" / "disable HIVEMIND" / "HIVEMIND off" (Case-Insensitive)

1. Deactivate HIVEMIND mode
2. Respond exactly: `HIVEMIND deactivated.`
3. Return to normal operation

