# HIVEMIND BOOTSTRAP

## ACTIVATION
Trigger: "HIVEMIND" or "hivemind" in any message  
Deactivate: "stop hivemind" or "disable hivemind" or "hivemind off"

## ON ACTIVATION, LOAD IN ORDER
1. `CLAUDE.md` → Core rules (must obey)
2. `runtime/VOICE-RULES.md` → Output constraints
3. `runtime/OUTPUT-FILTER.md` + `runtime/FILTER.md` → What never to show
4. `runtime/PROJECT-DETECTOR.md` → Scan environment
5. `memory/long-term/preferences.json` → User prefs
6. `memory/long-term/project.json` → Project context
7. `memory/long-term/user-profile.json` → User model

## ON EVERY TASK
1. `runtime/PREFLIGHT.md` → Pre-checks
2. `config/routing.json` → Route to expertise
3. Execute with loaded context
4. `protocols/QUALITY-GATES.md` → Validate output
5. `runtime/POSTTASK.md` → Learn and store

## DIRECTORIES
- `agents/` → specialist definitions (role playbooks + registry)
- `teams/` → team configurations and playbooks
- `workflows/` → process playbooks
- `templates/` → output formats
- `protocols/` → safety rules
- `memory/` → persistent storage
- `config/` → system configuration

## COMMANDS
/hivemind → Confirm active  
/status → Current project context (brief)  
/remember [X] → Store to long-term memory  
/forget [X] → Remove from memory  
/learn → Show recent learnings  
/improve [feedback] → Direct improvement input

