---
name: meeting-summary
description: Loads meeting text from a pasted transcript, file path, or Google Docs URL (fetched via Google Drive MCP), writes workspaces transcript.md and structured analysis.md via meeting-analysis. No research, tickets, JIRA, Slack, or TickTick.
---

# Meeting summary

Slim alternative to `meeting_plan` when you want **structured analysis** under `workspaces/` only. Produces the same six-section `analysis.md` as the meeting-analysis skill. No tickets, JIRA, Slack, or TickTick.

## What this skill skips

- No `research.md`, `tickets.md`, Phase 2, or execution steps

## Input

Provide meeting content in any of these ways:

- **Google Docs URL**: Bare `https://docs.google.com/document/d/...` or `gemini summary: https://...` (fetch body via Google Drive MCP and use as primary analysis source).
- **File path**: Readable path (for example `@temp/meeting.md`); use the Read tool.
- **Inline text**: Paste the transcript in the user message.

If a **file** and a **Docs URL** are both provided, use the **file** as the primary analysis source. Still fetch the doc and append it under a `## Fetched Google Doc` section in `transcript.md` so nothing is dropped (same idea as `meeting_plan` using the transcript first and Gemini as supplement).

If a transcript **file contains** a line like `gemini summary: https://docs.google.com/...`, extract the URL, fetch that doc, strip the link line from the file text, and use the file body (without the link line) as the primary source. Append the fetched markdown under `## Fetched Google Doc` in `transcript.md`.

If nothing usable is provided, ask: "Please paste the meeting transcript, give a file path, or share a Google Docs link."

## Google Docs fetch (same contract as `meeting_plan`)

When you find a Google Docs URL in the user message or inside loaded file text:

1. **Extract the document ID**: the segment between `/d/` and the next `/` in the URL (for example from `https://docs.google.com/document/d/1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w/edit?tab=t.abc` use `1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w`).
2. **Fetch the document**: call `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`. Treat the returned markdown as the doc body.
3. Keep the **original URL string** to write into `transcript.md` as provenance (see below).

## Steps

1. **Resolve source text**
   - Scan the user message (after the command) for Google Docs URLs and optional file paths.
   - If a file path is given, read it with the Read tool. Scan that content for embedded `gemini summary:` or bare Docs URLs; if found, extract IDs, fetch each doc, and remove those lines from the in-file primary text.
   - For Docs URLs given alongside a file (not embedded), fetch and hold the markdown for the appendix section.
   - For **Docs-only** input, the primary analysis source is the fetched markdown.
2. **Rename chat** to `YYYY-MM-DD <meeting-title>` when known (transcript metadata, doc title or first heading, or temp filename stem like `meeting_plan`).
3. Create `workspaces/YYYY-MM-DD/<meeting-slug>/`. If it exists, ask overwrite vs versioned slug (`-v2`).
4. **Write `transcript.md`**
   - If the source included a fetched doc, start with two lines: `Source: <original URL>` then a blank line, then the primary body (file text or fetched-only content).
   - If there is also fetched supplementary content (second doc or file-plus-doc case), append `\n\n---\n\n## Fetched Google Doc\n\n` and the supplementary markdown.
   - If there was no Google fetch, write the primary transcript text only (no `Source:` line required).
5. If the input was a file under `temp/*.md` and its contents were fully copied into `transcript.md`, delete that original temp file. Do not delete other files in `temp/`.
6. Read and follow `.cursor/skills/meeting-analysis/SKILL.md`. Use the full text of `transcript.md` as the meeting content and the workspace directory as the output location for `analysis.md`.
7. Reply with paths to `transcript.md` and `analysis.md` and a brief takeaway summary.

Stay in **Agent** mode end to end unless the user asks for collaborative edits.
