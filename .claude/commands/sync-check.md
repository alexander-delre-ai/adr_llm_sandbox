---
description: Checks for content drift between .claude/commands/ and their .cursor counterparts. Reports missing files, new skills not yet ported, and substantive differences in workflow logic. Run this before/after editing either location to keep capabilities in sync.
---

# Sync Check: .claude vs .cursor

Compares `.claude/commands/` files against their `.cursor/` counterparts and reports differences so you can decide which direction to sync.

## File Mapping

Each `.claude/commands/` file has a corresponding source in `.cursor/`:

| Claude Command | Cursor Counterpart |
|---|---|
| `.claude/commands/meeting_plan.md` | `.cursor/commands/meeting_plan.md` |
| `.claude/commands/meeting_summary.md` | `.cursor/skills/meeting-summary/SKILL.md` |
| `.claude/commands/meeting-analysis.md` | `.cursor/skills/meeting-analysis/SKILL.md` |
| `.claude/commands/meeting-workspace.md` | `.cursor/skills/meeting-workspace/SKILL.md` |
| `.claude/commands/meeting-tickets.md` | `.cursor/skills/meeting-tickets/SKILL.md` |
| `.claude/commands/meeting-slack-summary.md` | `.cursor/skills/meeting-summary/meeting-slack-summary/SKILL.md` |
| `.claude/commands/kata-jira-task-creation.md` | `.cursor/skills/kata-jira-task-creation/SKILL.md` |
| `.claude/commands/avp-jira-task-creation.md` | `.cursor/skills/avp-jira-task-creation/SKILL.md` |
| `.claude/commands/app-dev-k1-hw-ticket-creation.md` | `.cursor/skills/app-dev-k1-hw-ticket-creation/SKILL.md` |
| `.claude/commands/daily-todos.md` | `.cursor/skills/daily-todos/SKILL.md` |
| `.claude/commands/ticktick-sync.md` | `.cursor/skills/ticktick-sync/SKILL.md` |

## Expected Differences (Ignore These)

The Claude versions have deliberate modifications that are not drift - do not flag these as issues:

- **MCP tool names**: `.cursor` uses `user-atlassian-mcp-kata` server name; `.claude` uses `mcp__kata-atlassian__*` tool prefix
- **Skill references**: `.cursor` files reference `.cursor/skills/X/SKILL.md`; `.claude` files reference `.claude/commands/X.md`
- **Em-dashes**: `.cursor` files may contain em-dashes (`—`); `.claude` files replace them with commas, colons, or hyphens
- **Frontmatter**: `.cursor` files use `name:` + `description:`; `.claude` files use only `description:`
- **Script paths**: Both reference `.cursor/skills/*/scripts/` - this is correct and intentional
- **meeting_summary**: Substantive workflow in `.cursor/skills/meeting-summary/SKILL.md` and `.cursor/commands/meeting_summary.md`; compare to `.claude/commands/meeting_summary.md`

## Workflow

### Step 1 - Discover unmapped files

1. List all files in `.claude/commands/` (excluding `sync-check.md` itself)
2. List all files in `.cursor/commands/`
3. List all `SKILL.md` files under `.cursor/skills/*/`
4. Cross-reference against the mapping table above and report:
   - **Orphaned Claude commands**: `.claude/commands/` files with no `.cursor/` counterpart
   - **Unported Cursor skills**: `.cursor/skills/*/SKILL.md` files with no `.claude/commands/` counterpart
   - **Unported Cursor commands**: `.cursor/commands/` files with no `.claude/commands/` counterpart

### Step 2 - Compare each mapped pair

For each pair in the mapping table, read both files and compare them for **substantive differences** - changes to workflow logic, steps, field values, validation rules, or behavior. Ignore the expected differences listed above.

Focus on:
- Added or removed workflow steps
- Changed field defaults or validation rules
- New features or capabilities in one but not the other
- Changed output formats or file structures
- Updated epic IDs, release mappings, or other reference data
- New error handling or edge cases

### Step 3 - Check git modification times and detect bilateral changes

For each differing pair:

1. Run `git log -1 --format="%ai %s" -- <file>` on both files to get each file's last commit date and message.
2. Run `git log --oneline -- <file>` on both files to get the full commit history for each.
3. **Detect bilateral changes**: Find the most recent commit hash where both files were last intentionally aligned. Use this heuristic:
   - Search both files' git logs for a shared sync commit (e.g., a commit touching both files at the same timestamp, or a commit message containing "sync", "port", or "ported").
   - If found, check whether both files have commits *after* that shared point. If yes, both sides have diverged independently - flag as **bilateral changes**.
   - If no shared sync commit is found and both files have been modified within the same general timeframe (within 7 days of each other), flag as **possible bilateral changes** and recommend manual inspection.
4. If only one side has commits after the last sync point (or one file is clearly older), the sync direction is clear.

### Step 4 - Report results

Output a structured report with these sections:

---

## Sync Report

### Unmapped Files

**Orphaned Claude commands** (exist in `.claude/commands/` but no `.cursor/` counterpart):
- [list or "None"]

**Unported Cursor skills** (exist in `.cursor/skills/` but no `.claude/commands/` counterpart):
- [list or "None"]

**Unported Cursor commands** (exist in `.cursor/commands/` but no `.claude/commands/` counterpart):
- [list or "None"]

---

### Differences Found

For each pair with substantive differences:

**`<claude-file>` vs `<cursor-file>`**
- More recently modified: `<which file>` (`<date>`)
- Bilateral changes: [Yes / No / Possible - inspect manually]
- Differences:
  - [bullet list of specific changes - what section, what changed, and which side has the change]
- Recommended action: [sync Claude -> Cursor / sync Cursor -> Claude / MERGE REQUIRED - both sides changed]

---

### In Sync

Files with no substantive differences (after ignoring expected modifications):
- [list of pairs that match]

---

### Recommended Actions

Prioritized list of sync actions to take, with the direction for each.

---

## Syncing Changes

When the user asks to apply a sync after seeing the report:

### Cursor -> Claude (new content in .cursor, port to .claude)

1. Read the updated `.cursor` file
2. Apply Claude-specific modifications:
   - Replace `user-atlassian-mcp-kata` server references with `mcp__kata-atlassian__*` tool names
   - Update skill references from `.cursor/skills/X/SKILL.md` to `.claude/commands/X.md`
   - Remove any em-dashes (replace with comma, colon, or hyphen as appropriate)
   - Change frontmatter from `name:` + `description:` to just `description:`
3. Write the updated `.claude/commands/` file

### Claude -> Cursor (new content in .claude, port to .cursor)

1. Read the updated `.claude` file
2. Apply Cursor-specific modifications:
   - Replace `mcp__kata-atlassian__*` tool references with `user-atlassian-mcp-kata` server name
   - Update skill references from `.claude/commands/X.md` to `.cursor/skills/X/SKILL.md`
   - Change frontmatter to include both `name:` and `description:` fields
3. Write the updated `.cursor` file

### Bilateral Merge (both sides have independent changes)

When both files have been modified since their last sync point:

1. Read both files in full.
2. Identify each substantive difference and classify it:
   - **Claude-only change**: present in `.claude` but not `.cursor` (likely a Claude-specific improvement to port back)
   - **Cursor-only change**: present in `.cursor` but not `.claude` (likely a Cursor improvement to port forward)
   - **Conflicting change**: both sides modified the same section differently (requires a decision)
3. For each non-conflicting change, apply the change to the other side (with platform-specific modifications as above).
4. For conflicting changes, present both versions side-by-side and ask the user which to keep (or how to combine them).
5. After resolving all conflicts, write both updated files and confirm which version is now canonical.

### Adding a new skill to both locations

When a new skill is created in either location, automatically create its counterpart with the appropriate modifications applied.
