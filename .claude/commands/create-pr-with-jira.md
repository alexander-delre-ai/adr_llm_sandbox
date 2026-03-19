---
description: Creates a KATA JIRA ticket for a GitHub PR, updates the PR title to prepend the ticket ID, and comments the JIRA link on the PR. Auto-detects epic from PR content (uprev -> KATA-379, docs -> KATA-2226). Prompts for release.
---

# Create PR with JIRA

Links a GitHub PR to a new KATA JIRA ticket: creates the ticket, prepends the ticket ID to the PR title, and posts the JIRA link as a PR comment.

## Input

- `pr_url` - GitHub PR URL (required), e.g. `https://github.com/ExtAppliedVehicleOS/vehicle-os-katana/pull/228`

## Workflow

1. **Parse PR URL**: Extract `owner/repo` and PR number from the URL pattern `https://github.com/<owner>/<repo>/pull/<number>`

2. **Fetch PR details**: Run `gh pr view <number> --repo <owner/repo> --json title,body,url` to get the current title and body

3. **Check for existing ticket prefix**: If the PR title already starts with `KATA-`, warn the user and skip ticket creation and title update

4. **Determine epic** using auto-detection (checked in order):
   - If title or body contains `uprev`, `up-rev`, `upgrade`, or `bump` (version context): use **KATA-379**
   - If title or body contains `document`, `documentation`, `write`, `tutorial`, `guide`, `runbook`, `README`, `SDK setup`, or `API doc`: use **KATA-2226**
   - If no match: prompt user to provide the epic ID (`KATA-XXXX`)

5. **Prompt for release**: Ask user which release to target. Available releases:

   | Release | Release Date |
   |---------|-------------|
   | Release 25.1 | 2025-09-26 |
   | Release 25.2 | 2025-12-26 |
   | Release 25.3 | 2026-04-03 |
   | Release 26.1 | 2026-06-26 |
   | Release 26.2 | 2026-09-18 |

6. **Create KATA JIRA ticket** via MCP (see Implementation below)

7. **Update PR title**: Run `gh pr edit <number> --repo <owner/repo> --title "KATA-XXXX: <original title>"`

8. **Post comment**: Run `gh pr comment <number> --repo <owner/repo> --body "JIRA: https://appliedint-katana.atlassian.net/browse/KATA-XXXX"`

## Ticket Defaults

- **Summary**: Original PR title (unmodified)
- **Priority**: P1
- **Story points**: 0
- **Assignee**: Unassigned

## Release Mapping

The Release field uses `customfield_10104`:

| Release Name | Field ID |
|--------------|----------|
| Release 25.1 | 10000 |
| Release 25.2 | 10001 |
| Release 25.3 | 10036 |
| Release 26.1 | 10002 |
| Release 26.2 | 10003 |

## Epic Auto-Detection Rules

| Keyword match in PR title or body | Epic |
|-----------------------------------|------|
| `uprev`, `up-rev`, `upgrade`, `bump` (version context) | KATA-379 |
| `document`, `documentation`, `write`, `tutorial`, `guide`, `runbook`, `README`, `SDK setup`, `API doc` | KATA-2226 |
| No match | Prompt user |

## Implementation

Use the `mcp__kata-atlassian` MCP server:

1. **Create ticket**: Call `mcp__kata-atlassian__createJiraIssue` with:
   - `cloudId`: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`
   - `projectKey`: `KATA`
   - `issueTypeName`: `Task`
   - `summary`: PR title
   - `description`: PR URL + upstream context from body if available + `\n\nCreated via JIRA MCP`
   - `contentFormat`: `markdown`
   - `additional_fields`:
     - `priority`: `{"name": "P1"}`
     - `parent`: `{"key": "<epic_id>"}`
     - `customfield_10104`: `{"id": "<release_field_id>"}`
     - `customfield_10137`: `0`

2. **On success**: extract `key` (e.g. `KATA-2911`) from the response

3. **Update PR title**: `gh pr edit <number> --repo <owner/repo> --title "KATA-XXXX: <original title>"`

4. **Post comment**: `gh pr comment <number> --repo <owner/repo> --body "JIRA: https://appliedint-katana.atlassian.net/browse/KATA-XXXX"`

If MCP is unavailable, output the JSON payload for manual creation and skip the PR updates.

## Output

On completion, report:
- JIRA ticket key and URL
- Confirmation that PR title was updated
- Confirmation that PR comment was posted

ARGUMENTS: $ARGUMENTS
