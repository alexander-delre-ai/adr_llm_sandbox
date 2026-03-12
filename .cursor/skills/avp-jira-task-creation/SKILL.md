---
name: avp-jira-task-creation
description: Creates a new JIRA ticket in the AVP project space. Use when converting a meeting action item or planned task into an AVP JIRA issue. Epic IDs must use the AVP- prefix. Requires epic ID, release, and ticket name as mandatory fields.
---

# AVP JIRA Task Creation

Project space: **AVP** (ticket prefix `AVP-`)

## Mandatory fields

Every ticket requires:
- `epic_id` - the parent epic key, must use `AVP-` prefix (e.g. `AVP-42`)
- `release` - the target release/version (e.g. `v2.4.0`)
- `name` - short, imperative ticket title (e.g. `Implement OAuth2 login flow`)

## Optional fields

Include when available:
- `description` - detailed acceptance criteria or context
- `priority` - `Highest`, `High`, `Medium`, `Low`, `Lowest` (default: `Medium`)
- `assignee` - team member handle or name
- `labels` - comma-separated list
- `story_points` - numeric estimate

## Validation rules

- `summary` must be 10-255 characters
- `epic_id` must match pattern `AVP-[0-9]+`
- `release` must be a semver or named milestone string
- If any mandatory field is missing, stop and ask the user before generating the payload

## Workflow

1. **CRITICAL**: If working from tickets.md file, read the final edited version to get user-modified titles and descriptions
2. Confirm all mandatory fields are present; prompt for any that are missing
3. Reject any `epic_id` that does not start with `AVP-`
4. Fill optional fields with defaults when absent
4. Get the cloud ID for the AVP project using the MCP server
5. Create the actual JIRA ticket using the MCP server
6. Report the created ticket details including the ticket key

## Implementation

Use the `user-atlassian-mcp-applied` MCP server to create tickets:

1. **Get Cloud ID**: Call `getAccessibleAtlassianResources` to get the cloud ID for the AVP project
2. **Create Ticket**: Call `createJiraIssue` with these parameters:
   - `cloudId`: from step 1
   - `projectKey`: "AVP"
   - `issueTypeName`: "Task" (or "Story" if specified)
   - `summary`: the ticket name
   - `description`: the description in markdown format
   - `additional_fields`: object containing:
     - Epic link field (use appropriate custom field name)
     - Priority field
     - Fix versions for release
     - Labels array
     - Story points

## MCP Tool Usage

```javascript
// Step 1: Get cloud ID
CallMcpTool({
  server: "user-atlassian-mcp-applied",
  toolName: "getAccessibleAtlassianResources"
})

// Step 2: Lookup assignee (if not "Unassigned")
CallMcpTool({
  server: "user-atlassian-mcp-applied",
  toolName: "lookupJiraAccountId",
  arguments: {
    cloudId: "<cloud_id_from_step_1>",
    searchString: "assignee_name"
  }
})

// Step 3: Create the issue
CallMcpTool({
  server: "user-atlassian-mcp-applied", 
  toolName: "createJiraIssue",
  arguments: {
    cloudId: "<cloud_id_from_step_1>",
    projectKey: "AVP",
    issueTypeName: "Task",
    summary: "<name>",
    description: "<description>\n\nCreated via JIRA MCP",
    assignee_account_id: "<account_id_from_step_2>", // Omit if "Unassigned"
    additional_fields: {
      // Epic link, priority, fix versions, labels, story points
    }
  }
})
