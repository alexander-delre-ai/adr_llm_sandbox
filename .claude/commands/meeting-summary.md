---
description: Meeting text from transcript, file, or Google Docs (Drive MCP fetch), writes workspace transcript.md and analysis.md via meeting-analysis. No research, tickets, JIRA, Slack, or TickTick.
---

# /meeting-summary

Slim alternative to `/meeting-plan` when you only want **structured analysis** on disk. Reuses the same `analysis.md` format as `/meeting-analysis`.

## What this command does **not** do

- No `research.md`, `tickets.md`, JIRA creation, Slack summary, or TickTick sync
- No Phase 2 and no `confirm` / ticket review loop

## Input

Provide meeting content in any of these ways:

- **Google Docs URL**: Bare `https://docs.google.com/document/d/...` or `gemini summary: https://...` (fetch via Google Drive MCP, use as analysis source).
- **File path**: Any readable path (for example `@temp/2026-04-14-sync.md`). The Read tool loads the file.
- **Inline text**: Paste the transcript in the same message as the command.

If a **file** and a **Docs URL** are both in the message, use the **file** as the primary analysis source, fetch the doc, and put both into `transcript.md` (file body first, then a `## Fetched Google Doc` section with the fetched markdown).

If a transcript **file contains** a line like `gemini summary: https://docs.google.com/...`, extract the URL, fetch the doc, remove that link line from the file text for the primary body, and append the fetched markdown under `## Fetched Google Doc` in `transcript.md`.

If nothing usable is provided, ask: "Please paste the meeting transcript, provide a file path, or share a Google Docs link."

## Google Docs / Gemini link handling

When you find a Google Docs URL in the user message or inside loaded file text:

1. **Extract the document ID** from the URL: the segment between `/d/` and the next `/` (for example from `https://docs.google.com/document/d/1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w/edit?tab=t.abc` extract `1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w`).
2. **Fetch the document** using the Google Drive MCP: call `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`. This returns the full document content as markdown.
3. Keep the **original URL** for the `Source:` line at the top of `transcript.md` whenever a doc was fetched.

## Steps

1. **Resolve source text**: Scan the message for Docs URLs and file paths. Read files with the Read tool. Extract embedded links from file text, fetch those docs, strip link lines from the primary file body as needed. Fetch any standalone URLs from the message. Build the final `transcript.md` body (see Input for ordering: `Source:` URL line plus blank line when a fetch occurred, primary body, optional `## Fetched Google Doc` appendix).
2. **Rename chat** once a meeting title is known: `YYYY-MM-DD <meeting-title>` (same convention as `/meeting-plan`).
3. **Workspace directory** `workspaces/YYYY-MM-DD/<meeting-slug>/`. If it already exists, ask overwrite vs versioned slug (for example `<slug>-v2`).
4. **Write `transcript.md`** with the resolved content.
5. **Temp cleanup**: If the input was a file under `temp/`, delete that original file after its contents are represented in `transcript.md`. Do not delete other files in `temp/`.
6. **Create analysis**: Read and follow `.claude/commands/meeting-analysis.md`. Use the full text of `transcript.md` as meeting content and the workspace directory as the output location. Produce `analysis.md` with the standard six sections.
7. **Report**: Give the paths to `transcript.md` and `analysis.md` and a short verbal summary of the main takeaways.

Stay in **Agent** mode end to end unless the user asks for collaborative edits.
