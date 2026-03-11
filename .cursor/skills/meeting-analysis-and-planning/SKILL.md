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
- [ ] Step 6: Create JIRA tickets via MCP
- [ ] Step 7: Build prioritized action plan
- [ ] Step 8: Save workspace
- [ ] Step 9: Compose Slack summary (optional)
```

---

## Meeting Room Recognition

Applied uses well-known scientists and their associated work to identify conference rooms. When parsing attendee names, recognize these patterns:

**Known Meeting Rooms:**
- **Coulomb's Law** - Physics conference room
- **Newton** - Physics conference room  
- **Einstein** - Physics conference room
- **Faraday** - Physics conference room
- **Maxwell** - Physics conference room
- **Planck** - Physics conference room
- **Bohr** - Physics conference room
- **Heisenberg** - Physics conference room

**Recognition Pattern**: `<Scientist Name> (<Location Code>, <Building>)`
- Example: "Coulomb's Law (SVL-WCAL-HQ, FL3)" = Meeting room, not attendee
- If uncertain about a name, ask the user: "Is [Name] a meeting room or attendee?"

---

## Clarifying Questions Strategy

Throughout the analysis, especially in Steps 4-6, ask clarifying questions when:

- **Action items are vague**: "Research X" without clear deliverables
- **Ownership is unclear**: Multiple people mentioned or no clear assignee
- **Priorities conflict**: Everything seems urgent or no clear ranking
- **Scope is ambiguous**: "Improve Y" without specific success criteria
- **Dependencies are unclear**: Tasks that may block each other
- **Timelines are missing**: No clear deadlines or milestones mentioned

**Plan Mode Advantage**: Use this collaborative phase to resolve ambiguities before creating tickets.

---

### Step 1 - Extract meeting context

Pull these fields from the transcript header or opening minutes:

| Field | What to look for |
|-------|-----------------|
| Meeting title | explicit title, recurring series name, or infer from agenda |
| Date & time | timestamp in transcript metadata |
| Participants | speaker names/handles listed or inferred from dialogue (exclude meeting rooms) |
| Meeting location | identify conference room names (e.g., "Coulomb's Law (SVL-WCAL-HQ, FL3)") |
| Stated objective | agenda items or opening statement of purpose |

**Important**: Filter out meeting room names from participants list. Meeting rooms follow the pattern of scientist names with location codes.

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

### Step 6 - Plan JIRA tickets (Review Phase)

**Initial Mode**: Present proposed JIRA tickets for user review.

**Important**: Before finalizing ticket proposals, ask clarifying questions about:
- Unclear action items or vague requirements
- Missing assignees or ownership
- Ambiguous priorities or deadlines
- Scope boundaries or acceptance criteria
- Dependencies between tasks

For each action item, create a ticket proposal with:
- **Summary**: Derived from the task's **What** field
- **Description**: Task context from transcript
- **Priority**: Mapped from task's Priority field (P0, P1, P2, P3)
- **Assignee**: From task's Who field (ask if unclear)
- **Theme**: From task's Theme field
- **Ticket Type**: Identify if documentation/tutorial vs general task

Present tickets in a reviewable format:
```
## Proposed JIRA Tickets

### Ticket 1: [Summary]
- **Priority**: P1
- **Assignee**: [Name]  
- **Type**: Documentation (→ KATA-2226) / General (→ User Epic)
- **Description**: [Context from meeting]

### Ticket 2: [Summary]
...
```

**Execution Phase**: Only create actual tickets after user confirmation.

When user confirms ticket creation:
1. Ask for project space (KATA/AVP), epic ID, and release
2. Route documentation tickets to KATA-2226 automatically
3. Use MCP integration to create real tickets
4. Apply proper field mappings and required fields

---

### Step 7 - Build prioritized action plan

Output a markdown table sorted by priority (P1 first):

| # | Proposed Ticket | Assignee | Priority | Due | Type | Notes |
|---|-----------------|----------|----------|-----|------|-------|
| 1 | ...             | ...      | P1       | ... | Doc  | → KATA-2226 |
| 2 | ...             | ...      | P1       | ... | General | → User Epic |

Follow the table with a **Next steps** section: 3-5 bullet points the team should act on immediately.

**End with clarification and confirmation**:

First, ask any clarifying questions about unclear items, then:

"Would you like me to create these JIRA tickets? If yes, please confirm the project space (KATA/AVP), epic ID for general tickets, and target release."

---

### Step 8 - Save workspace (Post-Execution)

**Only execute after JIRA tickets are created** (if user confirms).

Read and follow `.cursor/skills/meeting-workspace/SKILL.md`.

Use `workspaces/` within the current repository.

Pass it:
- The original transcript
- The full analysis output from Steps 1-7
- All JIRA ticket metadata with actual ticket keys and URLs
- A summary of key decisions made during the session

**If tickets not created**: Save analysis with proposed ticket plans only.

### Step 9 - Compose Slack summary (automatic)

After workspace creation, automatically ask: "Would you like me to generate a Slack message for the office hours thread?"

If yes, read and follow `.cursor/skills/meeting-slack-summary/SKILL.md`.

Pass it:
- Meeting title and date (from Step 1) 
- Attendees (from Step 1) - categorize by organization
- Workspace path (from Step 8)
- Action items with assignee and priority (from Step 5)
- JIRA ticket keys and URLs (from Step 6, if any)
- Ask for Gemini notes link if available

The skill will generate both the thread starter and reply content in the office hours format.

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
