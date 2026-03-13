# Daily Todo Generator Skill

This skill automatically generates daily to-do lists for AlexD by scanning workspace directories for action items and JIRA tickets.

## Features

- **Automatic Scanning**: Reads all workspace directories under `/workspaces/`
- **Smart Filtering**: Only includes items assigned to AlexD or unassigned items
- **Priority Organization**: Groups items by priority (🔴 High → 🟡 Medium → 🟢 Low)
- **Theme Categorization**: Groups Slack items by common themes (Meeting Scheduling, JIRA Management, etc.)
- **Cursor-Optimized**: Checkboxes work in Cursor for progress tracking
- **Visual Indicators**: Priority emojis and type icons (💬 Slack, 🎫 JIRA)
- **Hyperlinked References**: Clickable links to Slack searches and JIRA tickets
- **Summary Statistics**: Progress tracking and focus area recommendations

## Quick Start

### Using the Skill
Just ask the agent:
```
Generate my daily todo list
```

### Manual Usage
```bash
# Generate today's organized todos
bash .cursor/skills/daily-todos/scripts/generate_todos.sh

# Generate for specific date
bash .cursor/skills/daily-todos/scripts/generate_todos.sh 2026-03-15

# Or use Python script directly
python3 .cursor/skills/daily-todos/scripts/parse_workspaces.py > todos/$(date +%Y-%m-%d).md
```

## Output Format

The generated todo files contain:

### Priority-Based Organization
Items organized by urgency with visual indicators:
```markdown
## 🔴 High Priority Items (P0/P1)

- [ ] 💬 **P1** Check with Katana team on provisioning a Katana Jira admin
      *Assigned to: AlexD* • [Meeting Name](https://appliedint.slack.com/archives/search?q=meeting%20terms)

- [ ] 🎫 **[KATA-2573](https://appliedint-katana.atlassian.net/browse/KATA-2573)** Define mandatory hardware diagnostics requirements
      *Priority: P1 • Points: 0.1 • Status: Backlog*

## 💬 Slack Items by Theme

### Meeting Scheduling (5 items)
- [ ] 🔴 **P1** Schedule manager planning meetings with system engineering
      *Assigned to: AlexD* • [Meeting Link](https://appliedint.slack.com/archives/search?q=terms)
```

### Summary
```markdown
## Summary
- **Total Slack Items**: 21
- **Total JIRA Tickets**: 8
- **High Priority Items**: 19
```

## Data Sources

The skill parses these files from each workspace:

1. **action-items.md**: Table format with action items
2. **tickets.md**: YAML blocks with tracking field
3. **jira-tickets/*.json**: Created JIRA ticket details

## Filtering Logic

**Included Items:**
- Assignee is "AlexD" (case insensitive)
- Assignee is "Unassigned" or empty
- JIRA tickets with null assignee

**Priority Mapping:**
- **High Priority**: P0, P1, or contains "high"
- **Medium Priority**: P2 or contains "medium"  
- **Low Priority**: P3 or contains "low"

## File Structure

```
daily-todos/
├── SKILL.md              # Main skill instructions
├── README.md             # This documentation
├── examples.md           # Usage examples and formats
└── scripts/
    ├── parse_workspaces.py   # Main parsing script
    └── generate_todos.sh     # Wrapper script
```

## Dependencies

- Python 3 with `yaml` and `json` modules (standard library)
- Bash (for wrapper script)

## Example Output

See `examples.md` for complete examples of generated todo files and workspace file formats.