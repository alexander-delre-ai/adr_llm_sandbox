---
description: Full meeting workflow - accepts transcript or Gemini summary link, produces meeting analysis with reviewable JIRA ticket plans, then optionally creates actual tickets via MCP integration and sends Slack summary.
---

# /meeting_plan

Accept a meeting transcript or Gemini summary link and produce a full meeting analysis with reviewable JIRA ticket plans, then optionally create actual tickets via MCP integration.

## Input

The meeting content may be provided as:
- **Full transcript**: Complete meeting recording transcript with detailed conversation
- **Gemini/Google Docs link**: Google Docs link to AI-generated meeting notes (fetched via Google Drive MCP and used as analysis source)
- Inline text pasted directly in the message
- A file path - read the file using the Read tool (supports `temp/` directory files)
- A file path that contains a Gemini link inside it (the link is extracted and fetched via Google Drive MCP)

**Input Format Examples:**
- `@temp/meeting-transcript.md` (file path -- read and use as transcript)
- `@temp/meeting-transcript.md gemini summary: https://docs.google.com/document/d/...` (transcript file + Gemini link -- use transcript for analysis, fetch Gemini doc for Slack reference)
- `gemini summary: https://docs.google.com/document/d/.../edit?tab=...` (Gemini link only -- fetch via Google Drive MCP and use as primary analysis source)
- `https://docs.google.com/document/d/.../edit?tab=...` (bare Google Docs URL -- same as above)

If no content is provided, ask: "Please paste the meeting transcript, provide a file path, or share a Google Docs/Gemini link."

**Google Docs / Gemini Link Handling**: When the user provides a Google Docs URL (either directly, via `gemini summary: [URL]`, or embedded inside a transcript file):

1. **Extract the document ID** from the URL. The ID is the segment between `/d/` and the next `/` in the URL (e.g., from `https://docs.google.com/document/d/1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w/edit?tab=t.abc` extract `1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w`).
2. **Fetch the document** using the Google Drive MCP: call `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`. This returns the full document content as markdown.
3. **Determine role based on context**:
   - If the Gemini link is the **only input** (no transcript file or inline text), use the fetched content as the **primary analysis source**.
   - If a transcript file is **also provided**, use the transcript for analysis and store the Gemini link for Slack summary reference. The fetched Gemini content can supplement the analysis if the transcript is sparse.
   - If a transcript file **contains a Gemini link** inside it (e.g., a line like `gemini summary: https://docs.google.com/...`), extract the link, fetch it via Google Drive MCP, and use the transcript text (minus the link line) as the primary source. Store the Gemini link for Slack reference.

**Temp Directory Support**: Files in `temp/` directory will be moved to the meeting workspace after successful analysis (saves processing time by avoiding content duplication).

## Steps

1. Accept the meeting content (transcript, Gemini link, or both) using one of the input methods above
2. **Extract and fetch Google Docs links**: Scan the user message (and transcript file contents, if a file was provided) for Google Docs URLs. For each link found:
   - Extract the document ID from the URL (the segment between `/d/` and the next `/`)
   - Fetch the document content using `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`
   - Store the original URL for Slack summary use
3. **Rename chat window**: Once the meeting title is known (extracted from transcript metadata, Gemini doc title/header, or inferred from content), rename the chat to `YYYY-MM-DD <meeting-title>` (e.g., "2026-03-30 TruckSim Sync"). Use the same title that will become the workspace slug. For temp file inputs without a Google Doc link, use the temp file's name without the extension (e.g., `temp/2026-03-26-vt-ml-meeting.md` becomes "2026-03-26 vt-ml-meeting").
4. **Identify content type and primary source**:
   - If a transcript file or inline text was provided, use that as the primary analysis source
   - If only a Google Docs link was provided (no transcript), use the fetched document content as the primary analysis source
   - If both a transcript and a Google Docs link were provided, use the transcript as primary and the fetched Gemini content as supplementary context
5. Switch to Plan mode so the analysis is collaborative before any artifacts are created
6. **Create workspace directory** immediately using YYYY-MM-DD/meeting-name format
7. **Store Gemini link**: Save the Google Docs URL (if any) to `gemini-link.txt` in the workspace for Slack summary use
8. **Create meeting analysis**: Read and follow `.claude/commands/meeting-analysis.md` to create analysis.md
9. **Create ticket proposals**: Read and follow `.claude/commands/meeting-tickets.md` to create tickets.md
10. **Stage files in workspace**:
   - `workspaces/YYYY-MM-DD/meeting-name/analysis.md` - Complete meeting analysis (context, decisions, themes, questions, action items, prioritized plan)
   - `workspaces/YYYY-MM-DD/meeting-name/tickets.md` - Editable ticket proposals with essential fields (tracking, priority, assignee, parent_id, release, story_points, description)
   - `workspaces/YYYY-MM-DD/meeting-name/transcript.md` - Original meeting transcript
   - `workspaces/YYYY-MM-DD/meeting-name/gemini-link.txt` - Gemini summary URL (if provided) for Slack summary reference
   - **Auto-assign tracking**: Items involving "schedule", "meeting", "coordinate", or "set up" default to "slack" tracking
   - **Single assignee**: Each action item assigned to one person for clear accountability. If multiple people are mentioned for one item (e.g., "Alex and Ashli need to..."), assign to the first person named and note the others in the description field.
11. Present summary with references to staged workspace files

## Review and Execution Phase

After staging files in workspace, ask:

**"I've created the workspace and staged files for your review:**
- **`workspaces/YYYY-MM-DD/meeting-name/analysis.md`** - Complete meeting analysis and plan
- **`workspaces/YYYY-MM-DD/meeting-name/tickets.md`** - Editable JIRA ticket proposals

**Please:**
1. **Review the analysis** for accuracy
2. **Edit the tickets file** as needed (tracking, priority, assignee, parent_id, release, story_points, description)
3. **Set story point estimates** - all story_points default to 0, please update before confirming
4. **Confirm Gemini notes link** (if provided) for Slack summary reference
5. **Type `confirm` or `create tickets`** when ready to create the JIRA tickets and complete the workspace"

**Phase 2 trigger**: Only proceed to Phase 2 when the user sends a message containing `confirm`, `create tickets`, or `/confirm`. Any other reply (questions, edits, comments) keeps the workflow in review mode.

If Phase 2 is triggered, execute using the specialized skills:
- **JIRA Ticket Creation**: Use appropriate skill based on parent_id project space:
  - `.claude/commands/kata-jira-task-creation.md` for KATA-XXXX parent_ids
  - `.claude/commands/avp-jira-task-creation.md` for AVP-XXXX parent_ids
  - **Read final tickets.md file** to get user-edited titles, descriptions, and field values
  - Process tracking field: create JIRA tickets only for "jira" or "both"
  - Apply proper field mappings (P0-P3 priorities, release IDs)
  - Lookup and set assignees from tickets.md (skip if "Unassigned" or lookup fails)
  - Use defaults: assignee="Unassigned", parent_id="KATA-127" (if TBD), release="Release 2026.1" (if TBD), story_points=0 (always default to 0)
  - Auto-format releases: prepend "Release " if only version number provided (e.g., "2025.3" -> "Release 2025.3")
  - **Documentation ticket routing**: A ticket is a documentation ticket if parent_id="KATA-2226" OR if the title/description contains any of these keywords: `document`, `documentation`, `write`, `tutorial`, `guide`, `runbook`, `README`, `SDK setup`, `API doc`
  - **Ticket title validation**: Ensure ticket summaries match the updated action item names from tickets.md after user review
  - **AVP mirrors**: Do **not** create AVP copies by default. Only if the user asks or `tickets.md` sets `avp_mirror: true` on an item (see kata-jira-task-creation command).
- **Slack Summary Generation**: Use `.claude/commands/meeting-slack-summary.md`
  - **Read Gemini link**: Check for `gemini-link.txt` in workspace and pass URL to Slack summary skill
  - Include all action items (Slack-only first, then JIRA tickets)
  - **Include Gemini summary link** (if available from workspace) as reference in Slack message
  - **Slack filtering**: Only include KATA tickets in summaries (exclude AVP mirrors)
  - Send formatted message to AlexD with workspace context
- **TickTick Sync**: Use `.claude/commands/ticktick-sync.md` to sync eligible meeting items
  - Run: `python3 .cursor/skills/ticktick-sync/scripts/sync_meeting_items.py --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md --meeting "<Meeting Title>"`
  - Syncs only Slack-tracked items assigned to AlexD or Unassigned
  - Tasks get short titles (15 words max) with full descriptions in content
- **Workspace Creation**: Use `.claude/commands/meeting-workspace.md`
  - Save complete workspace with all artifacts, JIRA ticket metadata, and TickTick sync results
  - Return workspace path and real ticket URLs for immediate actionability
- **Auto-update user mapping**: If any new Applied attendees were discovered during Slack summary generation, commit the updated `.cursor/skills/meeting-summary/meeting-slack-summary/user-mapping.md`
- **Update analysis.md** (final step): Re-read the final `tickets.md` and update sections 5 (Action Items) and 6 (Prioritized Action Plan + Next Steps) in `analysis.md` with real KATA-XXXX ticket keys and final reviewed content

## Two-Phase Workflow

### Phase 1: Analysis & Planning (Plan Mode)
- **Create workspace directory** immediately for staging files
- Complete meeting analysis with proposed tickets
- **Stage files in workspace** - analysis and editable tickets ready for review
- **Auto-categorize tracking** - scheduling/meeting items default to "slack", others to "jira"
- **Single assignee per item** - one person responsible per action (defaults to "Unassigned"). If multiple people are named for one item, assign to the first person and note others in description.
- **Ask clarifying questions** about unclear action items, priorities, or assignments
- User reviews analysis and edits tickets file directly in workspace
- Collaborative refinement before execution
- **Trigger**: Phase 2 starts only when user sends `confirm`, `create tickets`, or `/confirm`

### Phase 2: Execution (Agent Mode)

Execute in this order:

1. **Re-read tickets.md** to capture any user edits to titles, descriptions, assignments, etc.
2. **Create JIRA tickets**: Read and follow appropriate JIRA creation skill based on project space:
   - `.claude/commands/kata-jira-task-creation.md` for KATA project tickets
   - `.claude/commands/avp-jira-task-creation.md` for AVP project tickets
   - Apply proper field mappings and epic routing (defaults: Unassigned, KATA-127 if TBD, Release 2026.1 if TBD, story_points=0 always)
   - **Validate ticket titles**: Confirm ticket summaries match the action item names from the final edited tickets.md
   - Auto-format release names (prepend "Release " if needed)
   - **Documentation tickets**: A ticket is documentation if parent_id="KATA-2226" OR title/description contains: `document`, `documentation`, `write`, `tutorial`, `guide`, `runbook`, `README`, `SDK setup`, `API doc`
   - Do not create AVP mirrors unless explicitly requested (see kata-jira-task-creation command)
3. **Generate Slack summary**: Read and follow `.claude/commands/meeting-slack-summary.md`
   - Check for `gemini-link.txt` in workspace and include URL in Slack message
   - Include all action items (Slack-only first, then JIRA tickets)
   - Send formatted office hours thread message to AlexD
4. **TickTick Sync**: Run `python3 .cursor/skills/ticktick-sync/scripts/sync_meeting_items.py --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md --meeting "<Meeting Title>"`
   - Syncs Slack-tracked items assigned to AlexD or Unassigned to TickTick "Cursor Sync" project
   - Short titles (15 words max), full descriptions in content body
5. **Save workspace**: Read and follow `.claude/commands/meeting-workspace.md` to create complete workspace with TickTick sync results
   - **Move temp files**: If input was from `temp/` directory, move original file to workspace as transcript.md
6. **Auto-update user mapping**: If new Applied attendees were discovered, update `.cursor/skills/meeting-summary/meeting-slack-summary/user-mapping.md` and commit it with message: `update user-mapping with attendees from <meeting-slug>`
7. **Update analysis.md** (final step): Re-read final `tickets.md` and rewrite sections 5 (Action Items) and 6 (Prioritized Action Plan + Next Steps) with real KATA-XXXX ticket keys and final reviewed content. Provide workspace path and ticket URLs.

## Benefits

- Review before commit: See proposed tickets before creation
- Clarifying questions: Ask about unclear priorities, assignments, or scope
- Collaborative refinement: Adjust tickets based on discussion
- MCP integration: Create real tickets when ready
- Complete automation: Full workflow from review to execution
