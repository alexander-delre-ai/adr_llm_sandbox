---
name: meeting-workspace
description: Creates a structured workspace directory under /workspaces for a meeting, saving the transcript, analysis, JIRA tickets, and action plan. Use after completing a meeting analysis to persist all artifacts to disk.
---

# Meeting Workspace

Creates a persistent directory under `workspaces/` in the current repo for a completed meeting analysis and saves all artifacts to it.

## Directory naming

Workspaces are organized by date, with meeting names as subdirectories:

```
workspaces/<YYYY-MM-DD>/<slugified-title>/
```

Slugify rules: lowercase, spaces and special characters replaced with hyphens, max 60 chars.

Example: `workspaces/2026-03-11/q1-planning-kickoff/`

## Directory structure

```
workspaces/<YYYY-MM-DD>/<meeting-slug>/
  transcript.md OR summary.md    <- original content (transcript if full transcript, summary.md if meeting summary)
  analysis.md            <- full 6-section meeting analysis (updated after ticket review)
  tickets.md             <- original editable tickets file
  gemini-link.txt        <- Gemini summary URL (if provided) for Slack reference
  jira-tickets/
    <slug-of-ticket-name>.json   <- JIRA ticket metadata with actual keys and URLs
  slack-message.md       <- office hours thread content and AlexD message
  ticktick-sync.md       <- TickTick sync results summary
  chat-history.md        <- summary of key decisions made during the AI session
```

## Workflow

1. Derive the date and meeting slug from meeting title and date (see naming rules above)
2. Create the directory: `mkdir -p workspaces/<YYYY-MM-DD>/<meeting-slug>`
3. Handle original content file:
   - **If from temp/ directory**: Move the original file to workspace as `transcript.md` or `summary.md` (based on content type)
   - **If inline content**: Write `transcript.md` (full transcript) or `summary.md` (meeting summary) with provided content
   - **Efficiency**: Moving temp files avoids re-processing and preserves original formatting
4. Copy `<meeting-name>.analysis.md` and `<meeting-name>.tickets.md` to workspace directory
5. Write `gemini-link.txt` with Gemini summary URL (if provided during workflow)
6. For each JIRA ticket, write `jira-tickets/<ticket-slug>.json`
   - Derive filename by slugifying the ticket summary (lowercase, hyphens)
   - Write ticket metadata including actual JIRA key, URL, and creation details
7. Write `slack-message.md` with office hours thread content and AlexD message (if Slack summary was generated)
8. Record TickTick sync results in `ticktick-sync.md` (total items, created, skipped, errors)
9. Write `chat-history.md` using this template:

```markdown
# Session Summary: <title> (<date>)

## Decisions made during this session

- ...

## Open items flagged for follow-up

- ...

## Files saved

| File | Contents |
|------|----------|
| transcript.md OR summary.md | Original meeting content |
| analysis.md | Full 6-section analysis (updated after review) |
| tickets.md | Original editable tickets file |
| gemini-link.txt | Gemini summary URL (if provided) |
| jira-tickets/ | JIRA JSON payloads |
| ticktick-sync.md | TickTick sync results |
```

10. Confirm to the user:

```
Workspace created at workspaces/<YYYY-MM-DD>/<meeting-slug>/
  transcript.md OR summary.md
  analysis.md
  tickets.md
  gemini-link.txt (if provided)
  jira-tickets/
    <n> ticket(s) with actual JIRA keys saved
  slack-message.md
  ticktick-sync.md
  chat-history.md
```

## Notes

- If `workspaces/` does not exist, create it first with `mkdir -p workspaces`
- If a directory for the same date/slug already exists, append `-2`, `-3`, etc. to the meeting slug rather than overwriting
- All files are UTF-8 markdown or JSON; no binary content
- JIRA ticket files now contain actual ticket metadata, not just payloads
- Workspaces are stored within the current repository for version control and organization
