# /meeting_summary

**Mode: Agent**

Slim alternative to `meeting_plan` when you want **structured analysis** under `workspaces/` only. Produces a six-section `analysis.md` (same shape as the meeting-analysis skill). No `research.md`, `tickets.md`, Phase 2, JIRA, Slack, or TickTick.

## What this command does not do

- No `research.md`, `tickets.md`, or ticket review loops
- No JIRA, Slack, or TickTick

## Input

Provide meeting content in any of these ways:

- **Google Docs URL**: Bare `https://docs.google.com/document/d/...` or `gemini summary: https://...` (fetch body via Google Drive MCP and use as primary analysis source, or as supplement when a file is primary).
- **File path**: Readable path (for example `@temp/meeting.md`); use the Read tool.
- **Inline text**: Paste the transcript in the user message.

If a **file** and a **Docs URL** are both provided, use the **file** as the primary analysis source. Still fetch the doc and append it under a `## Fetched Google Doc` section in `transcript.md` so nothing is dropped.

If a transcript **file contains** a line like `gemini summary: https://docs.google.com/...`, extract the URL, fetch that doc, strip the link line from the file text, and use the file body (without the link line) as the primary source. Append the fetched markdown under `## Fetched Google Doc` in `transcript.md`.

If nothing usable is provided, ask: "Please paste the meeting transcript, give a file path, or share a Google Docs link."

## Google Docs fetch (same contract as `meeting_plan`)

When you find a Google Docs URL in the user message or inside loaded file text:

1. **Extract the document ID**: the segment between `/d/` and the next `/` in the URL (for example from `https://docs.google.com/document/d/1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w/edit?tab=t.abc` use `1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w`).
2. **Fetch the document**: use `fetch_mcp_resource` with server `user-google-drive` and URI `gdrive:///<document-id>`. Treat the returned markdown as the doc body.
3. Keep the **original URL string** to write into `transcript.md` as provenance (see below).

## Execution steps (transcript and workspace)

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
6. Run the **Analysis workflow** below using the full text of `transcript.md` and the workspace directory as the output location for `analysis.md`.
7. Reply with paths to `transcript.md` and `analysis.md` and a brief takeaway summary.

Stay in **Agent** mode end to end unless the user asks for collaborative edits.

## Analysis workflow (`analysis.md`)

Process the meeting content and write `analysis.md` in the workspace directory from step 3. No separate research or tools beyond what you already need for the transcript. Skip any instructions elsewhere about updating from `tickets.md` (this command does not create `tickets.md`).

### Step A: Meeting context

**First, identify the content type:**

- **Full Transcript**: Detailed conversation with speaker names, timestamps, and dialogue
- **Gemini Summary**: AI summary with sections such as Summary, Details, Next Steps

Pull these fields (adapt to content type):

| Field | Full Transcript | Gemini Summary |
| --- | --- | --- |
| Meeting title | explicit title, series name, or infer from agenda | title at top or in Invited |
| Date and time | from transcript metadata | at beginning (for example "Mar 10, 2026") |
| Participants | speaker names from dialogue (exclude meeting rooms) | Invited list, filter meeting rooms and strip email domains from names |
| Meeting location | conference room names in participant list | Invited or context |
| Stated objective | agenda or opening | Summary or main topics |

**Important**: Filter meeting room style entries from participants where appropriate. For Gemini summaries, you may clean names (for example `nuthan.sabbani@global.komatsu` to "Nuthan Sabbani").

### Step B: Key decisions

A decision is agreement, approval, or a chosen direction.

- **Transcript signals**: "we decided", "agreed to", "going with", "approved", "confirmed"
- **Gemini**: definitive statements in Summary and Details

Output: numbered list, `Decision N: <one-sentence summary>`

### Step C: Discussion themes

Group into 3 to 7 named themes. Each: short label (2 to 4 words) and one-sentence description.

- **Transcript**: group by topic
- **Gemini**: use Details headers and groupings

### Step D: Unresolved questions

Open questions, blockers, deferred work.

- **Transcript**: "we need to figure out", TBD, "who owns", "not sure yet", follow up
- **Gemini**: uncertainty, questions, future items

Output: bulleted list; include responsible person in brackets when known.

### Step E: Action items (detail)

**Transcript**: commitment language ("I'll", "we need to", "action item")

**Gemini**: Suggested next steps and action-oriented Details lines

For each item capture:

- **What**: clear imperative
- **Who**: assignee or "Unassigned"
- **When**: due or sprint if mentioned
- **Priority**: High / Medium / Low from context
- **Theme**: from Step C

### Step F: Prioritized action plan

Markdown table sorted with High first:

| # | Proposed Action Item | Assignee | Priority | Due | Type | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ... | ... | High | ... | Coordination | (for example: to Slack tracking) |
| 2 | ... | ... | High | ... | Technical | (for example: to JIRA) |

After the table, a **Next steps** section: 3 to 5 bullets for immediate follow-up.

## Output: `analysis.md` structure

Create `analysis.md` with:

```markdown
# Meeting Analysis: <title> (<date>)

## 1. Meeting Context
[Context details]

## 2. Key Decisions
[Numbered decisions]

## 3. Discussion Themes
[Named themes with descriptions]

## 4. Unresolved Questions
[Bullets with owners where known]

## 5. Action Items
[Detailed items with metadata]

## 6. Prioritized Action Plan
[Table and Next steps]
```
