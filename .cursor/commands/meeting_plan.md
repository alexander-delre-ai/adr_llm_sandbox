# /meeting_plan

**Mode: Plan**

Accept a meeting transcript and produce a full meeting analysis with reviewable JIRA ticket plans, then optionally create actual tickets via MCP integration.

## Input

The transcript may be provided as:
- Inline text pasted directly in the message
- A file path - read the file using the Read tool
- A URL - fetch using the appropriate fetch tool

If no transcript is provided, ask: "Please paste the meeting transcript or provide a file path."

## Steps

1. Accept the transcript using one of the input methods above
2. Switch to Plan mode so the analysis is collaborative before any artifacts are created
3. Read and follow `.cursor/skills/meeting-analysis-and-planning/SKILL.md` - execute through Step 7 (analysis and ticket planning)
4. Return the full analysis with **proposed** JIRA tickets for review

## Review and Execution Phase

After presenting the analysis, ask: 

**"Would you like me to create these JIRA tickets? If yes, please confirm:**
- **Project space** (KATA or AVP)
- **Epic ID** (or I'll route docs to KATA-2226)  
- **Release** (e.g., Release 26.1)
- Any **modifications** to the proposed tickets"

If confirmed, execute Step 6 with MCP integration:
- Create actual JIRA tickets via MCP server
- Apply proper field mappings (P0-P3 priorities, release IDs)
- Route documentation tickets to KATA-2226 automatically
- Include MCP creation tracking
- Return real ticket URLs and complete workspace

## Two-Phase Workflow

### Phase 1: Analysis & Planning (Plan Mode)
- Complete meeting analysis with proposed tickets
- **Ask clarifying questions** about unclear action items, priorities, or assignments
- User reviews and approves/modifies ticket plans
- Collaborative refinement before execution

### Phase 2: Execution (Agent Mode)  
- Create actual JIRA tickets via MCP integration
- Apply proper field mappings and epic routing
- Save complete workspace in `workspaces/` within current repo
- Generate office hours Slack thread message
- Provide immediate actionability

## Benefits

- ✅ **Review before commit**: See proposed tickets before creation
- ✅ **Clarifying questions**: Ask about unclear priorities, assignments, or scope
- ✅ **Collaborative refinement**: Adjust tickets based on discussion
- ✅ **MCP integration**: Create real tickets when ready
- ✅ **Complete automation**: Full workflow from review to execution
