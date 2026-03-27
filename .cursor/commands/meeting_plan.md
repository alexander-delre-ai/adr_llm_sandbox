# /meeting_plan

**Mode: Agent**

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

**Temp Directory Support**: The specific temp file referenced in the command input will be copied to the meeting workspace as transcript.md, then the original temp file is deleted after workflow completion. Other files in `temp/` are left untouched.

## Steps

1. Accept the meeting content (transcript, Gemini link, or both) using one of the input methods above
2. **Rename chat window**: If input is a temp file, rename the chat window to the temp file's name without the extension (e.g., `temp/2026-03-26-vt-ml-meeting.md` becomes "2026-03-26-vt-ml-meeting")
3. **Extract and fetch Google Docs links**: Scan the user message (and transcript file contents, if a file was provided) for Google Docs URLs. For each link found:
   - Extract the document ID from the URL (the segment between `/d/` and the next `/`)
   - Fetch the document content using `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`
   - Store the original URL for Slack summary use
4. **Identify content type and primary source**:
   - If a transcript file or inline text was provided, use that as the primary analysis source
   - If only a Google Docs link was provided (no transcript), use the fetched document content as the primary analysis source
   - If both a transcript and a Google Docs link were provided, use the transcript as primary and the fetched Gemini content as supplementary context
5. **Create workspace directory** immediately using YYYY-MM-DD/meeting-name format
6. **Store Gemini link**: Save the Google Docs URL (if any) to `gemini-link.txt` in the workspace for Slack summary use
7. **Create meeting analysis**: Read and follow `.cursor/skills/meeting-analysis/SKILL.md` to create analysis.md
8. **Research unresolved questions**: Read and follow `.cursor/skills/meeting-research/SKILL.md`, but first classify each question from Section 4 of analysis.md:
   - **Research** (run through meeting-research skill): Questions about architecture, implementation, technical decisions, prior art, existing tickets, design patterns, or system behavior
   - **Skip** (note in research.md only): Questions about scheduling, coordination, "who will attend", meeting logistics, or items requiring human action (e.g., "Who from Komatsu defines the manufacturing workflows?")
   - For researched questions: run the meeting-research skill with the workspace path as context
   - For skipped questions: add a note in research.md: "Skipped -- coordination/scheduling question, not researchable via Slack/Confluence/JIRA."
   - Compile all results into a single `research.md` in the workspace (batch format from the skill)
9. **Pause only if critical during analysis**: If there are crucial ambiguities (e.g., completely unclear assignees, conflicting action items, missing context that prevents ticket proposal generation), pause and ask the user. Otherwise, proceed automatically through analysis and ticket staging.
10. **Create ticket proposals**: Read and follow `.cursor/skills/meeting-tickets/SKILL.md` to create tickets.md. The tickets skill will:
    - Infer `parent_id` from meeting title via `.cursor/skills/meeting-tickets/meeting-epic-mapping.json`
    - Normalize assignee names via `.cursor/skills/meeting-slack-summary/user-mapping.md`
    - Estimate story points from description heuristics
    - Infer release from timeline mentions via `.cursor/skills/kata-jira-task-creation/release-mapping.json`
    - Suggest ticket groupings for related items
11. **Stage files in workspace**:
    - `workspaces/YYYY-MM-DD/meeting-name/analysis.md` - Complete meeting analysis (context, decisions, themes, questions, action items, prioritized plan)
    - `workspaces/YYYY-MM-DD/meeting-name/research.md` - Research findings for unresolved questions from analysis
    - `workspaces/YYYY-MM-DD/meeting-name/tickets.md` - Editable ticket proposals with smart defaults and suggested groupings
    - `workspaces/YYYY-MM-DD/meeting-name/transcript.md` - Original meeting transcript
    - `workspaces/YYYY-MM-DD/meeting-name/gemini-link.txt` - Gemini summary URL (if provided) for Slack summary reference
    - **Auto-assign tracking**: Conversations and follow-ups default to "slack"; technical work defaults to "jira"
    - **Single assignee**: Each action item assigned to one person (normalized to canonical name)
12. **Present summary and wait for user review**: Present a summary with references to staged workspace files. Explicitly tell the user to review and edit `tickets.md`, then confirm when ready to proceed.

## Review and Execution Phase

**IMPORTANT**: After staging files in workspace, do NOT automatically proceed to execution. Present a summary of staged files and **wait for the user to review and confirm `tickets.md`** before creating any JIRA tickets. The user may edit ticket titles, descriptions, priorities, tracking types, assignees, or remove items entirely. Only proceed to Phase 2 after the user explicitly confirms (e.g., "looks good", "go ahead", "create tickets", "confirmed").

Execute using the specialized skills:
- **Duplicate detection**: Before creating each JIRA ticket, search for existing open tickets with similar summary text under the same epic:
  - Use `searchJiraIssuesUsingJql` with: `project = KATA AND parent = <epic> AND status != Done AND status != Closed AND summary ~ "<key terms>"`
  - If a match is found (same epic, open status, similar title), auto-skip that ticket and log it in a `## Skipped Duplicates` section appended to `tickets.md` with the matching JIRA key and link
  - No user prompt needed -- skip silently and report all skips at the end
- **Generate JIRA payloads**: Before creating tickets, write `jira-payloads.json` to the workspace containing the full MCP call payload for each ticket (tool name, arguments, all field values). Each entry starts with `"status": "pending"`.
- **JIRA Ticket Creation**: Use appropriate skill based on parent_id project space:
  - `.cursor/skills/kata-jira-task-creation/SKILL.md` for KATA-XXXX parent_ids
  - `.cursor/skills/avp-jira-task-creation/SKILL.md` for AVP-XXXX parent_ids
  - **Read final tickets.md file** to get user-edited titles, descriptions, and field values
  - Process tracking field: create JIRA tickets only for "jira" or "both"
  - Apply proper field mappings (P0-P3 priorities, release IDs)
  - Lookup and set assignees from tickets.md (skip if "Unassigned" or lookup fails)
  - Use defaults: assignee="Unassigned", parent_id="KATA-127" (if TBD), release="Release 2026.1" (if TBD), story_points=0 (always default to 0)
  - Auto-format releases: prepend "Release " if only version number provided (e.g., "2025.3" -> "Release 2025.3")
  - **Documentation ticket routing**: Any tickets with parent_id="KATA-2226" are documentation tickets
  - **Ticket title validation**: Ensure ticket summaries match the updated action item names from tickets.md after user review
  - **Create AVP mirrors**: Automatically create AVP copies for documentation tickets (parent: AVP-5477, engagement: "Komatsu")
  - **On success**: Update the ticket's entry in `jira-payloads.json` with `"status": "created"`, the JIRA key, and URL
  - **On failure**: Update the ticket's entry with `"status": "failed"` and the error message. Continue creating remaining tickets.
  - **After all tickets**: If any failed, note in the output: "N ticket(s) failed. Payloads saved to `jira-payloads.json` for manual creation or retry."
- **Update analysis.md**: Re-read the final `tickets.md` and update sections 5 (Action Items) and 6 (Prioritized Action Plan + Next Steps) in `analysis.md` to match the final reviewed ticket content
- **Slack Summary Generation**: Use `.cursor/skills/meeting-slack-summary/SKILL.md`
  - **Read Gemini link**: Check for `gemini-link.txt` in workspace and pass URL to Slack summary skill
  - Include all action items (Slack-only first, then JIRA tickets)
  - **Include Gemini summary link** (if available from workspace) as reference in Slack message
  - **Slack filtering**: Only include KATA tickets in summaries (exclude AVP mirrors)
  - Send formatted message to AlexD with workspace context
- **TickTick Sync**: Use `.cursor/skills/ticktick-sync` to sync eligible meeting items
  - Run: `python3 .cursor/skills/ticktick-sync/scripts/sync_meeting_items.py --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md --meeting "<Meeting Title>"`
  - Syncs only Slack-tracked items assigned to AlexD or Unassigned
  - Tasks get short titles (15 words max) with full descriptions in content
- **Workspace Creation**: Use `.cursor/skills/meeting-workspace/SKILL.md`
  - Save complete workspace with all artifacts, JIRA ticket metadata, and TickTick sync results
  - Return workspace path and real ticket URLs for immediate actionability

## Two-Phase Workflow

### Phase 1: Analysis & Planning
- **Create workspace directory** immediately for staging files
- Complete meeting analysis with proposed tickets
- **Smart research filtering** - classify unresolved questions as technical (research) or coordination (skip), only research actionable questions
- **Epic inference** - match meeting title against `.cursor/skills/meeting-tickets/meeting-epic-mapping.json` for default parent_id
- **Assignee normalization** - resolve transcript names to canonical names via `user-mapping.md`
- **Story point estimation** - estimate from description heuristics (0.2-2 range, default 0.5)
- **Release inference** - map timeline mentions to releases via `release-mapping.json`
- **Auto-categorize tracking** - conversations/follow-ups default to "slack"; technical work defaults to "jira"
- **Ticket grouping suggestions** - identify related tickets and suggest groupings at bottom of tickets.md
- **Single assignee per item** - ensure clear accountability with one person responsible per action
- **Pause only if critical during Phase 1** - only stop to ask the user if there are crucial ambiguities that block ticket proposal generation. Otherwise proceed automatically through analysis and ticket staging.
- **Always pause between Phase 1 and Phase 2** - present staged files summary and wait for user to review and confirm `tickets.md` before any JIRA ticket creation

### Phase 2: Execution
- **Requires explicit user confirmation** before proceeding -- user must review and approve `tickets.md` first
- **Duplicate detection** - search JIRA for existing open tickets with similar titles under the same epic; auto-skip duplicates
- **Generate JIRA payloads** - write `jira-payloads.json` with full MCP payloads before creating tickets
- **Create JIRA tickets**: Read and follow appropriate JIRA creation skill based on project space:
  - `.cursor/skills/kata-jira-task-creation/SKILL.md` for KATA project tickets
  - `.cursor/skills/avp-jira-task-creation/SKILL.md` for AVP project tickets
  - Apply proper field mappings and epic routing
  - **Validate ticket titles**: Confirm ticket summaries match the action item names from the final edited tickets.md
  - Auto-format release names (prepend "Release " if needed)
  - Create AVP mirrors for documentation tickets (parent: AVP-5477, engagement: "Komatsu")
  - **Failure recovery**: Update `jira-payloads.json` with creation status (created/failed); continue on failure
- **Update analysis.md**: Re-read the final `tickets.md` and rewrite sections 5 (Action Items) and 6 (Prioritized Action Plan + Next Steps) in `analysis.md` to reflect the final ticket content
- **Generate Slack summary**: Read and follow `.cursor/skills/meeting-slack-summary/SKILL.md`
  - **Read Gemini link**: Check for `gemini-link.txt` in workspace and include URL in Slack message
  - **Include Gemini notes link** (if available from workspace) as reference in Slack message
  - Include all action items (Slack-only first, then JIRA tickets)
  - Send formatted office hours thread message to AlexD
- **TickTick Sync**: Run `python3 .cursor/skills/ticktick-sync/scripts/sync_meeting_items.py --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md --meeting "<Meeting Title>"`
  - Syncs Slack-tracked items assigned to AlexD or Unassigned to TickTick "Cursor Sync" project
  - Short titles (15 words max), full descriptions in content body
- **Save workspace**: Read and follow `.cursor/skills/meeting-workspace/SKILL.md` to create complete workspace with TickTick sync results
- **Clean up temp file**: If input was a specific file from `temp/`, copy that file to workspace as transcript.md, then delete only that temp file (do not touch other files in `temp/`)
- Provide immediate actionability with workspace path and ticket URLs

## Benefits

- **User-gated execution**: Completes analysis and ticket proposals automatically, then pauses for user review before creating JIRA tickets
- **Smart defaults**: Epic, release, story points, and tracking inferred from meeting context
- **Assignee normalization**: Consistent names across tickets and JIRA lookups
- **Duplicate detection**: Auto-skips tickets that already exist in JIRA
- **Smart research**: Only researches technical questions, skips coordination items
- **Ticket grouping**: Suggests related tickets that could share a parent
- **Failure recovery**: Saves JIRA payloads to `jira-payloads.json` for retry on failure
- **Complete automation**: Full end-to-end workflow from transcript to tickets, Slack, and TickTick
