---
name: meeting-analysis
description: Analyzes meeting content (transcripts or summaries) to extract context, decisions, themes, unresolved questions, and action items. Creates structured analysis.md file. Use for processing any meeting content into organized analysis format.
---

# Meeting Analysis

Processes meeting content (full transcripts or AI-generated summaries) to create structured analysis with context, decisions, themes, questions, and action items.

## Input Requirements

- **Meeting content**: Full transcript or AI summary
- **Output location**: Directory path where analysis.md should be created
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

**Important**: 
- Filter out meeting room names from participants list (scientist names with location codes)
- For Gemini summaries, remove email domains from names (e.g., "nuthan.sabbani@global.komatsu" → "Nuthan Sabbani")

### Step 2 - Identify key decisions

A decision is a statement of agreement, approval, or chosen direction.

**Full Transcript Signals**: "we decided", "agreed to", "going with", "approved", "confirmed"
**Gemini Summary**: Look for definitive statements in "Summary" and "Details" sections

Output as a numbered list: `Decision N: <one-sentence summary>`

### Step 3 - Identify discussion themes

Group related content into 3-7 named themes. Each theme gets:
- A short label (2-4 words)
- A one-sentence description of what was discussed

**Full Transcript**: Group conversation segments by topic
**Gemini Summary**: Use section headers and topic groupings from "Details" section

### Step 4 - Identify unresolved questions

Capture open questions, blockers, and deferred topics.

**Full Transcript Signals**: "we need to figure out", "TBD", "who owns", "not sure yet", "follow up on"
**Gemini Summary**: Look for uncertainty language, questions raised, or items marked for future discussion

Output as a bulleted list with the responsible person (if named) in brackets.

### Step 5 - Extract actionable tasks

**For Full Transcripts**: Look for commitment language ("I'll", "we need to", "action item")
**For Gemini Summaries**: Check "Suggested next steps" section and action-oriented items in "Details"

For each action item extract:
- **What**: clear imperative description of the work
- **Who**: assignee (if named; otherwise "Unassigned")
- **When**: due date or sprint (if mentioned)
- **Priority**: `High` / `Medium` / `Low` based on urgency language or context
- **Theme**: which theme from Step 3 this belongs to

### Step 6 - Build prioritized action plan

Output a markdown table sorted by priority (High first):

| # | Proposed Action Item | Assignee | Priority | Due | Type | Notes |
|---|---------------------|----------|----------|-----|------|-------|
| 1 | ...                 | ...      | High     | ... | Coordination | → Slack tracking |
| 2 | ...                 | ...      | High     | ... | Technical | → JIRA ticket |

Follow the table with a **Next steps** section: 3-5 bullet points the team should act on immediately.

## Output Format

Create `analysis.md` file with this structure:

```markdown
# Meeting Analysis: <title> (<date>)

## 1. Meeting Context
[Context details]

## 2. Key Decisions
[Numbered decisions list]

## 3. Discussion Themes
[Named themes with descriptions]

## 4. Unresolved Questions
[Bulleted questions with owners]

## 5. Action Items
[Detailed action items with metadata]

## 6. Prioritized Action Plan
[Table and next steps]
```

## Usage

This skill focuses purely on analysis and does not create tickets or workspaces. It produces a comprehensive analysis.md file that can be used by other workflows for ticket creation, planning, or documentation.

## Integration

- **Input**: Meeting content (transcript or summary)
- **Output**: Structured analysis.md file
- **Reusable**: Can be called from meeting-plan, standalone analysis, or other workflows
- **Consistent**: Always produces the same 6-section format