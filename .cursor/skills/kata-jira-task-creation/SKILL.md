---
name: kata-jira-task-creation
description: Creates a new JIRA ticket in the KATA project space. Use when converting a meeting action item or planned task into a KATA JIRA issue. Epic IDs must use the KATA- prefix. Requires epic ID, release, and ticket name as mandatory fields.
---

# KATA JIRA Task Creation

Project space: **KATA** (ticket prefix `KATA-`)

## Mandatory fields

Every ticket requires:
- `epic_id` - the parent epic key, must use `KATA-` prefix (e.g. `KATA-42`)
- `release` - the target release/version (e.g. `v2.4.0`)
- `name` - short, imperative ticket title (e.g. `Implement OAuth2 login flow`)

## Optional fields

Include when available:
- `description` - detailed acceptance criteria or context
- `priority` - `P0` (critical), `P1` (high), `P2` (medium), `P3` (low) (default: `P1`)
- `assignee` - team member handle or name
- `labels` - comma-separated list
- `story_points` - numeric estimate (set to 0 if not specified, field is required)

## Validation rules

- `summary` must be 10-255 characters
- `epic_id` must match pattern `KATA-[0-9]+`
- `release` must be a semver or named milestone string
- If any mandatory field is missing, stop and ask the user before generating the payload

## Workflow

1. Confirm all mandatory fields are present; prompt for any that are missing
2. Reject any `epic_id` that does not start with `KATA-`
3. Fill optional fields with defaults when absent
4. **IMPORTANT**: Check if KATA MCP server has tools available
5. If tools are available, create the actual JIRA ticket using the MCP server
6. If tools are not available, output the JSON payload for manual creation

## Release Mapping

The Release field uses `customfield_10104` with these available versions:

| Release Name | Field ID | Release Date |
|--------------|----------|--------------|
| Release 25.1 | 10000 | 2025-09-26 |
| Release 25.2 | 10001 | 2025-12-26 |
| Release 25.3 | 10036 | 2026-04-03 |
| Release 26.1 | 10002 | 2026-06-26 |
| Release 26.2 | 10003 | 2026-09-18 |

**Usage**: When creating tickets, use `{"id": "10002"}` format for Release 26.1, etc.

## Epic Mapping for Documentation

- **KATA-2226**: Documentation and tutorial expansion tickets
- **KATA-2561**: General meeting follow-up tickets

## Implementation

**Note**: The `user-atlassian-mcp-kata` MCP server is available and functional. This skill will:

### MCP Server Integration (Primary Method)
Use the `user-atlassian-mcp-kata` MCP server to create tickets:

1. **Get Cloud ID**: Call `getAccessibleAtlassianResources` to get the cloud ID for the KATA project
2. **Create Ticket**: Call `createJiraIssue` with these parameters:
   - `cloudId`: "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51" (KATA cloud ID)
   - `projectKey`: "KATA"
   - `issueTypeName`: "Task" (or "Story" if specified)
   - `summary`: the ticket name
   - `description`: the description in markdown format + "\n\n_Created via JIRA MCP from meeting analysis._"
   - `additional_fields`: object with required fields:
     - `priority`: {"name": "P1"} (or P0, P2, P3)
     - `parent`: {"key": "KATA-XXXX"} (epic ID)
     - `customfield_10104`: {"id": "10002"} (release ID from mapping above)
     - `customfield_10137`: 0 (story points, required field)

### Fallback: JSON Output
If MCP server is unavailable, produce a structured JIRA ticket payload as a fenced JSON block:

```json
{
  "fields": {
    "project": { "key": "KATA" },
    "issuetype": { "name": "Task" },
    "summary": "<name>",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "<description>" }]
        }
      ]
    },
    "priority": { "name": "<priority>" },
    "customfield_epic_link": "<epic_id>",
    "fixVersions": [{ "name": "<release>" }],
    "labels": ["<label1>"],
    "story_points": 0
  }
}
```

## MCP Tool Usage Example

```javascript
// Create a documentation ticket under KATA-2226
CallMcpTool({
  server: "user-atlassian-mcp-kata",
  toolName: "createJiraIssue", 
  arguments: {
    cloudId: "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51",
    projectKey: "KATA",
    issueTypeName: "Task",
    summary: "Create PyArch threading examples",
    description: "Document threading patterns and best practices for PyArch applications.\n\n_Created via JIRA MCP from meeting analysis._",
    additional_fields: {
      priority: {"name": "P2"},
      parent: {"key": "KATA-2226"},
      customfield_10104: {"id": "10002"}, // Release 26.1
      customfield_10137: 0 // Story points (required)
    }
  }
})
```

## Release ID Quick Reference

- Release 25.1: `{"id": "10000"}`
- Release 25.2: `{"id": "10001"}`  
- Release 25.3: `{"id": "10036"}`
- Release 26.1: `{"id": "10002"}`
- Release 26.2: `{"id": "10003"}`
