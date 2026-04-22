---
name: meeting-slack-summary
description: Sub-skill of meeting-summary. Composes a single Slack message summarizing a completed meeting analysis and sends it to AlexD. Includes attendees, action items, and corresponding JIRA ticket links. Use after meeting-workspace has run and the workspace path is known.
---

# Meeting Slack Summary (sub-skill of meeting-summary)

**Parent**: `.cursor/skills/meeting-summary/SKILL.md`. This folder lives at `.cursor/skills/meeting-summary/meeting-slack-summary/`.

Produces a single Slack message summarizing the meeting and sends it directly to AlexD. Load this skill when the Slack step is needed; the main meeting text and `analysis.md` still come from the **meeting-summary** workflow (or a full `meeting_plan` run) before this step.

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
| User organization mapping | Read `user-mapping.md` in this skill directory |

If the workspace path is not yet known, run the `meeting-workspace` skill first.

**IMPORTANT**: Before processing attendees, read the `user-mapping.md` file in this skill directory to get the latest user organization assignments and known Slack IDs.

**Check for Google Doc link in workspace**:
- Read `transcript.md` in the workspace directory
- If it contains a single-line Google Docs URL, use it for inclusion in the Slack summary
- If it contains full transcript content (multi-line), there is no Google Doc link to include

## Slack Message Format

Single message (no thread):
```
*<DD/MM/YYYY>: <Meeting Title>*
**Komatsu Attendees:** <name>, <name>
**Applied Attendees:** <@slack_id>, <@slack_id>
<Google Doc link> (only include this line if URL is available)
**Action items:**
• <@slack_id or name>: <short description> (Slack-only items first)
• <@slack_id or name>: <short description> (more Slack items...)
• <@slack_id>: <https://jira-url|JIRA-KEY>: <short description> (assigned JIRA tickets)
• <https://jira-url|JIRA-KEY>: <short description> (unassigned JIRA tickets)
```

## Implementation Steps

1. **Check for Google Doc link in workspace**:
   - Read `transcript.md` in the workspace directory
   - If it contains a single-line Google Docs URL, store for inclusion in the message
   - If multi-line (full transcript), no Google Doc link to include

2. **Parse attendees by organization and find Slack IDs**:
   - **Reference user mapping**: Read `user-mapping.md` in this skill directory for comprehensive user organization assignments and known Slack IDs
   - **Filter out meeting rooms**: Remove entries with location codes (e.g., "Coulomb's Law (SVL-WCAL-HQ, FL3)")
   - **Komatsu attendees**: Use plain names (no Slack mentions)
     - Examples: Jonas Hageman, Mike Lemm, Joseph Boyer, Nuthan Sabbani, Joshua Rohman
   - **Applied attendees**: Use Slack mentions format `<@USER_ID>`
     - Known IDs: Alex Del Re (U063Y6FQA5V), Lauren Joyce (U07CNBCK53P)
   - **Name corrections**: "Ashley" should be "Ashli Forbes"
   - **Special cases**: "Coulomb's Law/Alex (SVL)" or "Alex (SVL)" refers to Alex Del Re
   - Use `slack_search_users` to find Slack user IDs for new Applied attendees not in mapping
   - Update user-mapping.md when new users are discovered

3. **Format the date and title**:
   - Convert from meeting date to DD/MM/YYYY format
   - Example: "Mar 6, 2026" -> "06/03/2026"
   - Bold the title line: `*06/03/2026: Meeting Title*`

4. **Generate single message**:
   - Combine title, attendees, Google Doc link (if available), and action items into one message
   - Only include Google Doc link line if URL is available from `transcript.md`

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
   - Update `user-mapping.md` with new information for future use

## Rules

- **Date format**: Always use DD/MM/YYYY format in the title line
- **Title line**: Use actual meeting title, not generic "Office hours". Bold with `*...*`
- **Attendee formatting**: Bold headers, comma-separated lists, Slack mentions for Applied attendees
- **Slack mentions**: Use `<@USER_ID>` format for Applied attendees, plain names for external
- **JIRA links**: Use Slack hyperlink format `<URL|TICKET-ID>` to show only ticket IDs as clickable links (KATA tickets only, exclude AVP mirrors)
- **Assignee format**: Separate assignee and ticket with colon, omit "Unassigned" entirely for unassigned tickets
- **Google Doc link**: Include as hyperlink `<URL|Meeting notes>` only if available from `transcript.md`, otherwise omit the line entirely
- **Action items**: Bold header, no extra spacing between lines, remove "(Slack tracking)" suffixes, order with Slack items first then JIRA tickets
- **Character limit**: Keep under Slack's 4000-character message limit
- **Single message**: Everything in one message, no threads

## Example Output

```
*06/03/2026: Komatsu <> VehicleOS Adaptive Architecture sync*
**Komatsu Attendees:** Nuthan Sabbani
**Applied Attendees:** <@U080A6CFRAQ>, <@U063Y6FQA5V>
<https://docs.google.com/document/d/example|Meeting notes>
**Action items:**
• <@U063Y6FQA5V>: Follow up on meeting scheduling
• <@U080A6CFRAQ>: <https://appliedint-katana.atlassian.net/browse/KATA-2563|KATA-2563>: Research schema migration support in PyArch persistency module
• Nuthan Sabbani: <https://appliedint-katana.atlassian.net/browse/KATA-2565|KATA-2565>: Provide detailed payload feature requirements
• <https://appliedint-katana.atlassian.net/browse/KATA-2567|KATA-2567>: Check Komatsu repo dependencies for PyArch development
```

## AlexD Notification

Send the message above directly to AlexD as a single DM using `slack_send_message` with `channel_id` set to `U063Y6FQA5V`.
