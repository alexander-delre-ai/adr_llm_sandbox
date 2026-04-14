---
name: meeting-summary
description: Transcript-only meeting path. Loads a pasted transcript or file, writes workspaces transcript.md and structured analysis.md via meeting-analysis. No Google Docs fetch, research, tickets, JIRA, Slack, or TickTick.
---

# Meeting summary (transcript only)

Slim alternative to `meeting_plan` when you already have a **full transcript** and only want **structured analysis** under `workspaces/`. Produces the same six-section `analysis.md` as the meeting-analysis skill. No tickets, JIRA, Slack, or TickTick.

## What this skill skips

- No Google Docs fetch (use `meeting_plan` for Gemini or Docs links)
- No `research.md`, `tickets.md`, Phase 2, or execution steps

## Input

- **File path**: Readable path (for example `@temp/meeting.md`); use the Read tool.
- **Inline**: Paste the transcript in the user message.

If missing, ask: "Please paste the meeting transcript or give a file path."

Do not use a bare Google Docs URL as the transcript source; send the user to `meeting_plan` if they only have a link.

## Steps

1. Load transcript from file and/or message body.
2. **Rename chat** to `YYYY-MM-DD <meeting-title>` when known (same idea as `meeting_plan`).
3. Create `workspaces/YYYY-MM-DD/<meeting-slug>/`. If it exists, ask overwrite vs versioned slug (`-v2`).
4. Write `transcript.md` with the full text.
5. If input was `temp/*.md`, delete that file after copying into `transcript.md`.
6. Read and follow `.cursor/skills/meeting-analysis/SKILL.md` to write `analysis.md` in that workspace.
7. Reply with paths to both files and a brief takeaway summary.

Stay in **Agent** mode end to end unless the user asks for collaborative edits.
