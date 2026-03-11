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

## Output format

Produce a structured JIRA ticket payload as a fenced JSON block:

```json
{
  "fields": {
    "project": { "key": "AVP" },
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

## Validation rules

- `summary` must be 10-255 characters
- `epic_id` must match pattern `AVP-[0-9]+`
- `release` must be a semver or named milestone string
- If any mandatory field is missing, stop and ask the user before generating the payload

## Workflow

1. Confirm all mandatory fields are present; prompt for any that are missing
2. Reject any `epic_id` that does not start with `AVP-`
3. Fill optional fields with defaults when absent
4. Output the JSON payload
5. Append a one-line summary: `Ticket ready: [<name>] under epic <epic_id> for release <release>`
