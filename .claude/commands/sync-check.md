---
description: Sanity check that `.claude/commands/` references exist under `.claude/skills/` (scripts, JSON, data files). Run after moving paths or adding new commands.
---

# Sync check: `.claude/commands` vs `.claude/skills`

Use this command to verify that workflow instructions and on-disk assets stay aligned now that **all runnable assets live under** `.claude/skills/`.

## What to verify

1. **List** every `.claude/commands/*.md` file (except this file if you prefer).
2. **Extract path-like strings** that start with `.claude/skills/` (search `.claude/commands` for that prefix, or use a small script, or read each command and note paths).
3. For each unique path:
   - If it ends in `.py`, `.sh`, `.json`, `.md`, `.yaml`, `.yml`, or is a directory reference, confirm that path **exists** in the tree.
   - Skip variable placeholders such as `workspaces/<YYYY-MM-DD>/...`.

## Report format

```markdown
## Sync check report

### Missing references
- (none) or list of `.claude/skills/...` paths referenced by commands but not on disk

### Commands with no skill paths
- List commands that only reference other commands (expected for pure orchestration)

### Orphan asset folders (optional)
- Folders under `.claude/skills/` with no references from any command (informational only)
```

## Notes

- **Secrets**: `.claude/skills/ticktick-sync/.env` is gitignored; `env.example` should exist.
- **User-maintained data**: `user-mapping.md` may be gitignored; still confirm the directory exists.
- **Batch workflow**: `.claude/skills/batch-meeting-plan/SKILL.md` is intentionally kept as the long-form batch spec; `/batch-meeting-plan` points here.
