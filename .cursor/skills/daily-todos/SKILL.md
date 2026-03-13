---
name: daily-todos
description: Generates daily to-do lists for AlexD by scanning workspace directories for Slack action items and syncing them directly to TickTick Cursor Sync project. Optionally creates markdown files. Use when creating daily task lists, syncing todos to TickTick, or organizing action items.
---

# Daily Todo Generator

## Instructions

This skill scans all workspace directories and generates daily to-do lists for AlexD by syncing Slack action items directly to TickTick "Cursor Sync" project. Provides streamlined workflow from meeting analysis to actionable tasks with clean formatting.

### Workflow

1. **Scan workspaces**: Read all workspace directories under `/workspaces/`
2. **Extract Slack items**: Parse `action-items.md` and `tickets.md` files for Slack action items
3. **Sync to TickTick**: Add tasks directly to TickTick "Cursor Sync" project with proper priorities
4. **Optional markdown**: Generate `todos/YYYY-MM-DD.md` file if requested

### Output Format

**Primary**: TickTick "Cursor Sync" Project Tasks
- ✅ Clean task titles (no priority labels or theme text)
- ✅ Proper TickTick priority mapping (High=P0, Medium=P1, Low=P2)
- ✅ Meeting context in task descriptions (no Slack links)
- ✅ Theme-based tags/labels for organization
- ✅ Accessible across all devices via TickTick

**Optional Markdown**: `todos/YYYY-MM-DD.md` (use `--markdown-only` flag)
- ✅ Priority-based sections with visual indicators
- ✅ Slack items grouped by theme
- ✅ Hyperlinked Slack searches
- ✅ Summary statistics and completion tracking

### Todo Categories

**Slack Items**: Action items marked with `tracking: slack` in tickets.md or items from action-items.md that don't have corresponding JIRA tickets. Each item includes a hyperlink to search for the meeting in Slack.

**JIRA Tickets**: Items with actual JIRA ticket numbers and URLs from the jira-tickets directory. Ticket IDs are hyperlinked directly to the JIRA issue.

### Output Format

```markdown
# Daily Todos - [Date]

## Slack Action Items

- [ ] **[Priority]** [Description] - *Assigned to: [Person]* ([Meeting Source with Slack search link])
- [ ] **P1** Check with Katana team on provisioning a Katana Jira admin - *Assigned to: AlexD* ([2026-03-12-katana-jira-setup-sync](https://appliedint.slack.com/archives/search?q=katana%20jira%20setup%20sync))

## JIRA Tickets

- [ ] **[Clickable TICKET-ID]** [Summary] - *Priority: [Priority], Points: [Story Points]* ([Meeting Source])
  - **URL**: [JIRA URL]
  - **Status**: [Current Status]
  - **Assignee**: [Current Assignee]

- [ ] **[KATA-2573](https://appliedint-katana.atlassian.net/browse/KATA-2573)** Define mandatory hardware diagnostics requirements for each manager - *Priority: P1, Points: 0.1* (Katana Applied SDV SW Office Hours)
  - **URL**: https://appliedint-katana.atlassian.net/browse/KATA-2573
  - **Status**: Backlog
  - **Assignee**: Unassigned

## Summary

- **Total Slack Items**: [count]
- **Total JIRA Tickets**: [count]
- **High Priority Items**: [count]
```

### Implementation Steps

1. **Create todos directory** if it doesn't exist
2. **Scan workspace directories**:
   - List all directories in `/workspaces/`
   - For each workspace, check for:
     - `action-items.md` (contains action items table)
     - `tickets.md` (contains YAML action items with tracking field)
     - `jira-tickets/` directory (contains JSON files with created tickets)
3. **Parse action items**:
   - From `action-items.md`: Extract table rows with tasks
   - From `tickets.md`: Extract YAML blocks, filter by tracking field
   - From `jira-tickets/*.json`: Extract ticket details
4. **Filter for AlexD**: Only include items assigned to "AlexD" or unassigned items
5. **Generate markdown**: Create formatted todo list with checkboxes
6. **Save file**: Write to `todos/YYYY-MM-DD.md`

### File Parsing Patterns

**action-items.md format**:
```markdown
| # | What | Who | Priority | Due | Theme |
|---|------|-----|----------|-----|-------|
| 1 | Task description | AlexD | High | ASAP | Theme |
```

**tickets.md format**:
```yaml
tracking: slack  # or "jira"
priority: P1
assignee: AlexD
description: Task description
```

**jira-tickets/*.json format**:
```json
{
  "ticket_key": "KATA-2573",
  "web_url": "https://...",
  "summary": "Task summary",
  "priority": "P1",
  "status": "Backlog",
  "assignee": null,
  "story_points": 0.1,
  "meeting_source": "Meeting name"
}
```

### Error Handling

- Skip workspaces with missing or malformed files
- Log warnings for unparseable content
- Continue processing other workspaces if one fails
- Create empty sections if no items found

### Date Handling

- Use current date in YYYY-MM-DD format for filename
- Include human-readable date in todo file header
- Check if file already exists and offer to append or overwrite

### File Management

- **Check existing files**: `ls todos/` to see what dates have been generated
- **Overwrite behavior**: Script overwrites existing files by default
- **Backup option**: Copy existing file before regenerating if needed
- **Daily workflow**: Generate fresh list each morning with latest workspace data

## Usage Examples

**Sync today's todos to TickTick** (default behavior):
```
Generate my daily todos
```

**Sync specific date to TickTick**:
```
Generate todos for March 15, 2026
```

**Generate markdown file only**:
```
Generate todos markdown for today
```

**Generate for specific date**:
```
Create todo list for March 15, 2026
```

## Quick Implementation

To sync daily todos to TickTick:

1. **Sync today's todos**: `bash .cursor/skills/daily-todos/scripts/generate_todos.sh`
2. **Sync specific date**: `bash .cursor/skills/daily-todos/scripts/generate_todos.sh 2026-03-15`
3. **Generate markdown only**: `bash .cursor/skills/daily-todos/scripts/generate_todos.sh --markdown-only`

The script automatically:
- Scans all workspace directories for Slack action items
- Syncs tasks directly to TickTick Inbox with proper priorities
- Provides fallback to markdown generation if TickTick sync fails
- Filters out JIRA tickets (Slack items only)
- Creates clean task titles without priority labels
- Adds meeting context and Slack links to task descriptions