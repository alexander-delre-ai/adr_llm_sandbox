---
description: Transcript-only meeting workflow. Accepts a pasted transcript or file path, writes workspace transcript.md and structured analysis.md via meeting-analysis. No Google Docs fetch, research, tickets, JIRA, Slack, or TickTick.
---

# /meeting_transcript_summary

Slim alternative to `/meeting_plan` for when you already have a **full transcript** (text) and only want a structured **summary and analysis** on disk. Reuses the same `analysis.md` format as `/meeting-analysis`.

## What this command does **not** do

- No Google Docs or Gemini link fetch (use `/meeting_plan` for doc links)
- No `research.md`, `tickets.md`, JIRA creation, Slack summary, or TickTick sync
- No Phase 2 and no `confirm` / ticket review loop

## Input

Provide the transcript in one of these ways:

- **File path**: Any readable path (for example `@temp/2026-04-14-sync.md`). The Read tool loads the file.
- **Inline text**: Paste the transcript in the same message as the command.

If nothing is provided, ask: "Please paste the meeting transcript or give a file path to the transcript."

**Transcript-only**: The primary source must be the file or pasted text. Do not treat a bare Google Docs URL as the transcript; point the user to `/meeting_plan` if they only have a link.

## Steps

1. **Load transcript** from the file path and/or the user message body (after removing the command line).
2. **Rename chat** once a meeting title is known: use `YYYY-MM-DD <meeting-title>` (same convention as `/meeting_plan`). Prefer an explicit title from transcript metadata; otherwise derive from the temp filename without extension (for example `temp/2026-04-14-vt-sync.md` becomes `2026-04-14 vt-sync`).
3. **Workspace directory** `workspaces/YYYY-MM-DD/<meeting-slug>/` (lowercase slug, hyphens, max about 60 characters). Before creating, if that directory already exists, ask whether to overwrite or use a versioned slug (for example `<slug>-v2`).
4. **Write `transcript.md`** in the workspace with the full transcript text.
5. **Temp cleanup**: If the input was a file under `temp/`, delete that original file after its contents are copied into `transcript.md`. Do not delete other files in `temp/`.
6. **Create analysis**: Read and follow `.claude/commands/meeting-analysis.md`. Pass the transcript as meeting content and the workspace directory as the output location. Produce `analysis.md` with the standard six sections (context, decisions, themes, questions, action items, prioritized plan).
7. **Report**: Give the paths to `transcript.md` and `analysis.md` and a short verbal summary of the main takeaways.

Stay in **Agent** mode end to end unless the user asks for collaborative edits.
