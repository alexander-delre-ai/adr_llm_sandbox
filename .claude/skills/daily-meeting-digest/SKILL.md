---
name: daily-meeting-digest
description: Sends a daily Slack DM to AlexD summarizing all meetings processed by gemini-notes-processor today. Links back to each per-meeting Slack DM. Runs automatically at 5pm PDT Mon-Fri via remote routine. Skip if no meetings were processed today.
---

# Daily Meeting Digest

Scans today's `workspaces/2026.WW/YYYY-MM-DD/` directory for meetings auto-processed by `gemini-notes-processor`, then sends a single consolidated Slack DM to `alexanderdelre` with a summary and a link back to each per-meeting message.

## Workflow

### Step 1: Determine today's date

Use today's date in `YYYY-MM-DD` format (e.g. `2026-04-23`).

### Step 2: Find today's processed workspaces

Compute the year.week number (YYYY.WW) for today (zero-padded, e.g. W17). Check if `workspaces/2026.WW/<today>/` exists. If not, stop silently — nothing was processed today.

List all subdirectories under `workspaces/2026.WW/<today>/`. For each, check if `slack-dm.json` exists. Only include workspaces that have a `slack-dm.json` (written by `gemini-notes-processor` after the per-meeting DM was sent).

If no subdirectories have `slack-dm.json`, stop silently.

### Step 3: Build the meeting list

For each qualifying workspace, read:
- `status.md` — extract the meeting title from the `# Phase 2 Continuation: <title>` heading
- `slack-dm.json` — extract `channel` and `ts`
- `tickets.md` — count how many JIRA-tracked items (`tracking: jira` or `tracking: both`) and how many slack-only items

Construct a Slack message link for each meeting using the format:
`https://appliedintuition.slack.com/archives/<channel>/p<ts_without_dot>`

Where `<ts_without_dot>` is the `ts` value with the `.` removed (e.g. `1745432100.123456` → `1745432100123456`).

### Step 4: Send digest DM

Look up the Slack user ID for `alexanderdelre` via `mcp__claude_ai_Slack__slack_search_users` (query: `alexanderdelre`).

Send a DM:

```
:calendar: *Meeting digest — <Day, Month DD>*

<N> meeting(s) processed today:

• *<Meeting Title 1>* — <X> JIRA tickets, <Y> Slack-only items — <Slack DM link>
• *<Meeting Title 2>* — <X> JIRA tickets, <Y> Slack-only items — <Slack DM link>

To continue Phase 2 for any meeting, open Claude Code and run `/meeting-plan resume workspaces/2026.WW/<date>/<slug>/`
```

If only one meeting was processed, use singular "meeting" in the header.

## Error handling

- If `slack-dm.json` is malformed for a workspace, include the meeting in the digest but note "DM link unavailable" instead of the link.
- If the digest DM fails to send, stop — do not retry (the next daily run will include today's meetings if their workspaces still lack a `phase2-complete` marker).
- Never send a digest if no meetings were processed — do not send an empty or "no meetings today" message.

## Ad-hoc usage

To run manually for today:

```
/daily-meeting-digest
```

To run for a specific date:

```
/daily-meeting-digest 2026-04-22
```
