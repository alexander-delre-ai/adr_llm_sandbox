# /meeting_plan

**Mode: Agent**

Accept a Google Docs link or temp file transcript and produce a full meeting analysis with reviewable JIRA ticket plans, then optionally create actual tickets via MCP integration.

## Input

The meeting content may be provided as:
- **Google Docs link**: Gemini-generated meeting notes or manually written doc (fetched via Google Drive MCP)
- **Temp file**: A file path in `temp/` containing a full transcript (read via the Read tool)

**Input Format Examples:**
- `gemini summary: https://docs.google.com/document/d/.../edit?tab=...` (Gemini link with prefix)
- `https://docs.google.com/document/d/.../edit?tab=...` (bare Google Docs URL)
- `@temp/meeting-transcript.md` (temp file path)

If no content is provided, ask: "Please share a Google Docs link to the meeting notes, or provide a temp file path."

**Google Docs Link Handling**:

1. **Extract the document ID** from the URL. The ID is the segment between `/d/` and the next `/` in the URL (e.g., from `https://docs.google.com/document/d/1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w/edit?tab=t.abc` extract `1XBcQmsTCAU0mHwVhY7b0q_2EKxlmoLoMvmeRZtq_J8w`).
2. **Fetch the document** using the Google Drive MCP: call `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`. This returns the full document content as markdown.
3. Use the fetched content as the **primary analysis source**. The Google Doc link is also stored in the workspace for Slack summary and doc sharing use.

**Temp File Handling**: Read the file using the Read tool. Use its content as the primary analysis source. The temp file name (without extension) is used to derive the meeting title if no other title is available (e.g., `temp/2026-03-26-vt-ml-meeting.md` becomes "vt-ml-meeting").

## Steps

1. Accept the input from the user message (Google Docs link or temp file path)
2. **Fetch meeting content**:
   - **Google Docs link**: Parse the URL to extract the document ID (segment between `/d/` and the next `/`). Fetch the document content using `FetchMcpResource` with server `user-google-drive` and URI `gdrive:///<document-id>`. Store the original URL for Slack summary and doc sharing use.
   - **Temp file**: Read the file content using the Read tool. Use it as the primary analysis source.
3. **Create workspace directory** using YYYY-MM-DD/meeting-name format. Before creating, check if `workspaces/YYYY-MM-DD/meeting-name/` already exists. If it does, ask the user: "A workspace already exists at `workspaces/YYYY-MM-DD/meeting-name/`. Overwrite it, or create a versioned copy (e.g., `meeting-name-v2`)?" Proceed based on the answer.
5. **Store Google Doc link**: If a Google Docs URL was provided, save it to `gemini-link.txt` in the workspace for Slack summary and doc sharing use
5a. **Create transcript.md** in the workspace:
    - **If input was a Google Docs link**: Write a single-line file containing just the Google Docs URL (a reference link, not the fetched content)
    - **If input was a temp file**: Copy the temp file contents to `transcript.md`, then delete the original temp file. Other files in `temp/` are left untouched.
6. **Create meeting analysis**: Read and follow `.cursor/skills/meeting-analysis/SKILL.md` to create analysis.md
7. **Research unresolved questions**: Read and follow `.cursor/skills/meeting-research/SKILL.md`, but first classify each question from Section 4 of analysis.md:
   - **Research** (run through meeting-research skill): Questions about architecture, implementation, technical decisions, prior art, existing tickets, design patterns, or system behavior
   - **Skip** (note in research.md only): Questions about scheduling, coordination, "who will attend", meeting logistics, or items requiring human action (e.g., "Who from Komatsu defines the manufacturing workflows?")
   - **Run research in parallel**: Launch all "Research" classified questions concurrently using parallel subagent invocations (one per question, each running the meeting-research skill with the workspace path as context). Collect all results when complete.
   - For skipped questions: add a note in research.md: "Skipped -- coordination/scheduling question, not researchable via Slack/Confluence/JIRA."
   - Compile all results (parallel + skipped) into a single `research.md` in the workspace (batch format from the skill)
8. **Pause only if critical during analysis**: If there are crucial ambiguities (e.g., completely unclear assignees, conflicting action items, missing context that prevents ticket proposal generation), pause and ask the user. Otherwise, proceed automatically through analysis and ticket staging.
9. **Create ticket proposals**: Read and follow `.cursor/skills/meeting-tickets/SKILL.md` to create tickets.md. The tickets skill will:
    - Infer `parent_id` from meeting title via `.cursor/skills/meeting-tickets/meeting-epic-mapping.json`
    - Normalize assignee names via `.cursor/skills/meeting-slack-summary/user-mapping.md`
    - Estimate story points from description heuristics
    - Infer release from timeline mentions via `.cursor/skills/kata-jira-task-creation/release-mapping.json`
    - Suggest ticket groupings for related items
10. **Stage files in workspace**:
    - `workspaces/YYYY-MM-DD/meeting-name/analysis.md` - Complete meeting analysis (context, decisions, themes, questions, action items, prioritized plan)
    - `workspaces/YYYY-MM-DD/meeting-name/research.md` - Research findings for unresolved questions from analysis
    - `workspaces/YYYY-MM-DD/meeting-name/tickets.md` - Editable ticket proposals with smart defaults and suggested groupings
    - `workspaces/YYYY-MM-DD/meeting-name/transcript.md` - Google Docs URL (if link input) or full transcript content (if temp file input)
    - `workspaces/YYYY-MM-DD/meeting-name/gemini-link.txt` - Google Docs URL for Slack summary and doc sharing reference (only if link input)
    - **Auto-assign tracking**: Conversations and follow-ups default to "slack"; technical work defaults to "jira"
    - **Single assignee**: Each action item assigned to one person (normalized to canonical name)
11. **Present summary and wait for user review**:
    - Generate an interactive canvas (via browser MCP canvas tool) that renders all tickets from `tickets.md` in a compact review table. Columns: ticket title, assignee, priority, tracking (jira/slack/both), epic, release, story points. The canvas is read-only and informational; edits are still made directly in `tickets.md`.
    - Present the canvas alongside references to the staged workspace files.
    - Explicitly tell the user to review the canvas overview, edit `tickets.md` if changes are needed, then confirm when ready to proceed.

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
- **Share Google Doc with participants**: If a Google Docs/Gemini link was provided, grant access to the document for all meeting attendees and action item assignees:
  - **Skip if no link**: Only run this step when `gemini-link.txt` exists in the workspace
  - **Extract document ID**: Parse the Google Docs URL from `gemini-link.txt` to get the file ID (segment between `/d/` and the next `/`)
  - **Build recipient list**: Collect a unique set of people from:
    1. All attendees listed in analysis.md (Section 1)
    2. All action item assignees from the final tickets.md
  - **Resolve email addresses**: For each person in the recipient list:
    - Look up their email in `.cursor/skills/meeting-slack-summary/user-mapping.md`
    - For Komatsu users, use the `firstname.lastname@global.komatsu` pattern
    - For Applied users, use their known email (e.g., `timothy.kyung@applied.co`)
    - If email is not in `user-mapping.md`, use `slack_search_users` to find the person's Slack user ID by name, then `slack_read_user_profile` to retrieve their email. If found, update `user-mapping.md` with the discovery.
    - Skip anyone whose email still cannot be determined
  - **Confirm recipient list**: Present the resolved recipient list (name + email) to the user and wait for explicit approval before granting access. The user may remove people or adjust the list.
  - **Grant access**: After confirmation, for each approved email, call Google Drive MCP `shareFile` with:
    - `fileId`: the extracted document ID
    - `emailAddress`: the person's email
    - `role`: `"writer"`
    - `sendNotificationEmail`: `true` (so they receive a link in their inbox)
  - **Log results**: Note in the workspace summary how many participants were granted access and any that were skipped (no email found)
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
- **Smart research filtering** - classify unresolved questions as technical (research) or coordination (skip), only research actionable questions. Research questions run in parallel via concurrent subagents for speed.
- **Epic inference** - match meeting title against `.cursor/skills/meeting-tickets/meeting-epic-mapping.json` for default parent_id
- **Assignee normalization** - resolve names from meeting notes to canonical names via `user-mapping.md`
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
- **Share Google Doc with participants**: If `gemini-link.txt` exists in workspace, resolve emails from `user-mapping.md` (with Slack profile fallback for unknowns), present recipient list for user confirmation, then grant writer access via `shareFile` MCP with notification emails
- **TickTick Sync**: Run `python3 .cursor/skills/ticktick-sync/scripts/sync_meeting_items.py --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md --meeting "<Meeting Title>"`
  - Syncs Slack-tracked items assigned to AlexD or Unassigned to TickTick "Cursor Sync" project
  - Short titles (15 words max), full descriptions in content body
- **Save workspace**: Read and follow `.cursor/skills/meeting-workspace/SKILL.md` to create complete workspace with TickTick sync results
- Provide immediate actionability with workspace path and ticket URLs

## Benefits

- **User-gated execution**: Completes analysis and ticket proposals automatically, then pauses for user review before creating JIRA tickets
- **Smart defaults**: Epic, release, story points, and tracking inferred from meeting context
- **Assignee normalization**: Consistent names across tickets and JIRA lookups
- **Duplicate detection**: Auto-skips tickets that already exist in JIRA
- **Smart research**: Only researches technical questions, skips coordination items
- **Ticket grouping**: Suggests related tickets that could share a parent
- **Failure recovery**: Saves JIRA payloads to `jira-payloads.json` for retry on failure
- **Auto-share meeting notes**: Grants Google Doc access to all attendees and assignees so they get notified with a link
- **Complete automation**: Full end-to-end workflow from Google Doc to tickets, Slack, and TickTick
