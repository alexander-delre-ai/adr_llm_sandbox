# /meeting_plan

Accept a Google Gemini meeting transcript and produce a full meeting analysis, action plan, and JIRA ticket payloads.

## Input

The transcript may be provided as:
- Inline text pasted directly in the message
- A file path - read the file using the Read tool
- A URL - fetch using the appropriate fetch tool

If no transcript is provided, ask: "Please paste the meeting transcript or provide a file path."

## Steps

1. Accept the transcript using one of the input methods above
2. Switch to Plan mode so the analysis is collaborative before any artifacts are created
3. Read and follow `.cursor/skills/meeting-analysis-and-planning/SKILL.md` - execute all seven steps against the transcript
4. Return the full analysis using this structure:

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

5. After the analysis, ask: "Would you like me to finalize the JIRA ticket payloads? If yes, please confirm the **epic ID** and **release** (or provide them per ticket)."

If the user confirms, ask which project space applies (KATA or AVP) and collect any missing mandatory fields (`epic_id`, `release`). Invoke `kata-jira-task-creation` or `avp-jira-task-creation` accordingly for each action item. Output one validated JSON payload per fenced block, labeled with the ticket name.

## Step 6 - Save workspace

After the analysis and any JIRA payloads are complete, the `meeting-analysis-and-planning` skill will automatically:
1. Invoke `meeting-workspace` to persist all artifacts to `/workspaces/<date>-<meeting-slug>/`
2. Ask the user if they would like a Slack summary - only invoke `meeting-slack-summary` if they confirm

Confirm the saved workspace path to the user when done.
