---
name: meeting-workspace
description: Creates a structured workspace directory under /workspaces for a meeting, saving the transcript, analysis, JIRA tickets, and action plan. Use after completing a meeting analysis to persist all artifacts to disk.
---

# Meeting Workspace

Creates a persistent directory under `/workspaces` for a completed meeting analysis and saves all artifacts to it.

## Directory naming

Derive the directory name from the meeting title and date:

```
/workspaces/<YYYY-MM-DD>-<slugified-title>/
```

Slugify rules: lowercase, spaces and special characters replaced with hyphens, max 60 chars.

Example: `2026-03-11-q1-planning-kickoff`

## Directory structure

```
/workspaces/<meeting-slug>/
  transcript.md          <- original transcript (verbatim)
  analysis.md            <- full 7-section meeting analysis
  action-items.md        <- extracted tasks table only (Steps 5 + 7)
  jira-tickets/
    <slug-of-ticket-name>.json   <- one file per JIRA ticket payload
  chat-history.md        <- summary of key decisions made during the AI session
```

## Workflow

1. Derive the directory slug from meeting title and date (see naming rules above)
2. Create the directory: `mkdir -p /workspaces/<slug>`
3. Write `transcript.md` - the verbatim transcript provided by the user
4. Write `analysis.md` - the complete meeting analysis output (all 7 sections)
5. Write `action-items.md` using this template:

```markdown
# Action Items: <title> (<date>)

## Tasks

| # | What | Who | Priority | Due | Theme |
|---|------|-----|----------|-----|-------|
| 1 | ...  | ... | High     | ... | ...   |

## Next steps

- ...
```

6. For each JIRA ticket payload, write `jira-tickets/<ticket-slug>.json`
   - Derive filename by slugifying the ticket summary (lowercase, hyphens)
   - Write the raw JSON payload as produced by the relevant jira-task-creation skill
7. Write `chat-history.md` using this template:

```markdown
# Session Summary: <title> (<date>)

## Decisions made during this session

- ...

## Open items flagged for follow-up

- ...

## Files saved

| File | Contents |
|------|----------|
| transcript.md | Original meeting transcript |
| analysis.md | Full 7-section analysis |
| action-items.md | Extracted tasks and next steps |
| jira-tickets/ | JIRA JSON payloads |
```

8. Confirm to the user:

```
Workspace created at /workspaces/<slug>/
  transcript.md
  analysis.md
  action-items.md
  jira-tickets/
    <n> ticket(s) saved
  chat-history.md
```

## Notes

- If `/workspaces` does not exist, create it first with `mkdir -p /workspaces`
- If a directory for the same slug already exists, append `-2`, `-3`, etc. rather than overwriting
- All files are UTF-8 markdown or JSON; no binary content
