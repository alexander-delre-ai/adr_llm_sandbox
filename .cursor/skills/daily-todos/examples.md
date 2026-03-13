# Daily Todo Examples

## Example Usage

### Generate Today's Todos
```
Generate my daily todo list
```

### Generate for Specific Date
```
Create todo list for March 15, 2026
```

### Update Existing Todos
```
Update my todos with latest workspace items
```

## Example Output

### Sample Daily Todo File (todos/2026-03-12.md)

```markdown
# 📋 Daily Todos - March 12, 2026

**Progress**: 0/29 completed (0%) | 🔴 19 High | 🟡 10 Medium | 🟢 0 Low

---

## 🔴 High Priority Items (P0/P1)

- [ ] 🎫 **[KATA-2573](https://appliedint-katana.atlassian.net/browse/KATA-2573)** Define mandatory hardware diagnostics requirements for each manager
      *Priority: P1 • Points: 0.1 • Status: Backlog*

- [ ] 💬 **P1** Check with Katana team on provisioning a Katana Jira admin
      *Assigned to: AlexD* • [2026-03-12-katana-jira-setup-sync](https://appliedint.slack.com/archives/search?q=katana%20jira%20setup%20sync)

## 🟡 Medium Priority Items (P2)

- [ ] 💬 **P2** Document the purpose and usage of test_only targets and mock kernel interfaces
      *Assigned to: AlexD* • [2026-03-12-sdv-office-hours](https://appliedint.slack.com/archives/search?q=sdv%20office%20hours)

---

## 💬 Slack Items by Theme

### Meeting Scheduling (10 items)

- [ ] 🔴 **P1** Schedule manager planning meetings with system engineering
      *Assigned to: AlexD* • [2026-03-10-katana-applied-sdv-sw-office-hours](https://appliedint.slack.com/archives/search?q=katana%20applied%20sdv%20sw%20office%20hours)

### JIRA & Access Management (4 items)

- [ ] 🔴 **P1** Work with Lauren to get Komatsu team access to JIRA plans
      *Assigned to: AlexD* • [2026-03-11-katana-applied-sdv-sw-office-hours](https://appliedint.slack.com/archives/search?q=katana%20applied%20sdv%20sw%20office%20hours)

---

## 📊 Summary

| Priority | Count | Type Breakdown |
|----------|-------|----------------|
| 🔴 High (P0/P1) | 19 | 15 Slack, 4 JIRA |
| 🟡 Medium (P2) | 10 | 6 Slack, 4 JIRA |
| **📋 Total** | **29** | **21 Slack, 8 JIRA** |

### 🎯 Focus Areas
- **Immediate**: 19 high priority items need attention
- **This Week**: 10 medium priority items for planning
```

## Workspace File Formats

### action-items.md Format
```markdown
# Action Items: Meeting Name (Date)

## Tasks

| # | What | Who | Priority | Due | Theme |
|---|------|-----|----------|-----|-------|
| 1 | Check with Katana team on provisioning a Katana Jira admin | AlexD | High | ASAP | Jira Permissions & Access |
| 2 | Research options on conditional release field requirements | Lauren Joyce | Medium | Next week | Field Requirements & Workflows |
```

### tickets.md Format
```markdown
# Action Items: Meeting Name (Date)

## Action Item 2: Check with Katana team on provisioning a Katana Jira admin

```yaml
tracking: slack
priority: P1
assignee: AlexD
parent_id: TBD
release: TBD
story_points: 0
description: Verify if Komatsu should have dedicated Jira admin and confirm Mike as the right person for the role.
```

## Action Item 4: Research options on conditional release field requirements

```yaml
tracking: jira
priority: P2
assignee: Lauren Joyce
parent_id: KATA-127
release: Release 2026.1
story_points: 1
description: Investigate making release field required only when moving tickets to "In Progress" status.
```
```

### jira-tickets/*.json Format
```json
{
  "ticket_key": "KATA-2573",
  "ticket_id": "25968",
  "web_url": "https://appliedint-katana.atlassian.net/browse/KATA-2573",
  "api_url": "https://api.atlassian.com/ex/jira/...",
  "summary": "Define mandatory hardware diagnostics requirements for each manager",
  "description": "Work with Chad and Lee to determine mandatory requirements...",
  "issue_type": "Task",
  "priority": "P1",
  "status": "Backlog",
  "assignee": null,
  "parent_epic": "KATA-127",
  "release": "Release 25.3",
  "story_points": 0.1,
  "project": "KATA",
  "created_date": "2026-03-11",
  "created_via": "JIRA MCP",
  "meeting_source": "Katana <> Applied: SDV SW Office Hours (Mar 10, 2026)",
  "action_item_number": 6
}
```

## Filtering Logic

### Items Included for AlexD
- Action items with assignee "AlexD" (case insensitive)
- Items with assignee "Unassigned" or empty assignee field
- JIRA tickets with null assignee or assignee containing "alexd"

### Priority Mapping
- **High Priority**: P0, P1, or contains "high" (case insensitive)
- **Medium Priority**: P2 or contains "medium"
- **Low Priority**: P3 or contains "low"

### Tracking Types
- **slack**: Items that only need Slack notification (no JIRA ticket)
- **jira**: Items that have or will have JIRA tickets
- **both**: Same as jira (creates ticket + Slack notification)