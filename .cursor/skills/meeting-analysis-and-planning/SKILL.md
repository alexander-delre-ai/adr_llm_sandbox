---
name: meeting-analysis-and-planning
description: Analyzes a meeting transcript to extract context, decisions, themes, unresolved questions, and action items. Converts action items into JIRA-ready tickets and builds a prioritized plan. Use when processing meeting notes, call transcripts, or Google Gemini meeting exports.
---

# Meeting Analysis and Planning

## Workflow

Work through each step in order. Use the checklist to track progress.

```
- [ ] Step 1: Extract meeting context
- [ ] Step 2: Identify key decisions
- [ ] Step 3: Identify discussion themes
- [ ] Step 4: Identify unresolved questions
- [ ] Step 5: Extract actionable tasks
- [ ] Step 6: Convert tasks to JIRA tickets
- [ ] Step 7: Build prioritized action plan
- [ ] Step 8: Save workspace
- [ ] Step 9: Compose Slack summary (optional)
```

---

### Step 1 - Extract meeting context

Pull these fields from the transcript header or opening minutes:

| Field | What to look for |
|-------|-----------------|
| Meeting title | explicit title, recurring series name, or infer from agenda |
| Date & time | timestamp in transcript metadata |
| Participants | speaker names/handles listed or inferred from dialogue |
| Stated objective | agenda items or opening statement of purpose |

---

### Step 2 - Identify key decisions

A decision is a statement of agreement, approval, or chosen direction.

Signals: "we decided", "agreed to", "going with", "approved", "confirmed".

Output as a numbered list: `Decision N: <one-sentence summary>`

---

### Step 3 - Identify discussion themes

Group related conversation segments into 3-7 named themes. Each theme gets:
- A short label (2-4 words)
- A one-sentence description of what was discussed

---

### Step 4 - Identify unresolved questions

Capture open questions, blockers, and deferred topics.

Signals: "we need to figure out", "TBD", "who owns", "not sure yet", "follow up on".

Output as a bulleted list with the responsible person (if named) in brackets.

---

### Step 5 - Extract actionable tasks

For each action item extract:
- **What**: clear imperative description of the work
- **Who**: assignee (if named; otherwise "Unassigned")
- **When**: due date or sprint (if mentioned)
- **Priority**: `High` / `Medium` / `Low` based on urgency language in transcript
- **Theme**: which theme from Step 3 this belongs to

---

### Step 6 - Convert tasks to JIRA tickets

First, ask the user which project space the tickets belong to:
- **KATA** - invoke `kata-jira-task-creation` (`.cursor/skills/kata-jira-task-creation/SKILL.md`)
- **AVP** - invoke `avp-jira-task-creation` (`.cursor/skills/avp-jira-task-creation/SKILL.md`)

If tickets belong to different spaces, ask per ticket or per group.

Read the relevant skill file before proceeding.

Gather mandatory fields:
- `epic_id` - must match the chosen space prefix (`KATA-` or `AVP-`); ask the user if not found in transcript
- `release` - ask the user if not found in transcript
- `name` - derive from the task's **What** field

Map optional fields:
- `description` from task context in transcript
- `priority` from task's Priority field
- `assignee` from task's Who field
- `labels` from task's Theme field (snake_cased)

Produce one JSON payload per ticket.

---

### Step 7 - Build prioritized action plan

Output a markdown table sorted by priority (High first):

| # | Ticket name | Assignee | Priority | Due | Epic | Release |
|---|-------------|----------|----------|-----|------|---------|
| 1 | ...         | ...      | High     | ... | ...  | ...     |

Follow the table with a **Next steps** section: 3-5 bullet points the team should act on immediately.

---

### Step 8 - Save workspace

Read and follow `.cursor/skills/meeting-workspace/SKILL.md`.

Pass it:
- The original transcript
- The full analysis output from Steps 1-7
- All JIRA ticket JSON payloads from Step 6
- A summary of key decisions made during the session

### Step 9 - Compose Slack summary (optional)

Ask the user: "Would you like a Slack message to share with your team?"

Only proceed if the user confirms. If yes, read and follow `.cursor/skills/meeting-slack-summary/SKILL.md`.

Pass it:
- Meeting title and date (from Step 1)
- Attendees (from Step 1)
- Workspace path (from Step 8)
- Action items with assignee and priority (from Step 5)
- JIRA ticket keys and URLs (from Step 6, if any)

---

## Output structure

Return all seven sections in order under a top-level heading:

```
# Meeting Analysis: <title> (<date>)

## 1. Meeting context
## 2. Key decisions
## 3. Discussion themes
## 4. Unresolved questions
## 5. Action items
## 6. JIRA tickets
## 7. Prioritized action plan
```
