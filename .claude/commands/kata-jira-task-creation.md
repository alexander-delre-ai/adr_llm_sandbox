---
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

## AVP Documentation Mirroring

**CRITICAL**: When creating documentation tickets in KATA space:
1. **Identify documentation tickets**: A ticket is a documentation ticket if:
   - parent_id is "KATA-2226", OR
   - The ticket title or description contains any of these keywords: `document`, `documentation`, `write`, `tutorial`, `guide`, `runbook`, `README`, `SDK setup`, `API doc`
   - If detected by keyword but parent_id is TBD, automatically set parent_id to "KATA-2226"
2. **Create AVP mirror ticket**: Automatically create corresponding ticket in AVP space
3. **AVP ticket details**:
   - Parent epic: **AVP-5477** (AVP documentation epic)
   - Description: Include link to original KATA ticket
   - Same priority, story points, and assignee as KATA ticket
4. **Slack exclusion**: AVP documentation tickets should NOT appear in Slack summaries (only KATA tickets)

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
   - `description`: the description in plain markdown text. Append a blank line followed by "Created via JIRA MCP" as a separate paragraph — do NOT use `\n` escape sequences; pass the text with real line breaks or as separate sentences
   - `contentFormat`: "markdown"
   - `assignee_account_id`: account ID from lookup (omit if "Unassigned" or lookup failed)
   - `additional_fields`: object with required fields:
     - `priority`: {"name": "P1"} (or P0, P2, P3)
     - `parent`: {"key": "KATA-XXXX"} (epic ID)
     - `customfield_10104`: {"id": "10002"} (release ID from mapping above)
     - `customfield_10137`: 0 (story points, required field)
4. **Create AVP Mirror** (if documentation ticket):
   - Check if parent epic is "KATA-2226" or ticket involves documentation work
   - If yes, create corresponding ticket in AVP space using the applied MCP server:
     - Same summary and assignee as KATA ticket
     - Description: Original description + "\n\nMirror of KATA ticket: [KATA-XXXX](https://appliedint-katana.atlassian.net/browse/KATA-XXXX)\n\nCreated via JIRA MCP"
     - Parent epic: "AVP-5477"
     - Same priority and story points
     - **Engagement**: "Komatsu" (required field for AVP project)
   - AVP tickets are for internal tracking only and should NOT appear in Slack summaries

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
