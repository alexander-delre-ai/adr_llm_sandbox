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
- `story_points` - numeric estimate (always defaults to 0, field is required)

## Validation rules

- `summary` must be 10-255 characters
- `epic_id` must match pattern `KATA-[0-9]+`
- `release` must be a semver or named milestone string
- If any mandatory field is missing, stop and ask the user before generating the payload
- **TBD handling**: If `epic_id` is "TBD", use "KATA-127". If `release` is "TBD", use "Release 26.1"
- **Uprev auto-detection**: If the ticket title or description contains `uprev`, `up-rev`, `upgrade`, or `bump` (version context), automatically set `epic_id` to "KATA-379" when not otherwise specified

## Workflow

1. **MANDATORY RE-READ GATE**: When working from a tickets.md file, you MUST call the Read tool on the tickets.md file path **immediately before creating any JIRA tickets** -- even if you read it earlier in the conversation. The user may have edited titles, descriptions, tracking types, or removed items since your last read. Never rely on cached/in-memory contents of tickets.md.
2. **MANDATORY TRACKING FILTER**: After re-reading, parse each action item's `tracking` field. **Only create JIRA tickets for items where `tracking` is `jira` or `both`**. Skip any item where `tracking` is `slack` -- those are Slack-only action items and must not produce JIRA tickets. Log skipped items so the user can see what was filtered out.
3. **Validate ticket titles**: Ensure ticket summaries match the action item heading from the freshly-read tickets.md exactly (not from memory or a prior read)
4. Confirm all mandatory fields are present; prompt for any that are missing
5. Reject any `epic_id` that does not start with `KATA-`
6. Fill optional fields with defaults when absent
7. **IMPORTANT**: Check if KATA MCP server has tools available
8. If tools are available, create the actual JIRA ticket using the MCP server with **final edited content from the re-read**
9. If tools are not available, output the JSON payload for manual creation

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
- **KATA-379**: Uprev tickets (any ticket related to version/dependency uprevs)

## AVP documentation mirroring (opt in only)

**Default: do not create AVP mirror tickets** when creating KATA issues, including documentation work under KATA-2226 or tickets matched by documentation keywords.

**Create an AVP mirror only when** the user explicitly asks in the same workflow (for example "create AVP mirror" or "mirror this to AVP"), or when `tickets.md` includes an explicit per item note such as `avp_mirror: true` in the YAML block (convention: if absent, no mirror).

When mirroring is explicitly requested, use epic **AVP-5477**, engagement **Komatsu**, description includes a link to the KATA issue, same summary and assignee as KATA unless the user overrides.

**Slack summaries**: Only list KATA keys. If legacy AVP mirrors exist, still omit them from office hours Slack threads.

## Implementation

**Note**: The `user-atlassian-mcp-kata` MCP server is available and functional. This skill will:

### MCP Server Integration (Primary Method)
Use the `user-atlassian-mcp-kata` MCP server to create tickets:

1. **Get Cloud ID**: Call `getAccessibleAtlassianResources` to get the cloud ID for the KATA project
2. **Lookup Assignee** (if assignee is not "Unassigned"):
   - Call `lookupJiraAccountId` with assignee name to get account ID
   - If lookup fails, proceed without assignee (will be unassigned)
3. **Create KATA Ticket**: Call `createJiraIssue` with these parameters:
   - `cloudId`: "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51" (KATA cloud ID)
   - `projectKey`: "KATA"
   - `issueTypeName`: "Task" (or "Story" if specified)
   - `summary`: the ticket name
   - `description`: the description in plain markdown text. Append a blank line followed by "Created via JIRA MCP" as a separate paragraph. Do not use `\n` escape sequences; pass the text with real line breaks or as separate sentences
   - `contentFormat`: "markdown"
   - `assignee_account_id`: account ID from lookup (omit if "Unassigned" or lookup failed)
   - `additional_fields`: object with required fields:
     - `priority`: {"name": "P1"} (or P0, P2, P3)
     - `parent`: {"key": "KATA-XXXX"} (epic ID)
     - `customfield_10104`: {"id": "10002"} (release ID from mapping above)
     - `customfield_10137`: 0 (story points, required field)
4. **AVP mirrors**: Skip unless the user or `tickets.md` explicitly requests mirroring (see "AVP documentation mirroring" above). Do not call `user-atlassian-mcp-applied` `createJiraIssue` for mirrors by default.

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
// 1. Lookup assignee (if not "Unassigned")
CallMcpTool({
  server: "user-atlassian-mcp-kata",
  toolName: "lookupJiraAccountId",
  arguments: {
    cloudId: "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51",
    searchString: "Alex Del Re"
  }
})

// 2. Create KATA ticket
CallMcpTool({
  server: "user-atlassian-mcp-kata",
  toolName: "createJiraIssue", 
  arguments: {
    cloudId: "eadd00c6-0d3f-4c89-99e3-ad95a0daaa51",
    projectKey: "KATA",
    issueTypeName: "Task",
    summary: "Create PyArch threading examples",
    description: "Document threading patterns and best practices for PyArch applications.\n\nCreated via JIRA MCP",
    assignee_account_id: "account_id_from_lookup", // Omit if "Unassigned"
    additional_fields: {
      priority: {"name": "P2"},
      parent: {"key": "KATA-2226"},
      customfield_10104: {"id": "10002"}, // Release 26.1
      customfield_10137: 0 // Story points (required)
    }
  }
})

// 3. Optional: AVP mirror only if user explicitly requests (see "AVP documentation mirroring").
```

## Release ID Quick Reference

- Release 25.1: `{"id": "10000"}`
- Release 25.2: `{"id": "10001"}`  
- Release 25.3: `{"id": "10036"}`
- Release 26.1: `{"id": "10002"}`
- Release 26.2: `{"id": "10003"}`
