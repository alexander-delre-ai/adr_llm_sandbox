---
name: meeting-tickets
description: Creates editable tickets.md file from meeting action items with proper tracking categorization, defaults, and YAML format. Use after meeting analysis to generate reviewable ticket proposals.
---

# Meeting Tickets

Converts meeting action items into editable tickets.md file with proper tracking categorization, field defaults, and clean YAML format for user review and editing.

## Input Requirements

- **Action items list**: From meeting analysis (Step 5 output)
- **Meeting metadata**: Title, date for file headers
- **Output location**: Directory path where tickets.md should be created (format: workspaces/YYYY-MM-DD/meeting-name/)

## Workflow

### Step 1 - Categorize tracking types

For each action item, determine tracking type:

**Auto-assign to "slack":**
- Items involving: "schedule", "meeting", "coordinate", "set up", "discuss", "follow up", "check with", "bring up", "talk to", "sync with", "ping", "ask about", "confirm with"
- Coordination and planning tasks
- Administrative follow-ups
- Conversational actions (discussions, check-ins, raising topics with someone)

**Auto-assign to "jira":**
- Technical development work
- Research and analysis tasks
- Documentation creation
- Implementation work

### Step 2 - Apply field defaults

**Epic inference**: Read `.cursor/skills/meeting-tickets/meeting-epic-mapping.json` and match the meeting title/slug against the patterns. If a match is found, use the mapped `parent_id` as the default instead of TBD. Individual tickets can still override this value.

For each action item, set these defaults:
- **tracking**: Based on categorization above
- **priority**: Map from analysis priority (High→P1, Medium→P2, Low→P3)
- **assignee**: "Unassigned" (single person per item)
- **parent_id**: Inferred from meeting-epic-mapping.json if meeting matches a pattern, otherwise "TBD" (will become KATA-127 if unchanged)
- **release**: Inferred from timeline mentions in the action item or transcript (see table below), otherwise "TBD" (will become Release 2026.1 if unchanged)
- **story_points**: Estimated from description heuristics (see table below), editable by user
- **description**: Clean summary from action item

**Story point estimation heuristics:**

| Points | Signals in title/description | Examples |
|--------|------------------------------|----------|
| 0.2 | "follow up", "check", "confirm", "ask", "ping", single-step coordination | "Follow up on HDR plugin delivery" |
| 0.5 | "investigate", "research", "define", "review", multi-person coordination | "Investigate steering system architecture" |
| 1 | "implement", "create", "build", "design", technical deliverables | "Create JIRA ticket for variable naming convention" |
| 2 | Multiple sub-tasks implied, cross-team dependency | "Define inter-zonal communication interface and signal gateway approach" |

- Default to 0.5 if the description doesn't clearly match any category
- Never estimate above 2 without explicit scope signals in the transcript
- User can always override in tickets.md

**Release inference from timeline mentions**: Read `.cursor/skills/kata-jira-task-creation/release-mapping.json` and map timeline mentions from the action item description or transcript context to release versions:

| Timeline mention | Mapped release | Reasoning |
|-----------------|----------------|-----------|
| "next sprint", "this sprint", "next 2 weeks" | Release 25.3 | Nearest upcoming release (releaseDate: 2026-04-03) |
| "sprint 15", "Apr 6", "April", "Q2 2026" | Release 26.1 | Mid-2026 release (releaseDate: 2026-06-26) |
| "end of Q3", "September", "Q3 2026" | Release 26.2 | Late-2026 release (releaseDate: 2026-09-18) |
| "Aug 2027", "before Peoria build", dates beyond 2026 | TBD | Beyond current release schedule |

- If no timeline is mentioned, keep "TBD"
- Set the inferred release in tickets.md (still editable by user)
- When the meeting date is close to a release date, prefer the next release rather than one that's nearly past

### Step 3 - Normalize assignee names

Read `.cursor/skills/meeting-slack-summary/user-mapping.md` and resolve each assignee to their canonical name:

- Match transcript names, nicknames, and aliases to the canonical entry (e.g., "NickT" -> "Nick Sturm", "Juan" -> "Hwan Chul Kang", "Ashley" -> "Ashli Forbes", "Nathan" -> "Nuthan Sabbani")
- Use the canonical name consistently in tickets.md for both display and JIRA lookup
- If a name has no match in the mapping, keep the original name as-is
- Names with organization context (Komatsu vs Applied) help with JIRA assignee lookup accuracy

### Step 4 - Format action item titles

- **No numbering**: Do not prefix headings with "Action Item 1:", "Action Item 2:", etc.
- **Sentence case**: Use natural sentence case for headings (e.g., "Follow up on build system documentation"), not Title Case

### Step 5 - Generate YAML format

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

### Step 6 - Suggest ticket groupings

After generating all tickets, scan for related items that could be grouped:

- **Shared keywords**: Tickets with overlapping technical terms (e.g., "signal", "interface", "naming convention" all relate to signal architecture)
- **Same assignee + same epic**: Multiple tickets assigned to the same person under the same parent epic
- **Sequential dependencies**: One ticket's output is another ticket's input (e.g., "define naming conventions" before "create DBC/ARXML files")

If 2+ tickets appear related, append a `## Suggested Groupings` section at the bottom of `tickets.md`:

```markdown
## Suggested Groupings

- **Signal architecture**: "Create JIRA ticket for variable naming convention definition" + "Define inter-zonal communication interface" -- both address signal/interface architecture for MVP UI
```

This is advisory only -- the skill does not auto-create parent tickets. The user can choose to group them manually in JIRA.

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
- "Discuss X with Y"
- "Check with Z about..."
- "Bring up X to Y"
- "Talk to / sync with / ping Z"
- "Ask about / confirm with..."
- Administrative tasks
- Planning and coordination
- Conversational actions (anything that is a discussion, not a deliverable)

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