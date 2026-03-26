# /meeting_plan

**Mode: Agent**

Accept a meeting transcript or Gemini summary link and produce a full meeting analysis with reviewable JIRA ticket plans, then optionally create actual tickets via MCP integration.

## Input

The meeting content may be provided as:
- **Full transcript**: Complete meeting recording transcript with detailed conversation
- **Gemini summary link**: Google Docs link to AI-generated meeting summary (for reference only, used in Slack summary)
- Inline text pasted directly in the message
- A file path - read the file using the Read tool (supports `temp/` directory files)

**Input Format Examples:**
- `@temp/meeting-transcript.md` (file path)
- `@temp/meeting-transcript.md gemini summary: https://docs.google.com/document/d/...` (transcript + Gemini link)
- `gemini summary: https://docs.google.com/document/d/...` (Gemini link only - ask for transcript)

If no content is provided, ask: "Please paste the meeting transcript or provide a file path."

**Gemini Link Extraction**: When user provides "gemini summary: [URL]" in their message, extract and store this URL for inclusion in the Slack summary. The link is for reference only and not processed for content.

**Temp Directory Support**: The specific temp file referenced in the command input will be copied to the meeting workspace as transcript.md, then the original temp file is deleted after workflow completion. Other files in `temp/` are left untouched.

## Steps

1. Accept the meeting content (transcript) or Gemini summary link using one of the input methods above
2. **Rename chat window**: If input is a temp file, rename the chat window to the temp file's name without the extension (e.g., `temp/2026-03-26-vt-ml-meeting.md` becomes "2026-03-26-vt-ml-meeting")
3. **Extract Gemini link**: If user message contains "gemini summary: [URL]", extract and store this URL for later use in Slack summary
4. **Identify content type**: Determine if input is a full transcript or Gemini summary link (for reference only)
5. **Create workspace directory** immediately using YYYY-MM-DD/meeting-name format
6. **Store Gemini link**: If extracted in step 3, save Gemini summary URL to workspace metadata for Slack summary use
7. **Create meeting analysis**: Read and follow `.cursor/skills/meeting-analysis/SKILL.md` to create analysis.md
8. **Research unresolved questions**: Read and follow `.cursor/skills/meeting-research/SKILL.md` to research each unresolved question from Section 4 of analysis.md
   - Parse each bullet from Section 4 (Unresolved Questions) as a separate question
   - Run the meeting-research skill for each question with the workspace path as context
   - Compile all results into a single `research.md` in the workspace (batch format from the skill)
9. **Pause only if critical**: If there are crucial ambiguities (e.g., completely unclear assignees, conflicting action items, missing context that prevents ticket creation), pause and ask the user. Otherwise, proceed automatically.
10. **Create ticket proposals**: Read and follow `.cursor/skills/meeting-tickets/SKILL.md` to create tickets.md
11. **Stage files in workspace**:
    - `workspaces/YYYY-MM-DD/meeting-name/analysis.md` - Complete meeting analysis (context, decisions, themes, questions, action items, prioritized plan)
    - `workspaces/YYYY-MM-DD/meeting-name/research.md` - Research findings for unresolved questions from analysis
    - `workspaces/YYYY-MM-DD/meeting-name/tickets.md` - Editable ticket proposals with essential fields (tracking, priority, assignee, parent_id, release, story_points, description)
    - `workspaces/YYYY-MM-DD/meeting-name/transcript.md` - Original meeting transcript
    - `workspaces/YYYY-MM-DD/meeting-name/gemini-link.txt` - Gemini summary URL (if provided) for Slack summary reference
    - **Auto-assign tracking**: Items involving "schedule", "meeting", "coordinate", or "set up" default to "slack" tracking
    - **Single assignee**: Each action item assigned to one person for clear accountability
12. Present summary with references to staged workspace files

## Review and Execution Phase

After staging files in workspace, automatically proceed to execution. Present a brief summary of staged files and immediately continue to Phase 2:

Execute using the specialized skills:
- **JIRA Ticket Creation**: Use appropriate skill based on parent_id project space:
  - `.cursor/skills/kata-jira-task-creation/SKILL.md` for KATA-XXXX parent_ids
  - `.cursor/skills/avp-jira-task-creation/SKILL.md` for AVP-XXXX parent_ids
  - **Read final tickets.md file** to get user-edited titles, descriptions, and field values
  - Process tracking field: create JIRA tickets only for "jira" or "both"
  - Apply proper field mappings (P0-P3 priorities, release IDs)
  - Lookup and set assignees from tickets.md (skip if "Unassigned" or lookup fails)
  - Use defaults: assignee="Unassigned", parent_id="KATA-127" (if TBD), release="Release 2026.1" (if TBD), story_points=0 (always default to 0)
  - Auto-format releases: prepend "Release " if only version number provided (e.g., "2025.3" → "Release 2025.3")
  - **Documentation ticket routing**: Any tickets with parent_id="KATA-2226" are documentation tickets
  - **Ticket title validation**: Ensure ticket summaries match the updated action item names from tickets.md after user review
  - **Create AVP mirrors**: Automatically create AVP copies for documentation tickets (parent: AVP-5477, engagement: "Komatsu")
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
- **Research unresolved questions** - search Slack, Confluence, JIRA, and codebase for answers to open questions from analysis Section 4
- **Stage files in workspace** - analysis, research, and editable tickets ready for review
- **Auto-categorize tracking** - scheduling/meeting items default to "slack", others to "jira"
- **Single assignee per item** - ensure clear accountability with one person responsible per action (defaults to "Unassigned")
- **Pause only if critical** - only stop to ask the user if there are crucial ambiguities that block ticket creation (e.g., conflicting action items, completely missing context). Otherwise proceed automatically.

### Phase 2: Execution
- Automatically proceeds after Phase 1 (no manual confirmation required)
- Process tracking preferences (JIRA tickets vs Slack-only items)
- **Create JIRA tickets**: Read and follow appropriate JIRA creation skill based on project space:
  - `.cursor/skills/kata-jira-task-creation/SKILL.md` for KATA project tickets
  - `.cursor/skills/avp-jira-task-creation/SKILL.md` for AVP project tickets
  - Apply proper field mappings and epic routing (defaults: Unassigned, KATA-127 if TBD, Release 2026.1 if TBD, story_points=0 always)
  - **Validate ticket titles**: Confirm ticket summaries match the action item names from the final edited tickets.md
  - Auto-format release names (prepend "Release " if needed)
  - Create AVP mirrors for documentation tickets (parent: AVP-5477, engagement: "Komatsu")
- **Update analysis.md**: Re-read the final `tickets.md` and rewrite sections 5 (Action Items) and 6 (Prioritized Action Plan + Next Steps) in `analysis.md` to reflect the user-reviewed ticket content
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

- ✅ **Automatic progression**: Runs straight through analysis, tickets, and execution without pausing
- ✅ **Smart interrupts**: Only pauses for crucial ambiguities that block ticket creation
- ✅ **Post-execution review**: Workspace files available for review and adjustment after completion
- ✅ **MCP integration**: Creates real tickets automatically
- ✅ **Complete automation**: Full end-to-end workflow from transcript to tickets and Slack summary
