---
name: jira-task-creation-KATA
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
- `component` - add `appliedsync` component only when explicitly requested in the prompt

## Validation rules

- `summary` must be 10-255 characters
- `epic_id` must match pattern `KATA-[0-9]+`
- `release` must be a semver or named milestone string
- If any mandatory field is missing, stop and ask the user before generating the payload
- **TBD handling**: If `epic_id` is "TBD", use "KATA-127". If `release` is "TBD", use "Release 26.1"
- **Uprev auto-detection**: If the ticket title or description contains `uprev`, `up-rev`, `upgrade`, or `bump` (version context), automatically set `epic_id` to "KATA-379" when not otherwise specified

## Workflow

1. **CRITICAL**: If working from tickets.md file, read the final edited version to get user-modified titles and descriptions
2. **Validate ticket titles**: Ensure ticket summaries match the action item names from tickets.md exactly
3. Confirm all mandatory fields are present; prompt for any that are missing
4. Reject any `epic_id` that does not start with `KATA-`
5. Fill optional fields with defaults when absent
5. **IMPORTANT**: Check if KATA MCP server has tools available
6. If tools are available, create the actual JIRA ticket using the MCP server with **final edited content**
7. If tools are not available, output the JSON payload for manual creation

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

**Default: do not create AVP mirror tickets** for KATA work, including documentation tickets (KATA-2226 or documentation keyword matches).

**Mirror to AVP only when** the user explicitly asks, or when `tickets.md` sets `avp_mirror: true` on that item.

When mirroring is requested: epic **AVP-5477**, engagement **Komatsu**, link to the KATA issue in the description. Slack summaries still list **KATA keys only**.

## Implementation

**Note**: The `kata-atlassian` MCP server is available and functional. This skill will:

### MCP Server Integration (Primary Method)

Use the `mcp__kata-atlassian` MCP tools to create tickets:

1. **Get Cloud ID**: Call `mcp__kata-atlassian__getAccessibleAtlassianResources` to get the cloud ID for the KATA project
2. **Lookup Assignee** (if assignee is not "Unassigned"):
   - Call `mcp__kata-atlassian__lookupJiraAccountId` with assignee name to get account ID
   - If lookup fails, proceed without assignee (will be unassigned)
3. **Create KATA Ticket**: Call `mcp__kata-atlassian__createJiraIssue` with these parameters:
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
     - `components`: [{"name": "appliedsync"}] (only include when explicitly requested)
4. **AVP mirrors**: Skip by default. Only create AVP issues when explicitly requested (see section above).

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

## Release ID Quick Reference

- Release 25.1: `{"id": "10000"}`
- Release 25.2: `{"id": "10001"}`
- Release 25.3: `{"id": "10036"}`
- Release 26.1: `{"id": "10002"}`
- Release 26.2: `{"id": "10003"}`
