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

## Workflow

### Step 1: Load keyword filter

Read `.claude/skills/gmail-inbox/keyword-filter.json`. Extract the `keywords` array.

### Step 2: Search Gmail for unprocessed threads

Call `mcp__claude_ai_Gmail__search_threads` with:
- `query`: `from:gemini-notes@google.com newer_than:2d -label:gemini-auto-processed`
- `pageSize`: 20

The `-label:gemini-auto-processed` filter ensures each thread is processed at most once across all runs.

### Step 3: Filter by keywords

For each thread, check if the subject contains any keyword from the filter (case-insensitive substring). Skip non-matching threads. If none pass, stop silently.

### Step 4: For each qualifying thread

#### 4a: Extract the Google Docs transcript URL

**Critical**: Gemini notes emails embed the "Open meeting notes" link as an HTML hyperlink. The `plaintextBody` from `mcp__claude_ai_Gmail__get_thread` does NOT contain the URL. Do not try to parse it.

Instead, use Google Drive:

1. Strip the `"Notes: "` prefix and date suffix from the subject to get the meeting name.
   - e.g. `Notes: "Toolchain Weekly Sync" Apr 22, 2026` → `Toolchain Weekly Sync`
2. Call `mcp__claude_ai_Google_Drive__list_recent_files`.
3. Find the file titled `"<Meeting Name> - YYYY/MM/DD HH:MM PDT - Notes by Gemini"`.
4. From the `contentSnippet`, find the Transcript tab URL: a link matching `edit?usp=drive_web&tab=t.<id>` under the "Meeting records / Transcript" section.
5. Use the Transcript tab URL if found. Fall back to the file's `viewUrl` (Notes tab) if not.

If no matching file is found in Drive, send a Slack DM warning (see Step 4e) and apply the processed label anyway to avoid infinite retries.

#### 4b: Run meeting-plan Phase 1

Read and follow `.claude/skills/meeting-plan/SKILL.md`.

Pass the Google Docs URL as the sole input. Run Phase 1 fully:
- Create workspace under `workspaces/YYYY-MM-DD/<slug>/`
- Write `transcript.md` (single-line URL with transcript tab), `gemini-link.txt`
- Generate `analysis.md`, `research.md`, `tickets.md`

**Stop before Phase 2.** Do not create JIRA tickets, post Slack summaries, or sync TickTick.

#### 4c: Write status.md

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

#### 4d: Apply processed label

Call `mcp__claude_ai_Gmail__list_labels` to find the ID of `gemini-auto-processed`. If the label does not exist, create it with `mcp__claude_ai_Gmail__create_label`.

Call `mcp__claude_ai_Gmail__label_thread` with the thread ID and label ID.

#### 4e: Send Slack DM

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

### Error handling

- **Drive lookup fails**: DM the user with `"Could not find Google Doc for: <subject>"`, apply the processed label, continue.
- **meeting-plan Phase 1 fails**: DM the user with `"meeting-plan failed for: <subject> — <error>"`. Do NOT apply the processed label (retry next run).
- **Slack DM fails**: Log and continue. Still apply the processed label.
- **One thread fails**: Continue processing remaining threads independently.
- **keyword-filter.json missing or malformed**: DM the user with a warning and stop.

## Ad-hoc usage

To run this manually against the current inbox:

```
/gemini-notes-processor
```

To run against a specific meeting URL directly (skipping Gmail scan):

```
/gemini-notes-processor https://docs.google.com/document/d/.../edit?tab=t....
```

When a URL is provided directly, skip Steps 1-3 and go straight to Step 4b with that URL.

## Sharing with other users

To adapt this skill for a different user:

1. Update the Slack DM recipient in Step 4e (replace `alexanderdelre` with the target user's Slack handle).
2. Update `.claude/skills/gmail-inbox/keyword-filter.json` with the meetings they care about.
3. The `workspaces/` output path and meeting-plan skill references are relative to the repo root and need no changes.
