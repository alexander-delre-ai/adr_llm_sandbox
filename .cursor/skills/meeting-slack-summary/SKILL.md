---
name: meeting-slack-summary
description: Composes a Slack message summarizing a completed meeting analysis. Includes attendees, a link to the saved transcript, action items, and corresponding JIRA ticket links. Use after meeting-workspace has run and the workspace path is known.
---

# Meeting Slack Summary

Produces a ready-to-paste Slack message (Block Kit JSON and plain-text fallback) summarizing the meeting for sharing with the team.

## Required inputs

Collect these before composing the message:

| Input | Source |
|-------|--------|
| Meeting title | Step 1 of analysis |
| Meeting date | Step 1 of analysis |
| Attendees | Step 1 of analysis |
| Workspace path | Output of `meeting-workspace` skill |
| Action items | Step 5 of analysis (What, Who, Priority) |
| JIRA ticket keys + URLs | Step 6 of analysis (optional - omit row if no tickets were created) |

If the workspace path is not yet known, run the `meeting-workspace` skill first.

Ask the user for one optional input:
- **Slack channel** - where this message will be posted (e.g. `#team-engineering`). Used only as a label in the output header; leave blank if unknown.

## Plain-text format

Output this first so it can be pasted into any Slack input:

```
*Meeting Summary: <title>* | <date>

*Attendees:* <comma-separated list>

*Transcript:* /workspaces/<slug>/transcript.md

*Action Items:*
• <what> — <who> [<Priority>] <JIRA-KEY: https://jira.example.com/browse/JIRA-KEY> (omit if no ticket)
• ...

_Full analysis:_ /workspaces/<slug>/analysis.md
```

## Block Kit JSON format

After the plain-text version, output a `json` fenced block containing a Slack Block Kit payload:

```json
{
  "text": "Meeting Summary: <title>",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "Meeting Summary: <title>" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Date:*\n<date>" },
        { "type": "mrkdwn", "text": "*Attendees:*\n<comma-separated list>" }
      ]
    },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Transcript:* `/workspaces/<slug>/transcript.md`" }
    },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Action Items:*" }
    },
    {
      "type": "rich_text",
      "elements": [
        {
          "type": "rich_text_list",
          "style": "bullet",
          "elements": [
            {
              "type": "rich_text_section",
              "elements": [
                { "type": "text", "text": "<what> — <who> ", "style": { "bold": false } },
                { "type": "text", "text": "[<Priority>]", "style": { "italic": true } },
                { "type": "text", "text": " " },
                { "type": "link", "url": "https://jira.example.com/browse/<JIRA-KEY>", "text": "<JIRA-KEY>" }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        { "type": "mrkdwn", "text": "Full analysis: `/workspaces/<slug>/analysis.md`" }
      ]
    }
  ]
}
```

## Rules

- Omit the JIRA link element entirely for any action item that has no ticket
- If no JIRA tickets were created at all, remove the link column and note `_(No JIRA tickets created)_` after the action items list
- Replace `https://jira.example.com/browse/` with the actual Jira base URL if the user provides one; otherwise keep the placeholder
- Keep the plain-text version under 3000 characters (Slack message limit)
- If the action items list would exceed the limit, truncate to the top 10 by priority and add `_(+ N more — see analysis.md)_`
