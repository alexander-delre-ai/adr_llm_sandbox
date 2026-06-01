---
name: meeting-analysis
description: Analyzes meeting content (transcripts or summaries) to extract context, decisions, themes, unresolved questions, and action items. Creates structured analysis.md file. Use for processing any meeting content into organized analysis format.
---

# Meeting Analysis

Processes meeting content (full transcripts or AI-generated summaries) to create structured analysis with context, decisions, themes, questions, risks, follow-ups, and a prioritized action plan.

## Input Requirements

- **Meeting content**: Full transcript or AI summary
- **Output location**: Directory path where analysis.md should be created (format: workspaces/YYYY-MM-DD/meeting-name/)
- **Meeting metadata**: Title, date, participants (extracted from content)

## Workflow

### Step 1 - Extract meeting context

**First, identify the content type:**
- **Full Transcript**: Contains detailed conversation with speaker names, timestamps, and dialogue
- **Gemini Summary**: AI-generated summary with structured sections (Summary, Details, Next Steps)

Pull these fields based on content type:

| Field | Full Transcript | Gemini Summary |
|-------|----------------|----------------|
| Meeting title | explicit title, recurring series name, or infer from agenda | Look for title at top or in "Invited" section |
| Date & time | timestamp in transcript metadata | Date at beginning (e.g., "Mar 10, 2026") |
| Participants | speaker names/handles from dialogue (exclude meeting rooms) | Parse "Invited" list, filter out meeting rooms and email domains |
| Meeting location | identify conference room names in participant list | Extract from "Invited" section or infer from context |
| Stated objective | agenda items or opening statement | Extract from "Summary" section or main topics |

**Participant filtering rules:**
- Remove conference room names from the participants list
- For Gemini summaries, strip email domains (e.g., "nuthan.sabbani@global.komatsu" -> "Nuthan Sabbani")
- For full transcripts, only include names that appear as speakers in the dialogue
- For Gemini summaries, flag any invited names that never appear in the content body with `(invited, no participation noted)`

### Step 2 - Identify key decisions

A decision is a statement of agreement, approval, or chosen direction.

**Full Transcript Signals**: "we decided", "agreed to", "going with", "approved", "confirmed"
**Gemini Summary**: Look for definitive statements in "Summary" and "Details" sections

Output as a numbered list: `Decision N: <one-sentence summary>`

### Step 3 - Identify discussion themes

Group related content into 3-7 named themes. Each theme gets:
- A short label (2-4 words)
- 2-4 concise bullet points capturing the specific talking points raised

Keep bullet points brief enough to include in a Slack message (one line each, no full sentences needed).

Do **not** include action items, commitments, or "I'll do X" statements in themes. Those belong in the prioritized action plan (Step 6).

**Full Transcript**: Group conversation segments by topic
**Gemini Summary**: Use section headers and topic groupings from "Details" section

### Step 4 - Identify unresolved questions

Capture open questions, blockers, and deferred topics.

**Full Transcript Signals**: "we need to figure out", "TBD", "who owns", "not sure yet", "follow up on"
**Gemini Summary**: Look for uncertainty language, questions raised, or items marked for future discussion

Output as a bulleted list with the responsible person (if named) in brackets.

### Step 5 - Identify risks and blockers

Capture anything raised as a risk, blocker, dependency, or concern that could impede progress.

**Signals**: "blocked by", "waiting on", "risk", "concern", "dependency", "this could be a problem", "we might be stuck"

Output as a bulleted list. For each item include:
- The risk or blocker (one line)
- Owner or affected party in brackets (if named)
- Severity: `High` / `Medium` / `Low`

### Step 6 - Build prioritized action plan

**For Full Transcripts**: Look for commitment language ("I'll", "we need to", "action item")
**For Gemini Summaries**: Check "Suggested next steps" section and action-oriented items in "Details"

For each action item extract:
- **What**: clear imperative description of the work
- **Who**: assignee (if named; otherwise "Unassigned")
- **When**: due date or sprint (if mentioned)
- **Priority**: `High` / `Medium` / `Low` based on urgency language or context. Default to `Low` when no urgency signals are present; append `(inferred)` to flag it.
- **Type**: `Technical` / `Coordination` / `Documentation` / `Research`

Output as a markdown table sorted by priority (High first):

| Proposed Action Item | Assignee | Priority | Due | Type |
|---------------------|----------|----------|-----|------|
| ...                 | ...      | High     | ... | Technical |
| ...                 | ...      | Low (inferred) | ... | Coordination |

### Step 7 - Slack summary block

Produce a compact, pre-formatted block suitable for pasting directly into Slack. No markdown headers; use plain Slack formatting only.

Structure:
```
*<Meeting Title> - <Date>*

*Themes*
- <theme label>: <key point>, <key point>
- <theme label>: <key point>, <key point>
...

*Top Action Items*
1. <action> (@assignee)
2. <action> (@assignee)
3. <action> (@assignee)

*Risks/Blockers*
- <risk or blocker> [owner]

*Follow-ups*
- <follow-up meeting or sync>
```

Keep the entire block under 20 lines. If no risks or follow-ups exist, omit those sections.

### Step 8 - Identify follow-up meetings

Capture any meetings, reviews, or syncs that were agreed to be scheduled.

**Signals**: "let's set up a meeting", "we should sync on", "schedule a review", "I'll send an invite", "follow-up with"

Output as a bulleted list. For each item include:
- Purpose of the meeting
- Who should attend (if named)
- Suggested timing (if mentioned)

If none were mentioned, write: `No follow-up meetings identified.`

## Output Format

Create `analysis.md` file with this structure:

```markdown
# Meeting Analysis: <title> (<date>)

## 1. Meeting Context
[Context details]

## 2. Key Decisions
[Numbered decisions list]

## 3. Discussion Themes
[Named themes with bullet points — no action items]

## 4. Unresolved Questions
[Bulleted questions with owners]

## 5. Risks and Blockers
[Bulleted risks with owners and severity]

## 6. Prioritized Action Plan
[Table without # column]

## 7. Slack Summary
[Compact Slack-ready block]

## 8. Follow-up Meetings
[Bulleted follow-up meetings or "No follow-up meetings identified."]
```

## Post-Review Update

After the user reviews and edits `tickets.md`, Section 6 of `analysis.md` must be updated to match the final ticket content:

1. Re-read the final `tickets.md` to capture user edits (title changes, priority adjustments, assignee updates, removed items)
2. Rewrite **Section 6 (Prioritized Action Plan)** table to reflect the reviewed tickets
3. Update **Section 7 (Slack Summary)** top action items to match

This ensures `analysis.md` remains the single source of truth after user review.

## Usage

This skill focuses purely on analysis and does not create tickets or workspaces. It produces a comprehensive analysis.md file that can be used by other workflows for ticket creation, planning, or documentation.

## Integration

- **Input**: Meeting content (transcript or summary)
- **Output**: Structured analysis.md file (updatable after ticket review)
- **Reusable**: Can be called from `meeting-plan`, standalone analysis, or other workflows
- **Consistent**: Always produces the same 8-section format
