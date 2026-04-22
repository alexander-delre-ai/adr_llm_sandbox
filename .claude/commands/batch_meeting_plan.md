---
description: Process multiple meeting Google Docs links in parallel - each link launches a separate agent running meeting_plan Phase 1 (fetch, analyze, research, stage tickets). All pause for review before JIRA creation.
---

# /batch_meeting_plan

Process multiple meeting Google Docs links in parallel. Each link gets its own background agent running the full `meeting_plan` Phase 1 workflow (fetch, analyze, research, stage tickets). All meetings pause for review before JIRA ticket creation.

## Usage

Paste Google Docs links (one per line) after the command:

```
/batch_meeting_plan
https://docs.google.com/document/d/.../edit?tab=...
https://docs.google.com/document/d/.../edit
https://docs.google.com/document/d/...
```

## Instructions

Read and follow `.claude/skills/batch-meeting-plan/SKILL.md` in this repository (subagent prompts reference `.claude/commands/meeting_plan.md`).
