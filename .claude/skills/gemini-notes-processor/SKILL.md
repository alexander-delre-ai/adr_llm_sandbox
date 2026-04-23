---
name: gemini-notes-processor
description: Scans Gmail for new Gemini meeting notes emails, filters by keyword, extracts the Google Docs transcript link, and runs meeting-plan Phase 1 to produce analysis.md, research.md, and tickets.md in a workspace. Writes status.md so a separate session can continue to Phase 2. Use for automated or ad-hoc processing of Gemini-generated meeting notes.
---

# Gemini Notes Processor

Scans Gmail for Gemini auto-generated meeting notes, extracts the transcript link from Google Drive, runs meeting-plan Phase 1 autonomously, and generates a `status.md` resumption file so a different session or user can continue to Phase 2 (JIRA, Slack, TickTick) at any time.

## Configuration

Edit `.claude/skills/gmail-inbox/keyword-filter.json` to control which meetings are processed:

```json
{
  "description": "Subjects containing any keyword (case-insensitive) trigger meeting-plan.",
  "keywords": ["Office Hours", "Weekly", "Toolchain", "Middleware"]
}
```

The processor checks this file on every run. Adding a keyword takes effect immediately on the next run.

## State file

`.claude/skills/gemini-notes-processor/last-run.json` tracks when the skill last ran:

```json
{
  "last_run_iso": "2026-04-23T16:40:00Z",
  "last_run_gmail_date": "2026/04/23"
}
```

On first run (file absent or malformed), fall back to `newer_than:7d`. After all threads are processed, overwrite this file with the current UTC timestamp and commit + push it so future runs (local or remote) inherit the correct window.

## Workflow

### Step 1: Load last-run timestamp

Read `.claude/skills/gemini-notes-processor/last-run.json`.

- If the file exists and is valid, extract `last_run_gmail_date` (format `YYYY/MM/DD`). Use `after:<last_run_gmail_date>` as the date filter in Step 3.
- If the file is missing or malformed, use `newer_than:7d` as the fallback date filter.

### Step 2: Load keyword filter

Read `.claude/skills/gmail-inbox/keyword-filter.json`. Extract the `keywords` array.

### Step 3: Search Gmail for unprocessed threads

Call `mcp__claude_ai_Gmail__search_threads` with:
- `query`: `from:gemini-notes@google.com <date_filter> -label:gemini-auto-processed`
  where `<date_filter>` is `after:YYYY/MM/DD` from Step 1 (or `newer_than:7d` on first run)
- `pageSize`: 20

The `-label:gemini-auto-processed` filter ensures each thread is processed at most once even if the date window overlaps.

### Step 4: Filter by keywords

For each thread, check if the subject contains any keyword from the filter (case-insensitive substring). Skip non-matching threads. If none pass, skip to Step 6 (still write last-run.json).

### Step 5: For each qualifying thread

#### 5a: Check for existing workspace

Derive the workspace slug from the meeting name (extracted from the email subject: strip `"Notes: "` prefix and date suffix, lowercase, replace spaces with hyphens, max 60 chars). Check if `workspaces/YYYY-MM-DD/<slug>/` already exists.

If the workspace directory exists: apply the `gemini-auto-processed` label to the thread (step 5d) and skip to the next thread. Do not run Phase 1 again.

#### 5b: Extract the Google Docs transcript URL

**Critical**: Gemini notes emails embed the "Open meeting notes" link as an HTML hyperlink. The `plaintextBody` from `mcp__claude_ai_Gmail__get_thread` does NOT contain the URL. Do not try to parse it.

Use the email subject as the source of truth for the meeting name, then find the file in Google Drive:

1. Extract the meeting name from the email subject: strip the `"Notes: "` prefix and the trailing date (e.g. `Notes: "Toolchain Weekly Sync" Apr 22, 2026` → `Toolchain Weekly Sync`).
2. Call `mcp__claude_ai_Google_Drive__list_recent_files`. Look for a file whose title contains both the meeting name and `"Notes by Gemini"`.
3. If not found in recent files, call `mcp__claude_ai_Google_Drive__search_files` with the meeting name as the query and filter results for files whose title contains `"Notes by Gemini"`.
4. From the matched file's `contentSnippet`, find the Transcript tab URL: a link matching `edit?usp=drive_web&tab=t.<id>` under the "Meeting records / Transcript" section.
5. Use the Transcript tab URL if found. Fall back to the file's `viewUrl` (Notes tab) if not.

If no matching file is found after both lookups, send a Slack DM warning (see step 5f) and apply the processed label anyway to avoid infinite retries.

#### 5c: Run meeting-plan Phase 1

Read and follow `.claude/skills/meeting-plan/SKILL.md`.

Pass the Google Docs URL as the sole input. Run Phase 1 fully:
- Create workspace under `workspaces/YYYY-MM-DD/<slug>/`
- Write `transcript.md` (single-line URL with transcript tab), `gemini-link.txt`
- Generate `analysis.md`, `research.md`, `tickets.md`

**Stop before Phase 2.** Do not create JIRA tickets, post Slack summaries, or sync TickTick.

#### 5d: Write status.md

After Phase 1 completes, write `workspaces/YYYY-MM-DD/<slug>/status.md` using this template:

```markdown
# Phase 2 Continuation: <Meeting Title>

**Created**: <ISO date> by gemini-notes-processor (automated)
**Status**: Phase 1 complete — ready for Phase 2
**Workspace**: `workspaces/<YYYY-MM-DD>/<slug>/`

## Phase 1 artifacts
- [x] transcript.md
- [x] gemini-link.txt
- [x] analysis.md
- [x] research.md
- [x] tickets.md

## Google Docs transcript
<Google Docs URL>

## Resume Phase 2

Open Claude Code in this project and send:

```
/meeting-plan resume workspaces/<YYYY-MM-DD>/<slug>/
```

Or paste directly:

```
Continue meeting-plan Phase 2 for the workspace at workspaces/<YYYY-MM-DD>/<slug>/. Phase 1 is complete — analysis.md, research.md, and tickets.md are staged. Review tickets.md if needed, then proceed with JIRA ticket creation, Slack summary, Google Doc sharing, and TickTick sync.
```
```

#### 5e: Apply processed label

Call `mcp__claude_ai_Gmail__list_labels` to find the ID of `gemini-auto-processed`. If the label does not exist, create it with `mcp__claude_ai_Gmail__create_label`.

Call `mcp__claude_ai_Gmail__label_thread` with the thread ID and label ID.

#### 5f: Send Slack DM

Look up the Slack user ID for `alexanderdelre` via `mcp__claude_ai_Slack__slack_search_users` (query: `alexanderdelre`). Send a DM:

```
:robot_face: *New meeting notes processed:* <meeting title>

:memo: *Notes link:* <Google Docs URL>

:white_check_mark: *Proposed action items:*
• [PRIORITY] Title — Assignee
(one line per item from tickets.md)

:file_folder: Workspace: workspaces/<date>/<slug>/

To continue Phase 2: open Claude Code and run `/meeting-plan resume workspaces/<date>/<slug>/`
```

After sending, capture the response `channel` and `ts` fields and write them to `workspaces/YYYY-MM-DD/<slug>/slack-dm.json`:

```json
{
  "channel": "<channel_id>",
  "ts": "<message_timestamp>"
}
```

This file is read by the daily digest routine to link back to this message.

### Step 6: Write last-run.json and commit

After all threads are processed (whether or not any matched), write the current UTC time to `.claude/skills/gemini-notes-processor/last-run.json`:

```json
{
  "last_run_iso": "<current UTC ISO 8601 timestamp>",
  "last_run_gmail_date": "<current date as YYYY/MM/DD>"
}
```

Then commit and push:

```bash
git add .claude/skills/gemini-notes-processor/last-run.json
git commit -m "chore: update gemini-notes-processor last-run timestamp"
git push
```

If the commit or push fails (e.g. no GitHub App access), write the file to disk only. The `gemini-auto-processed` label still prevents reprocessing even without the timestamp update.

### Error handling

- **Drive lookup fails**: DM the user with `"Could not find Google Doc for: <subject>"`, apply the processed label, continue.
- **meeting-plan Phase 1 fails**: DM the user with `"meeting-plan failed for: <subject> — <error>"`. Do NOT apply the processed label (retry next run).
- **Slack DM fails**: Log and continue. Still apply the processed label.
- **One thread fails**: Continue processing remaining threads independently.
- **keyword-filter.json missing or malformed**: DM the user with a warning and stop (still write last-run.json).

## Ad-hoc usage

To run this manually against the current inbox:

```
/gemini-notes-processor
```

To run against a specific meeting URL directly (skipping Gmail scan):

```
/gemini-notes-processor https://docs.google.com/document/d/.../edit?tab=t....
```

When a URL is provided directly, skip Steps 1-5 and go straight to Step 5b with that URL. Still write `last-run.json` at the end (Step 6).

## Sharing with other users

To adapt this skill for a different user:

1. Update the Slack DM recipient in Step 4e (replace `alexanderdelre` with the target user's Slack handle).
2. Update `.claude/skills/gmail-inbox/keyword-filter.json` with the meetings they care about.
3. The `workspaces/` output path and meeting-plan skill references are relative to the repo root and need no changes.
