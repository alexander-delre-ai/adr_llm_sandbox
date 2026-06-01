---
name: workspace-search
description: Search the workspaces directory to find relevant context on a topic. Reads analysis.md, transcript.md, and research.md across meetings. Always cites sources. Escalates to meeting-research if nothing is found. Use when the user asks what was discussed, decided, or mentioned about a topic across past meetings.
---

# Workspace Search

Searches local meeting workspace files to find context on a topic. Reads structured analysis and raw transcripts. Returns concise, cited findings with no assumptions beyond what is written.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| query | Yes | Topic or question to search for |
| date_range | No | Approximate range, e.g. "last 2 weeks", "March 2026", "2026-03-01 to 2026-04-30". Defaults to all time. |

## Workflow

### Step 1: Identify candidate workspaces

- List all directories under `workspaces/` recursively to depth 3 (structure: `2026.WW/YYYY-MM-DD/{slug}/`).
- If the user provided a date range, filter to directories whose `YYYY-MM-DD` date falls within it. Otherwise include all.
- Sort candidates newest-first.

### Step 2: Search for relevance

For each candidate workspace:

1. Check whether the directory contains `analysis.md` or `transcript.md`.
2. Run a case-insensitive grep for the key terms derived from the query across `analysis.md`, `transcript.md`, and `research.md`.
3. Keep the workspace if any match is found. Discard silently if none.

Key term extraction:
- Split the query into 2-4 meaningful keywords or short phrases.
- Also try common synonyms or abbreviations if the initial terms are technical (e.g., "efuse" and "e-fuse", "NPM" and "power manager").

### Step 3: Read matching workspaces

For each kept workspace, read in this order:

1. `analysis.md` - always read fully.
2. `transcript.md` - always read fully alongside analysis.
3. `research.md` - read if present.
4. `tickets.md` - read only if the query directly concerns a JIRA ticket, action item status, or open task.

Do not read `slack-dm.json`, `status.md`, or `gemini-link.txt`.

### Step 4: Extract relevant content

From each workspace, extract only the passages directly relevant to the query. Do not paraphrase beyond what the text says. Do not infer intent or fill gaps.

For each extracted passage note:
- The workspace path (relative to repo root, e.g., `workspaces/2026.20/2026-05-12/shadow-katana-applied-sdv-sw-office-hours/`)
- The file it came from (`analysis.md`, `transcript.md`, or `research.md`)
- The meeting date (from the `YYYY-MM-DD` directory name)

### Step 5: Compose the response

**Format rules:**
- Be concise. One sentence per finding unless the source text requires more.
- Never state something as fact unless the workspace text explicitly says it.
- When evidence is partial or qualified in the source, preserve that qualification.
- Do not add commentary, opinions, or suggestions unless the user explicitly asks.

**Structure:**

```
## Findings

### {Meeting slug} ({YYYY-MM-DD})
> Source: `{relative file path}`

{Extracted finding(s), in plain prose or bullets.}

[Repeat for each relevant workspace, newest-first.]

---
## JIRA tickets  ← include this section only if a ticket is directly the answer
- {TICKET-ID}: {title} ({link if present in the file})
```

If only one workspace matched, skip the H3 heading and cite inline.

### Step 6: No results

If no workspace contains a match after searching all candidates:

1. State clearly: "No matching content found in workspaces for: {query}."
2. List the date range searched and the number of workspaces checked.
3. Offer to escalate: "Would you like me to search external sources (Slack, JIRA, Confluence) using /meeting-research?"
4. Do not fabricate or guess.

## Constraints

- Never make assumptions beyond what is written in the workspace files.
- Do not merge or reconcile conflicting information across meetings; surface both verbatim and cite each separately.
- Do not omit a finding because it seems minor; include everything relevant and let the user decide.
- If a claim in one file contradicts another, report both with their respective dates.
- Do not include action items or ticket proposals from `tickets.md` unless the query is specifically about tasks or JIRA status.
