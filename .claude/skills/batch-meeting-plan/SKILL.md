---
name: batch-meeting-plan
description: Runs meeting-plan in parallel across multiple Google Docs links. Each link launches a separate subagent that independently fetches, analyzes, creates a workspace, and stages tickets. All meetings pause at Phase 1 for user review. Use when processing multiple meeting notes at once, batch meeting analysis, or running meeting-plan on a list of links.
---

# Batch Meeting Plan

Accepts a list of Google Docs/Gemini links and launches a parallel `meeting-plan` subagent for each one. Each subagent runs Phase 1 (fetch, analyze, stage workspace and tickets) independently. All meetings pause at Phase 1 for user review before any JIRA tickets are created.

## Input

One or more Google Docs URLs provided inline, one per line. Accepts any of these formats:

```
https://docs.google.com/document/d/.../edit?tab=...
gemini summary: https://docs.google.com/document/d/.../edit
https://docs.google.com/document/d/...
```

If no links are provided, ask: "Please paste the Google Docs links (one per line)."

## Workflow

### Step 1 - Parse links

Extract all Google Docs URLs from the user's message. For each URL:
- Validate it matches `https://docs.google.com/document/d/<id>/...`
- Extract the document ID (segment between `/d/` and the next `/`)
- Assign each a sequential label (Meeting 1, Meeting 2, ...) for progress tracking

Report the count: "Found N meeting links. Launching N parallel agents."

### Step 2 - Launch parallel subagents

For each link, launch a `Task` subagent with `subagent_type="generalPurpose"` and `run_in_background=true`. Each subagent receives a self-contained prompt that includes:

1. The full text of the `meeting-plan` command (from `.claude/commands/meeting-plan.md`)
2. The specific Google Docs URL to process
3. Instruction to execute **Phase 1 only** (analysis, research, workspace creation, ticket staging)
4. Instruction to **stop after staging files** and report back the workspace path and a summary of action items found

**Subagent prompt template:**

```
You are running a meeting-plan workflow for a single meeting. Follow these instructions exactly.

INPUT: Google Docs link: <URL>

INSTRUCTIONS:
1. Read and follow the meeting-plan command at .claude/commands/meeting-plan.md
2. Use the Google Docs link as your input (fetch via FetchMcpResource with server "user-google-drive" and URI "gdrive:///<document-id>")
3. Execute Phase 1 ONLY:
   - Fetch the document content
   - Create the workspace directory
   - Run meeting analysis (read .claude/commands/meeting-analysis.md)
   - Research unresolved questions (read .claude/commands/meeting-research.md)
   - Create ticket proposals (read .claude/commands/meeting-tickets.md)
   - Stage all files in the workspace
4. STOP after Phase 1. Do NOT create JIRA tickets, send Slack messages, or run TickTick sync.
5. Return a summary containing:
   - Workspace path (workspaces/YYYY-MM-DD/meeting-slug/)
   - Meeting title and date
   - Number of action items found
   - Number of JIRA tickets proposed vs Slack-only items
   - Any critical questions or ambiguities found
```

### Step 3 - Monitor progress

After launching all subagents:
1. Poll each background agent's output file periodically
2. As each agent completes, collect its summary
3. Report incremental progress: "Meeting 2 of 4 complete: <title> - N tickets staged"

### Step 4 - Present consolidated summary

Once all agents complete, present a single summary table:

```markdown
## Batch Meeting Plan Results

| # | Meeting Title | Date | Workspace | Tickets | Slack Items | Status |
|---|---------------|------|-----------|---------|-------------|--------|
| 1 | <title>       | <date> | `workspaces/...` | N | N | Ready for review |
| 2 | <title>       | <date> | `workspaces/...` | N | N | Ready for review |

**Next steps:**
1. Review each meeting's `tickets.md` file in its workspace
2. Edit ticket fields as needed (priority, assignee, parent_id, release, story_points)
3. When ready, run Phase 2 for each meeting individually or confirm all at once
```

### Step 5 - Phase 2 execution (user-triggered)

Phase 2 does NOT run automatically. After the user reviews all workspaces, they can trigger execution by:

- **Individual**: "confirm <workspace-path>" or "create tickets for <meeting-name>"
- **All at once**: "confirm all" or "create all tickets"

For each confirmed meeting, follow the Phase 2 steps from `meeting-plan`:
- Re-read the final `tickets.md`
- Create JIRA tickets via appropriate skill
- Update `analysis.md`
- Generate Slack summary
- Run TickTick sync
- Save workspace

## Error Handling

- If a subagent fails to fetch a Google Docs link, report the error and continue with remaining links
- If a subagent crashes mid-analysis, note which meeting failed and provide the partial workspace path (if created)
- Final summary marks failed meetings as "Failed - <reason>" in the status column

## Notes

- Each subagent runs independently with no shared state between meetings
- Workspace directories follow the standard `workspaces/YYYY-MM-DD/meeting-slug/` convention
- If two meetings share the same date and slug, the standard `-2`, `-3` suffix applies
- All standard `meeting-plan` features apply per-meeting (epic inference, assignee normalization, story point estimation, research filtering)
