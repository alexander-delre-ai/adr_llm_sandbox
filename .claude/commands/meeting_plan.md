---
description: Full meeting workflow. Accepts Google Docs link, temp transcript, inline text, or combinations. Produces analysis, optional research.md, tickets, then on user approval creates JIRA tickets, Slack summary, TickTick sync, Google Doc sharing, and workspace bundle.
---

# /meeting_plan

**Mode: Agent**

Accept meeting content and produce a full meeting analysis with reviewable JIRA ticket plans, then optionally create actual tickets via MCP integration, Slack summary, TickTick sync, and Google Doc sharing.

## Input

The meeting content may be provided as any combination of:

- **Google Docs or Gemini link**: AI-generated meeting notes or manual doc (fetched via Google Drive MCP)
- **Full transcript**: Inline paste, file path (Read tool), or file under `temp/`
- **Transcript file that embeds** a line like `gemini summary: https://docs.google.com/...` (extract URL, fetch doc, use file body minus that line as primary source where applicable)

**Input format examples:**

- `gemini summary: https://docs.google.com/document/d/.../edit?tab=...`
- `https://docs.google.com/document/d/.../edit?tab=...` (bare URL)
- `@temp/meeting-transcript.md`
- `@temp/meeting-transcript.md` plus a Gemini link in the same message
- Inline transcript text in the message

If no content is provided, ask: "Please paste the meeting transcript, provide a file path, or share a Google Docs link."

**Google Docs link handling**

1. Extract the document ID: segment between `/d/` and the next `/` in the URL.
2. Fetch using Google Drive MCP: `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`.
3. **Primary source**:
   - If the link is the **only** input, use fetched markdown as the primary analysis source.
   - If a transcript file or inline text is **also** provided, use that as primary; use fetched doc as supplement if the transcript is sparse; always retain the original URL for Slack and doc sharing.
   - If a transcript **file contains** an embedded Gemini or Docs URL line, strip that line from the body for the primary text, fetch the doc, and keep the URL for later steps.

**Temp directory**: If input is from `temp/`, delete the original temp file after its content is represented in `transcript.md` (Phase 2 workspace step may move or finalize paths). Do not delete other files in `temp/`.

## Phase 1: Analysis and staging

1. Accept and normalize input from the user message (and from any file read via the Read tool).
2. **Extract and fetch** all Google Docs URLs found in the message or in loaded file text. Store each original URL string for `gemini-link.txt` and for `transcript.md` when using the URL-only pattern below.
3. **Rename chat** once the meeting title is known: `YYYY-MM-DD <meeting-title>` (same string you will use for the workspace slug). Derive title from transcript metadata, doc title or first heading, or temp filename stem.
4. **Create workspace directory** `workspaces/YYYY-MM-DD/<meeting-slug>/`. If it exists, ask: overwrite, or versioned slug (e.g. `<slug>-v2`).
5. **Write `transcript.md`**:
   - **Google Docs link only** (no full transcript body): write a **single line** containing only the Google Docs URL. This is the contract for Slack summary and Google Doc sharing steps.
   - **Temp file or inline transcript**: write the full transcript text. If a Docs URL was also used, you may append `## Fetched Google Doc` with fetched markdown (optional) or rely on the URL in `gemini-link.txt` only; do not drop the URL needed for sharing.
   - **Mixed file plus standalone URL**: follow `meeting_summary` style if helpful: `Source: <url>` plus body, or single-line URL file when the workflow is Doc-first (batch mode).
6. **Write `gemini-link.txt`** whenever you have a Google Docs URL for this meeting: one line, the full URL. Slack command checks this file first.
7. **Create meeting analysis**: Read and follow `.claude/commands/meeting-analysis.md` to create `analysis.md`.
8. **Research unresolved questions**: Read and follow `.claude/commands/meeting-research.md`, but first classify each question from **Section 4** of `analysis.md`:
   - **Research** (run research): architecture, implementation, technical decisions, prior art, existing tickets, design patterns, system behavior.
   - **Skip** (note only in `research.md`): scheduling, coordination, who will attend, logistics, or questions that need a human decision outside tools.
   - **Parallel subagents**: For every "Research" item, launch concurrent subagents (one question each) with workspace path as context. Collect all results.
   - For skipped questions, add a short entry: "Skipped: coordination or scheduling question, not researchable via Slack, Confluence, or JIRA."
   - Compile into **`research.md`** using the batch format in `meeting-research.md`.
9. **Pause only if critical**: If assignees are unknowable, action items conflict, or context blocks ticket generation, ask the user. Otherwise continue through staging.
10. **Zero action items**: If analysis has no action items (status-only or demo meeting), skip ticket staging (skip steps that create `tickets.md` content beyond a note if needed), still write `research.md` if questions existed, then go to Phase 1 wrap-up and Phase 2 with **Slack-only** path (no JIRA, no TickTick for tickets). Tell the user clearly.
11. **Create ticket proposals**: Read and follow `.claude/commands/meeting-tickets.md` to create `tickets.md` (epic inference, assignee normalization, story points heuristics, release inference, suggested groupings).
12. **Stage files** (typical set):
    - `analysis.md`
    - `research.md`
    - `tickets.md`
    - `transcript.md`
    - `gemini-link.txt` when a Docs URL exists
13. **Phase 1 review (no canvas)**: Claude Code may not expose a browser canvas tool. Instead:
    - **Show inferred epic** from `.claude/skills/meeting-tickets/meeting-epic-mapping.json` default for this meeting title.
    - **Markdown table**: Render a read-only summary table in chat parsed from `tickets.md` (title, assignee, priority, tracking, parent_id, release, story_points). Tell the user to edit `tickets.md` directly for changes (the table is for review only).
    - **Google Doc sharing recipients**: If `transcript.md` is a single-line Google Docs URL (or `gemini-link.txt` exists), build the proposed recipient list from analysis Section 1 attendees plus assignees from `tickets.md`, resolve emails via `.claude/skills/meeting-summary/meeting-slack-summary/user-mapping.md` (and Slack profile lookup if allowed). Present the list so the user can note adds or removals before Phase 2.

**Gate**: Do **not** run Phase 2 until the user replies with **`continue`** or **`confirm`** or **`create tickets`** (all mean proceed), or **`stop`** (end with no JIRA, no Slack, no sharing). Treat other messages as still in review unless the user clearly cancels.

## Phase 2: Execution

Run only after **`continue`**, **`confirm`**, or **`create tickets`**. On **`stop`**, leave workspace files as-is and do not create tickets or send Slack.

1. **Re-read `tickets.md`** (skip JIRA steps if there were zero JIRA-tracked items).
2. **Duplicate detection** (per proposed KATA ticket before create): use `searchJiraIssuesUsingJql` such as `project = KATA AND parent = <epic> AND status != Done AND status != Closed AND summary ~ "key terms"`. If a strong duplicate match exists, skip creating that row and append to `tickets.md` under `## Skipped Duplicates` with JIRA key and link. No extra user prompt for each skip.
3. **Create JIRA tickets**: Read and follow:
   - `.claude/commands/kata-jira-task-creation.md` for KATA- parent_ids
   - `.claude/commands/avp-jira-task-creation.md` for AVP- parent_ids  
   Only for `tracking: jira` or `tracking: both`. Respect defaults, assignee lookup, documentation routing, AVP mirror rules in those commands. On per-ticket failure, log and continue; report failures at the end.
4. **Update `analysis.md`**: Re-read final `tickets.md` and align Sections 5 and 6 with final titles and keys.
5. **Slack summary**: Read and follow `.claude/commands/meeting-slack-summary.md`. Pass Google Doc URL from `gemini-link.txt` or from single-line `transcript.md` if needed. KATA keys only in summary per command rules.
6. **Share Google Doc** (when `transcript.md` is a one-line Google Docs URL or URL is in `gemini-link.txt`): extract file ID, build recipient list (with Phase 1 adjustments), resolve emails from `user-mapping.md` and Slack if needed, then call Google Drive MCP `shareFile` with `role: writer`, `sendNotificationEmail: true` where supported. Log who was granted access and who was skipped.
7. **TickTick sync**: Read `.claude/commands/ticktick-sync.md` and run:

   `python3 .claude/skills/ticktick-sync/scripts/sync_meeting_items.py --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md --meeting "<Meeting Title>"`

8. **Workspace bundle**: Read and follow `.claude/commands/meeting-workspace.md` to persist artifacts, metadata, and sync results.
9. **User mapping**: If new Applied attendees were discovered, update `.claude/skills/meeting-summary/meeting-slack-summary/user-mapping.md` and commit with message: `update user-mapping with attendees from <meeting-slug>`.
10. **Final `analysis.md` pass**: Re-read `tickets.md` and rewrite Sections 5 and 6 with real KATA keys and final wording. Return workspace path and ticket URLs.

## Two-phase summary

| Phase | Purpose |
|-------|---------|
| 1 | Fetch, analyze, research, stage `tickets.md`, present table and recipients, wait for `continue` / `confirm` or `stop` |
| 2 | Dedupe check, JIRA, analysis update, Slack, Doc share, TickTick, workspace, mapping commit, final analysis |

## Benefits

- User-gated execution after automated staging
- Smart defaults: epic, release, story points, tracking, assignee normalization
- Research filtered to tool-answerable questions
- Duplicate detection before create
- Doc sharing and Slack reference link in one flow
- TickTick and workspace completion for traceability
