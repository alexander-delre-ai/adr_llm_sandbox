# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

An AI workflow automation system for meeting analysis, JIRA ticket creation, and team collaboration. It processes meeting transcripts into structured analysis, staged JIRA ticket proposals, and Slack summaries using Claude Code commands, assets under `.claude/skills/`, and MCP server integrations.

## Global Rules (Always Apply)

- Never use em-dashes in responses
- One story point equals one week of work

## Python Scripts

The only runnable code lives in `.claude/skills/`:

```bash
# TickTick auth setup
python3 .claude/skills/ticktick-sync/scripts/auth_setup.py

# TickTick todo sync
python3 .claude/skills/ticktick-sync/scripts/sync_todos.py

# Daily todo generation (parses workspaces, generates markdown)
bash .claude/skills/daily-todos/scripts/generate_todos.sh
```

No build system, linter, or test framework is configured.

## Auto-Commit Rule

When any file under `.claude/commands/`, `.claude/skills/`, or `.cursor/rules/` is created or modified, commit the change immediately after the edit is complete. Use a concise commit message describing what was updated (e.g., "update ticktick-sync scripts to remove assignee from task content"). Do not batch skill or command or rule changes with unrelated file changes.

## Architecture

### Claude Commands (`/.claude/commands/`)

Claude Code slash commands - invoke with `/command-name`. These are the primary way to run skills and workflows in Claude Code.

| Command | Purpose |
|---|---|
| `/meeting_plan` | Full meeting workflow orchestrator (analysis, tickets, JIRA, Slack) |
| `/meeting_summary` | Transcript, file, or Google Doc to `analysis.md` (no tickets, JIRA, or Slack) |
| `/meeting-analysis` | Extract decisions, action items, themes from transcripts |
| `/meeting-research` | Slack, Confluence, JIRA, optional codebase research for meeting questions |
| `/meeting-workspace` | Create persistent `workspaces/YYYY-MM-DD/{slug}/` directories |
| `/meeting-tickets` | Stage editable JIRA ticket proposals in workspace |
| `/meeting-slack-summary` | Slack office hours DMs; sub-skill of `meeting-summary` (path: `meeting-summary/meeting-slack-summary/`) |
| `/kata-jira-task-creation` | Create JIRA tickets in KATA project |
| `/avp-jira-task-creation` | Create JIRA tickets in AVP project |
| `/app-dev-k1-hw-ticket-creation` | K1 hardware batch manager ticket processing |
| `/daily-todos` | Generate daily task lists from workspaces |
| `/ticktick-sync` | Sync todos to TickTick API |

### Claude skills assets (`/.claude/skills/`)

Scripts, JSON mappings, env templates, and small reference files used by slash commands. Workflow instructions live in `.claude/commands/` only (no duplicate `SKILL.md` per feature), except `batch-meeting-plan/SKILL.md`, which `/batch_meeting_plan` loads directly.

### Workspaces (`/workspaces/`)

Persistent meeting artifacts organized by date. Structure is `YYYY-MM-DD/{meeting-slug}/` where each meeting directory contains: `transcript.md`, `analysis.md`, `tickets.md`, JIRA metadata JSON files, and chat history.

### MCP Integrations

- `mcp__kata-atlassian__*` — KATA JIRA project (tools: createJiraIssue, lookupJiraAccountId, getAccessibleAtlassianResources, etc.)
- `user-Slack` — Slack messaging
- `user-github` — GitHub
- `user-buildkite` — CI/CD

**KATA Cloud ID**: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`

## Key Conventions

- **Workspace naming**: `YYYY-MM-DD/{slug}` (date directory with meeting slug subdirectory, lowercase, hyphens, max 60 chars for slug)
- **Ticket titles**: Imperative voice, 10–255 characters
- **KATA priorities**: P0–P3; **AVP priorities**: Highest/High/Medium/Low/Lowest
- **Story points**: Default to 0 (always requires explicit estimation)
- **Assignees**: Single person per task; default to "Unassigned"
- **Slack dates**: DD/MM/YYYY format

## Release Mapping (KATA)

Defined in `.claude/skills/kata-jira-task-creation/release-mapping.json`:

| Release | Fix Version ID | Date |
|---|---|---|
| 25.1 | 10000 | 2025-09-26 |
| 25.2 | 10001 | 2025-12-26 |
| 25.3 | 10036 | 2026-04-03 |
| 26.1 | 10002 | 2026-06-26 |
| 26.2 | 10003 | 2026-09-18 |
