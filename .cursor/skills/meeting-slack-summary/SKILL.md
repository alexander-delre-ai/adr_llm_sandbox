---
name: meeting-slack-summary
description: Composes a Slack message summarizing a completed meeting analysis and sends notification to AlexD. Includes attendees, action items, and corresponding JIRA ticket links in office hours thread format. Use after meeting-workspace has run and the workspace path is known.
---

# Meeting Slack Summary

Produces a ready-to-paste Slack message in the specific office hours thread format and sends a notification to AlexD with the content ready for posting.

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

Ask the user for optional inputs (if not already provided):
- **Gemini notes link** - URL to the original meeting notes (if available)
- **Attendee organization** - to separate Komatsu vs Applied attendees  
- **Meeting room confirmation** - if uncertain whether a name is a meeting room or attendee

**Note**: If Gemini notes link was not provided during initial workflow, ask for it before generating Slack summary.

## Slack Message Format

### Top-level thread message:
```
🧵<DD/MM/YYYY>: <Meeting Title>
```

### Reply in thread:
```
**Komatsu Attendees:** <name>, <name>

**Applied Attendees:** <@slack_id>, <@slack_id>

<Gemini notes: URL> (only include this line if URL is provided)

**Action items:**
• <@slack_id or name>, <https://jira-url|JIRA-KEY>: <short description> (if ticket exists)
• <@slack_id or name>: <short description> (if no ticket)
• ...
```

## Implementation Steps

1. **Parse attendees by organization and find Slack IDs**:
   - **Filter out meeting rooms**: Remove scientist names with location codes (e.g., "Coulomb's Law (SVL-WCAL-HQ, FL3)")
   - Identify which attendees are from Komatsu vs Applied
   - Use `slack_search_users` to find Slack user IDs for Applied attendees
   - Format Applied attendees as `<@USER_ID>` for Slack mentions
   - Keep external attendees (like Komatsu) as plain names

2. **Format the date and thread title**:
   - Convert from meeting date to DD/MM/YYYY format
   - Example: "Mar 6, 2026" → "06/03/2026"
   - Add colon after date: `🧵06/03/2026: Meeting Title`

3. **Generate both messages**:
   - Top-level thread starter
   - Threaded reply with full details
   - Only include Gemini notes line if URL is provided

4. **Handle JIRA links**:
   - Include actual ticket URLs if tickets were created
   - Use Slack hyperlink format: `<https://appliedint-katana.atlassian.net/browse/KATA-2563|KATA-2563>`
   - This displays only the ticket ID as a clickable link
   - Omit JIRA reference entirely if no ticket exists for that action item

5. **Send message to AlexD**:
   - After generating the Slack content, send a direct message to AlexD
   - Include the office hours thread content for posting
   - Provide context about the meeting and action items

## Rules

- **Date format**: Always use DD/MM/YYYY: format in the thread title
- **Thread title**: Use actual meeting title, not generic "Office hours"
- **Attendee formatting**: Bold headers, comma-separated lists, Slack mentions for Applied attendees
- **Slack mentions**: Use `<@USER_ID>` format for Applied attendees, plain names for external
- **JIRA links**: Use Slack hyperlink format `<URL|TICKET-ID>` to show only ticket IDs as clickable links
- **Gemini notes**: Include as hyperlink only if provided, otherwise omit the line entirely
- **Action items**: Bold header, format as assignee, hyperlink, description
- **Character limit**: Keep under Slack's message limits
- **Two separate messages**: Provide both the thread starter and the reply content

## Example Output

**Thread starter:**
```
🧵06/03/2026: Komatsu <> VehicleOS Adaptive Architecture sync
```

```
**Komatsu Attendees:** Nuthan Sabbani

**Applied Attendees:** <@U080A6CFRAQ>, <@U063Y6FQA5V>

Link to gemini notes: N/A

**Action items:**
• <@U080A6CFRAQ>, <https://appliedint-katana.atlassian.net/browse/KATA-2563|KATA-2563>: Research schema migration support in PyArch persistency module
• Nuthan Sabbani, <https://appliedint-katana.atlassian.net/browse/KATA-2565|KATA-2565>: Provide detailed payload feature requirements
• <@U063Y6FQA5V>, <https://appliedint-katana.atlassian.net/browse/KATA-2567|KATA-2567>: Check Komatsu repo dependencies for PyArch development
```

## AlexD Notification

After generating the Slack content, send a direct message to AlexD with:

```
Cursor output for <meeting title> (<date>):

[Include the full thread starter and reply content above]
```

**Gemini Link Handling**: If no Gemini notes link was provided, the Slack message will omit the Gemini notes line entirely (as per the rules).
