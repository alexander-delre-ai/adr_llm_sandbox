# /batch_meeting_plan

**Mode: Agent**

Process multiple meeting Google Docs links in parallel. Each link gets its own background agent running the full `meeting_plan` Phase 1 workflow (fetch, analyze, research, stage tickets). All meetings pause for review before JIRA ticket creation.

## Usage

Paste Google Docs links (one per line):

```
/batch_meeting_plan
https://docs.google.com/document/d/.../edit?tab=...
https://docs.google.com/document/d/.../edit
https://docs.google.com/document/d/...
```

## Instructions

Read and follow the skill at `~/.cursor/skills/batch-meeting-plan/SKILL.md`.
