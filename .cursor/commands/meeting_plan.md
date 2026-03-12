# /meeting_plan

**Mode: Plan**

Accept a meeting transcript or Gemini summary and produce a full meeting analysis with reviewable JIRA ticket plans, then optionally create actual tickets via MCP integration.

## Input

The meeting content may be provided as:
- **Full transcript**: Complete meeting recording transcript with detailed conversation
- **Gemini summary**: AI-generated meeting summary with key points, decisions, and action items
- Inline text pasted directly in the message
- A file path - read the file using the Read tool (supports `temp/` directory files)
- A URL - fetch using the appropriate fetch tool

If no content is provided, ask: "Please paste the meeting transcript/summary or provide a file path."

**Temp Directory Support**: Files in `temp/` directory will be moved to the meeting workspace after successful analysis (saves processing time by avoiding content duplication).

## Steps

1. Accept the meeting content (transcript or Gemini summary) using one of the input methods above
2. **Identify content type**: Determine if input is a full transcript or Gemini summary
3. Switch to Plan mode so the analysis is collaborative before any artifacts are created
4. **Create workspace directory** immediately using meeting title and date
5. **Create meeting analysis**: Read and follow `.cursor/skills/meeting-analysis/SKILL.md` to create analysis.md
6. **Create ticket proposals**: Read and follow `.cursor/skills/meeting-tickets/SKILL.md` to create tickets.md
7. **Stage files in workspace**:
   - `workspaces/<meeting-slug>/analysis.md` - Complete meeting analysis (context, decisions, themes, questions, action items, prioritized plan)
   - `workspaces/<meeting-slug>/tickets.md` - Editable ticket proposals with essential fields (tracking, priority, assignee, parent_id, release, story_points, description)
   - **Auto-assign tracking**: Items involving "schedule", "meeting", "coordinate", or "set up" default to "slack" tracking
   - **Single assignee**: Each action item assigned to one person for clear accountability
8. Present summary with references to staged workspace files

## Review and Execution Phase

After staging files in workspace, ask: 

**"I've created the workspace and staged files for your review:**
- **`workspaces/<meeting-slug>/analysis.md`** - Complete meeting analysis and plan
- **`workspaces/<meeting-slug>/tickets.md`** - Editable JIRA ticket proposals

**Please:**
1. **Review the analysis** for accuracy
2. **Edit the tickets file** as needed (tracking, priority, assignee, parent_id, release, story_points, description)
3. **Provide Gemini notes link** (if available) for Slack summary
4. **Confirm when ready** to create the JIRA tickets and complete the workspace"

If confirmed, execute Step 6 with MCP integration:
- **Read final tickets.md file** to get user-edited titles, descriptions, and field values
- Process tracking field: create JIRA tickets only for "jira" or "both", include all items in Slack summary
- Create actual JIRA tickets via MCP server using **edited content from tickets.md**
- Apply proper field mappings (P0-P3 priorities, release IDs)
- Lookup and set assignees from tickets.md (skip if "Unassigned" or lookup fails)
- Use defaults: assignee="Unassigned", parent_id="KATA-127" (if TBD), release="Release 2026.1" (if TBD), story_points=0 if not specified
- Auto-format releases: prepend "Release " if only version number provided (e.g., "2025.3" → "Release 2025.3")
- Route documentation tickets to KATA-2226 automatically
- Include MCP creation tracking
- Return real ticket URLs and complete workspace

## Two-Phase Workflow

### Phase 1: Analysis & Planning (Plan Mode)
- **Create workspace directory** immediately for staging files
- Complete meeting analysis with proposed tickets
- **Stage files in workspace** - analysis and editable tickets ready for review
- **Auto-categorize tracking** - scheduling/meeting items default to "slack", others to "jira"
- **Single assignee per item** - ensure clear accountability with one person responsible per action (defaults to "Unassigned")
- **Ask clarifying questions** about unclear action items, priorities, or assignments
- User reviews analysis and edits tickets file directly in workspace
- Collaborative refinement before execution

### Phase 2: Execution (Agent Mode)  
- **Re-read tickets.md** to capture any user edits to titles, descriptions, assignments, etc.
- Process tracking preferences (JIRA tickets vs Slack-only items)
- Create actual JIRA tickets via MCP integration using **final edited content**
- Apply proper field mappings and epic routing (defaults: Unassigned, KATA-127 if TBD, Release 2026.1 if TBD, story_points=0)
- Auto-format release names (prepend "Release " if needed)
- Save complete workspace in `workspaces/` within current repo
- **Move temp files**: If input was from `temp/` directory, move original file to workspace
- **Request Gemini notes link** (if not already provided) before generating Slack summary
- Generate office hours Slack thread message (includes all items and Gemini link if provided)
- Provide immediate actionability

## Benefits

- ✅ **Review before commit**: See proposed tickets before creation
- ✅ **Clarifying questions**: Ask about unclear priorities, assignments, or scope
- ✅ **Collaborative refinement**: Adjust tickets based on discussion
- ✅ **MCP integration**: Create real tickets when ready
- ✅ **Complete automation**: Full workflow from review to execution
