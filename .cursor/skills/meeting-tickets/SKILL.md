---
name: meeting-tickets
description: Creates editable tickets.md file from meeting action items with proper tracking categorization, defaults, and YAML format. Use after meeting analysis to generate reviewable ticket proposals.
---

# Meeting Tickets

Converts meeting action items into editable tickets.md file with proper tracking categorization, field defaults, and clean YAML format for user review and editing.

## Input Requirements

- **Action items list**: From meeting analysis (Step 5 output)
- **Meeting metadata**: Title, date for file headers
- **Output location**: Directory path where tickets.md should be created (format: workspaces/YYYY-MM-DD-meeting-name/)

## Workflow

### Step 1 - Categorize tracking types

For each action item, determine tracking type:

**Auto-assign to "slack":**
- Items involving "schedule", "meeting", "coordinate", "set up"
- Coordination and planning tasks
- Administrative follow-ups

**Auto-assign to "jira":**
- Technical development work
- Research and analysis tasks
- Documentation creation
- Implementation work

### Step 2 - Apply field defaults

For each action item, set these defaults:
- **tracking**: Based on categorization above
- **priority**: Map from analysis priority (High→P1, Medium→P2, Low→P3)
- **assignee**: "Unassigned" (single person per item)
- **parent_id**: "TBD" (will become KATA-127 if unchanged)
- **release**: "TBD" (will become Release 2026.1 if unchanged)
- **story_points**: 0 (always default to 0)
- **description**: Clean summary from action item

### Step 3 - Format action item titles

- **No numbering**: Do not prefix headings with "Action Item 1:", "Action Item 2:", etc.
- **Sentence case**: Use natural sentence case for headings (e.g., "Follow up on build system documentation"), not Title Case

### Step 4 - Generate YAML format

Create clean YAML blocks for each action item:

```yaml
tracking: jira
priority: P1
assignee: Unassigned
parent_id: TBD
release: TBD
story_points: 0
description: Clear description of the work to be done.
```

## Output Format

Create `tickets.md` file with this structure:

```markdown
# Action Items: <Meeting Title> (<Date>)

## Instructions
Edit the fields below as needed. When ready, confirm with the agent to create the action items.

**Field Guide:**

- **tracking**: "jira" (create JIRA ticket + include in Slack), "slack" (Slack summary only, no JIRA ticket), "both" (same as jira)
  - Auto-assigned: Items involving scheduling/meetings default to "slack", others to "jira"
- **priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **assignee**: Single person responsible for the action item (one assignee per item) - defaults to "Unassigned"
- **parent_id**: Epic ID (KATA-XXXX or AVP-XXXX format) - leave as "TBD" to use default "KATA-127"
- **release**: Target release - leave as "TBD" to use default "Release 2026.1". Can use short format (e.g., "2025.3" will become "Release 2025.3")
- **story_points**: 0.2 (1 day), 0.5 (2.5 days), 1 (1 week), 2 (2 weeks), 3 (3 weeks), 5 (5 weeks), 8 (8 weeks) - always defaults to 0
- **description**: Brief summary of the work

---

## [Action item title in sentence case]

```yaml
tracking: [auto-assigned]
priority: [mapped from analysis]
assignee: Unassigned
parent_id: TBD
release: TBD
story_points: 0
description: [Clean description]
```

[Continue for each action item - no numbering, sentence case headings]
```

## Smart Categorization Rules

### Slack Tracking (Coordination)
- "Schedule X meeting"
- "Follow up on Y"
- "Coordinate with Z team"
- "Set up discussion about..."
- Administrative tasks
- Planning and coordination

### JIRA Tracking (Technical)
- "Research X technology"
- "Create Y documentation" (will be mirrored to AVP space)
- "Implement Z feature"
- "Define requirements for..."
- Development work
- Technical analysis

**Documentation Mirroring**: Documentation tickets in KATA space are automatically mirrored to AVP space (parent: AVP-5477). AVP mirrors are excluded from Slack summaries.

## TBD Default System

- **Display**: Shows "TBD" for parent_id and release in tickets.md
- **Processing**: If user approves with TBD values, system applies defaults:
  - `parent_id: TBD` → `KATA-127`
  - `release: TBD` → `Release 2026.1`
- **Flexibility**: User can specify custom values or leave as TBD

## Usage

This skill focuses purely on ticket file creation and does not create JIRA tickets or workspaces. It produces an editable tickets.md file that can be reviewed and modified before ticket creation.

## Integration

- **Input**: Action items from meeting analysis
- **Output**: Editable tickets.md file with smart defaults
- **Reusable**: Can be called from meeting-plan, standalone ticket creation, or other workflows
- **User-friendly**: Clean YAML format with clear field guide and TBD system