---
name: sync-check
description: Sanity check that paths referenced from SKILL files under .claude/skills exist (scripts, JSON, data, other SKILL.md). Run after moving files or adding skills.
---

# Sync check: `SKILL.md` vs on-disk assets

Use this skill to ensure workflow text and cross-references in `.claude/skills/` match real paths on disk.

## What to verify

1. **List** every `SKILL.md` under `.claude/skills/`, including nested paths (for example `meeting-summary/meeting-slack-summary/SKILL.md`).
2. **Extract** path-like strings that start with `.claude/skills/` (search the tree for that prefix, or use a small script).
3. For each unique path:
   - If it ends in `.py`, `.sh`, `.json`, `.md`, `.yaml`, `.yml`, or is a directory reference, confirm that path **exists** in the tree.
   - Skip variable placeholders such as `workspaces/<YYYY-MM-DD>/...`.

## Report format

```markdown
## Sync check report

### Missing references
- (none) or list of `.claude/skills/...` paths that appear in SKILL files but are not on disk

### Pure orchestration skills
- Skills that only reference other `SKILL.md` files and no scripts (expected in some cases)

### Orphan asset folders (optional)
- Folders under `.claude/skills/` with no references from any `SKILL.md` (informational only)
```

## Notes

- **Secrets**: `.claude/skills/ticktick-sync/.env` is gitignored; `env.example` should exist.
- **User-maintained data**: `user-mapping.md` may be gitignored; still confirm the parent directory exists.
- **Batch workflow**: `.claude/skills/batch-meeting-plan/SKILL.md` is the long-form spec for running parallel Phase 1 `meeting-plan` work.
