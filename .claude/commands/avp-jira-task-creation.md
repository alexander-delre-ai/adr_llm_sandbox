---
description: Creates a new JIRA ticket in the AVP project space. Use when converting a meeting action item or planned task into an AVP JIRA issue. Epic IDs must use the AVP- prefix. Documentation tickets default to epic AVP-5477. Requires epic ID (or documentation default), engagement, and ticket name as mandatory fields where applicable.
---

# AVP JIRA Task Creation

Project space: **AVP** (ticket prefix `AVP-`)

## Documentation tickets

**All documentation work** (docs, README updates, API docs, runbooks, local machine requirements, SDK setup guides, etc.) must be filed under epic:

| Field | Value |
|-------|--------|
| **epic_id** | **AVP-5477** (fixed; do not ask unless the user overrides) |

When the user asks for a documentation ticket, or the issue is clearly documentation-only, set `epic_id` to **AVP-5477** without prompting for epic. If the user specifies a different epic, use theirs.

## Mandatory fields

Every ticket requires:
- `epic_id` - the parent epic key, must use `AVP-` prefix (e.g. `AVP-42`). **Documentation: always `AVP-5477`** unless overridden. If the user says no parent/epic, omit this field entirely.
- `engagement` - the customer engagement this ticket belongs to (default: `Komatsu`)
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
- `epic_id` must match pattern `AVP-[0-9]+` when provided
- `engagement` defaults to `Komatsu` if not specified
- For documentation tickets, default `epic_id` to **AVP-5477**
- If any mandatory field is missing (except documentation epic default and engagement default), stop and ask the user before generating the payload

## Workflow

1. **CRITICAL**: If working from tickets.md file, read the final edited version to get user-modified titles and descriptions
2. If the ticket is **documentation**, set epic to **AVP-5477** unless the user gave another epic
3. Confirm all mandatory fields are present; prompt for any that are missing
4. Reject any `epic_id` that does not start with `AVP-`
5. Fill optional fields with defaults when absent
6. Get the cloud ID for the AVP project using the MCP server
7. Create the actual JIRA ticket using the MCP server
8. Report the created ticket details including the ticket key

## Implementation

Use the `mcp__kata-atlassian` MCP tools (applied instance) to create tickets:

1. **Get Cloud ID**: Call `mcp__kata-atlassian__getAccessibleAtlassianResources` to get the cloud ID for the AVP project
2. **Create Ticket**: Call `mcp__kata-atlassian__createJiraIssue` with these parameters:
   - `cloudId`: from step 1
   - `projectKey`: "AVP"
   - `issueTypeName`: "Task" (or "Story" if specified)
   - `summary`: the ticket name
   - `description`: the description in markdown format
   - `additional_fields`: object containing:
     - Epic link field: **AVP-5477** for documentation tickets (or user epic), omit if user specified no parent
     - Priority field
     - Labels array (include engagement as a label, e.g. `komatsu`)
     - Story points
