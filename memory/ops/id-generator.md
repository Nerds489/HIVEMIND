# Memory ID Generation

## Format

```
mem_[12 random alphanumeric characters]
```

## Character Set

- Lowercase letters: a-z (26 characters)
- Digits: 0-9 (10 characters)
- Total: 36 characters
- Combinations: 36^12 = 4.7 × 10^18 (effectively infinite)

## Generation Algorithm

```
1. Generate 12 random characters from [a-z0-9]
2. Prefix with "mem_"
3. Check uniqueness:
   - Scan all _index.json files in memory/
   - Check entries[].id for collision
4. If collision detected:
   - Log collision (rare event)
   - Regenerate new ID
   - Repeat check
5. Return unique ID
```

## Examples

```
mem_a7b3c9d2e4f1
mem_x9y2z8w5v3u1
mem_k4m7n1p8q2r5
```

## Reserved IDs

These IDs are reserved for system use:

| ID | Purpose |
|----|---------|
| `mem_userprofile0` | User profile |
| `mem_systemconfig` | System configuration |
| `mem_learnpattern` | Learned patterns |
| `mem_terminology` | Terminology glossary |

## Uniqueness Scope

IDs must be unique across:
- All global memories
- All team memories
- All agent memories
- All project memories
- All session memories
- All archived memories

## Collision Handling

Expected collision rate: ~0% (4.7 quintillion combinations)

If collision occurs:
1. Generate new ID
2. Log: `WARN: ID collision detected, regenerating`
3. Maximum 3 retries
4. If still colliding after 3 retries: `ERROR: ID generation failure`
