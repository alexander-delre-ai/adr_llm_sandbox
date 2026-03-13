---
name: daily-todos
description: Generates daily to-do lists for AlexD by scanning workspace directories for action items and JIRA tickets. Creates organized markdown files with checkboxes in todos directory, sorted by Slack items and JIRA tickets. Use when creating daily task lists, organizing action items, or tracking completion status.
---

# Daily Todo Generator

## Instructions

This skill scans all workspace directories and generates daily to-do lists for AlexD with organized, priority-based layout optimized for Cursor. The todos are grouped by priority and theme for efficient daily review.

### Workflow

1. **Scan workspaces**: Read all workspace directories under `/workspaces/`
2. **Extract action items**: Parse `action-items.md`, `tickets.md`, and `jira-tickets/*.json` files
3. **Categorize todos**: Group by priority (High/Medium/Low) and theme
4. **Generate organized list**: Create Cursor-optimized markdown with checkboxes
5. **Save to todos directory**: Place in `todos/YYYY-MM-DD.md` format

### Output Format

**Organized Markdown**: `todos/YYYY-MM-DD.md`
- ✅ Priority-based sections (🔴 High → 🟡 Medium → 🟢 Low)
- ✅ Slack items grouped by theme (Meeting Scheduling, JIRA Management, etc.)
- ✅ Cursor-compatible checkboxes for progress tracking
- ✅ Visual priority indicators and emojis
- ✅ Hyperlinked Slack searches and JIRA tickets
- ✅ Summary statistics and focus areas
- ✅ Clean, scannable layout for daily review

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

**Generate today's todos**:
```
Generate my daily todo list
```

**Generate and sync to TickTick**:
```
Generate my daily todos and sync to TickTick
```

**Generate for specific date**:
```
Create todo list for March 15, 2026
```

## Quick Implementation

To generate organized daily todo list:

1. **Create todos directory**: `mkdir -p todos`
2. **Generate organized todos**: `bash .cursor/skills/daily-todos/scripts/generate_todos.sh`
3. **Generate and sync to TickTick**: `bash .cursor/skills/daily-todos/scripts/generate_todos.sh --sync-ticktick`
4. **For specific date**: `bash .cursor/skills/daily-todos/scripts/generate_todos.sh 2026-03-15 --sync-ticktick`

The script automatically:
- Scans all workspace directories
- Extracts action items from tables and YAML blocks
- Filters for AlexD or unassigned items
- Groups by priority (High → Medium → Low)
- Categorizes Slack items by theme
- Generates Cursor-optimized markdown with checkboxes and hyperlinks
- Optionally syncs to TickTick for task management integration