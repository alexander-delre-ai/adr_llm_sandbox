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
| User organization mapping | Read `.claude/skills/meeting-summary/meeting-slack-summary/user-mapping.md` |

If the workspace path is not yet known, run the `meeting-workspace` skill first.

**IMPORTANT**: Before processing attendees, read the `user-mapping.md` file at `.claude/skills/meeting-summary/meeting-slack-summary/user-mapping.md` to get the latest user organization assignments and known Slack IDs.

**Check for Gemini or Google Doc link in workspace**:
- Prefer `gemini-link.txt` in the workspace (single line URL) for the notes link line in Slack
- Else, if `transcript.md` exists and its **first non-empty line** is a single `https://docs.google.com/document/...` URL (whole file may be that one line), use that URL the same way
- If neither yields a URL, ask the user for a Gemini or Google Doc link (optional)

Ask the user for optional inputs (if not already provided):
- **Gemini notes link** - URL to the original meeting notes (if not available in workspace)
- **Attendee organization** - to separate Komatsu vs Applied attendees (use mapping file as primary reference)
- **Meeting room confirmation** - if uncertain whether a name is a meeting room or attendee

## Slack Message Format

### Top-level thread message:
```
🧵<DD/MM/YYYY>: <Meeting Title>
```

### Reply in thread:
```
**Komatsu Attendees:** <name>, <name>
**Applied Attendees:** <@slack_id>, <@slack_id>
<Gemini notes link> (only include this line if URL is provided)
**Action items:**
• <@slack_id or name>: <short description> (Slack-only items first)
• <@slack_id or name>: <short description> (more Slack items...)
• <@slack_id>: <https://jira-url|JIRA-KEY>: <short description> (assigned JIRA tickets)
• <https://jira-url|JIRA-KEY>: <short description> (unassigned JIRA tickets)
```

## Implementation Steps

1. **Check for Gemini link in workspace**:
   - Look for `gemini-link.txt` file in the workspace directory
   - If found, read the URL content for inclusion in Slack summary
   - Store for use in step 3 (message generation)

2. **Parse attendees by organization and find Slack IDs**:
   - **Reference user mapping**: Read `.claude/skills/meeting-summary/meeting-slack-summary/user-mapping.md` for comprehensive user organization assignments and known Slack IDs
   - **Filter out meeting rooms**: Remove entries with location codes (e.g., "Coulomb's Law (SVL-WCAL-HQ, FL3)")
   - **Komatsu attendees**: Use plain names (no Slack mentions)
     - Examples: Jonas Hageman, Mike Lemm, Joseph Boyer, Nuthan Sabbani, Joshua Rohman
   - **Applied attendees**: Use Slack mentions format `<@USER_ID>`
     - Known IDs: Alex Del Re (U063Y6FQA5V), Lauren Joyce (U07CNBCK53P)
   - **Name corrections**: "Ashley" should be "Ashli Forbes"
   - **Special cases**: "Coulomb's Law/Alex (SVL)" or "Alex (SVL)" refers to Alex Del Re
   - Use `slack_search_users` to find Slack user IDs for new Applied attendees not in mapping
   - Update `.claude/skills/meeting-summary/meeting-slack-summary/user-mapping.md` when new users are discovered

3. **Format the date and thread title**:
   - Convert from meeting date to DD/MM/YYYY format
   - Example: "Mar 6, 2026" -> "06/03/2026"
   - Add colon after date: `🧵06/03/2026: Meeting Title`

4. **Generate both messages**:
   - Top-level thread starter
   - Threaded reply with full details
   - Only include Gemini notes line if URL is provided

5. **Handle action items ordering and formatting**:
   - **Order**: List Slack-only items first, then JIRA tickets last
   - **Slack items**: `<@slack_id>: <description>` (no ticket link)
   - **JIRA items**:
     - If assigned: `<@slack_id>: <ticket_link>: <description>`
     - If unassigned: `<ticket_link>: <description>` (omit "Unassigned")
   - Use Slack hyperlink format: `<https://appliedint-katana.atlassian.net/browse/KATA-2563|KATA-2563>`
   - **IMPORTANT**: Only include KATA tickets in Slack summaries, exclude AVP documentation mirrors

6. **Send message to AlexD**:
   - After generating the Slack content, send a direct message to AlexD
   - Include the office hours thread content for posting
   - Provide context about the meeting and action items

7. **Update user mapping (if needed)**:
   - If new users were discovered during Slack ID lookup
   - If organizational assignments were clarified
   - Update `.claude/skills/meeting-summary/meeting-slack-summary/user-mapping.md` with new information
   - **Auto-commit**: If the file was changed, commit it immediately with message: `update user-mapping with attendees from <meeting-slug>`

## Rules

- **Date format**: Always use DD/MM/YYYY: format in the thread title
- **Thread title**: Use actual meeting title, not generic "Office hours"
- **Attendee formatting**: Bold headers, comma-separated lists, Slack mentions for Applied attendees
- **Slack mentions**: Use `<@USER_ID>` format for Applied attendees, plain names for external
- **JIRA links**: Use Slack hyperlink format `<URL|TICKET-ID>` to show only ticket IDs as clickable links (KATA tickets only, exclude AVP mirrors)
- **Assignee format**: Separate assignee and ticket with colon, omit "Unassigned" entirely for unassigned tickets
- **Gemini notes**: Include as hyperlink `<URL|Gemini notes>` only if provided, otherwise omit the line entirely
- **Action items**: Bold header, no extra spacing between lines, remove "(Slack tracking)" suffixes, order with Slack items first then JIRA tickets
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
<https://docs.google.com/document/d/example|Gemini notes>
**Action items:**
• <@U063Y6FQA5V>: Follow up on meeting scheduling
• <@U080A6CFRAQ>: <https://appliedint-katana.atlassian.net/browse/KATA-2563|KATA-2563>: Research schema migration support in PyArch persistency module
• Nuthan Sabbani: <https://appliedint-katana.atlassian.net/browse/KATA-2565|KATA-2565>: Provide detailed payload feature requirements
• <https://appliedint-katana.atlassian.net/browse/KATA-2567|KATA-2567>: Check Komatsu repo dependencies for PyArch development
```

## AlexD Notification

After generating the Slack content, send a direct message to AlexD with:

```
Cursor output for <meeting title> (<date>):

<thread starter>

<reply content - without "Reply content:" header>
```

**Gemini Link Handling**: If no Gemini notes link was provided, the Slack message will omit the Gemini notes line entirely (as per the rules).
