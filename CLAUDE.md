# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

An AI workflow automation system for meeting analysis, JIRA ticket creation, and team collaboration. It uses **Agent Skills** under `.claude/skills/` (each workflow is typically `SKILL.md` plus scripts, JSON, and data) and MCP server integrations.

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

## Architecture

### Agent skills (`/.claude/skills/`)

Load the `SKILL.md` for the workflow you need. Paths are relative to the repository root.

| Skill | Primary `SKILL.md` | Purpose |
|-------|--------------------|--------|
| meeting-plan | [`.claude/skills/meeting-plan/SKILL.md`](.claude/skills/meeting-plan/SKILL.md) | Full meeting workflow: analysis, research, tickets, JIRA, Slack, TickTick, doc share |
| meeting-summary | [`.claude/skills/meeting-summary/SKILL.md`](.claude/skills/meeting-summary/SKILL.md) | Transcript, file, or Google Doc to `analysis.md` only (no JIRA) |
| meeting-analysis | [`.claude/skills/meeting-analysis/SKILL.md`](.claude/skills/meeting-analysis/SKILL.md) | Extract decisions, action items, themes from transcripts |
| meeting-research | [`.claude/skills/meeting-research/SKILL.md`](.claude/skills/meeting-research/SKILL.md) | Slack, Confluence, JIRA, optional codebase research for meeting questions |
| meeting-workspace | [`.claude/skills/meeting-workspace/SKILL.md`](.claude/skills/meeting-workspace/SKILL.md) | Create persistent `workspaces/2026.WW/YYYY-MM-DD/{slug}/` |
| meeting-tickets | [`.claude/skills/meeting-tickets/SKILL.md`](.claude/skills/meeting-tickets/SKILL.md) | Stage editable JIRA ticket proposals in workspace |
| meeting-slack-summary | [`.claude/skills/meeting-summary/meeting-slack-summary/SKILL.md`](.claude/skills/meeting-summary/meeting-slack-summary/SKILL.md) | Slack office hours DMs to AlexD |
| jira-task-creation-KATA | [`.claude/skills/jira-task-creation-KATA/SKILL.md`](.claude/skills/jira-task-creation-KATA/SKILL.md) | Create JIRA tickets in KATA project |
| jira-task-creation-AVP | [`.claude/skills/jira-task-creation-AVP/SKILL.md`](.claude/skills/jira-task-creation-AVP/SKILL.md) | Create JIRA tickets in AVP project |
| daily-todos | [`.claude/skills/daily-todos/SKILL.md`](.claude/skills/daily-todos/SKILL.md) | Generate daily task lists from workspaces |
| daily-meeting-digest | [`.claude/skills/daily-meeting-digest/SKILL.md`](.claude/skills/daily-meeting-digest/SKILL.md) | End-of-day Slack DM summarizing all meetings auto-processed today |
| gemini-notes-processor | [`.claude/skills/gemini-notes-processor/SKILL.md`](.claude/skills/gemini-notes-processor/SKILL.md) | Automated Gmail scan: Gemini notes to meeting-plan Phase 1 + status.md |
| ticktick-sync | [`.claude/skills/ticktick-sync/SKILL.md`](.claude/skills/ticktick-sync/SKILL.md) | Sync todos to TickTick API |
| chat-keyword-insights | [`.claude/skills/chat-keyword-insights/SKILL.md`](.claude/skills/chat-keyword-insights/SKILL.md) | Transcript keyword insights to `insights/` |
| create-pr-with-jira | [`.claude/skills/create-pr-with-jira/SKILL.md`](.claude/skills/create-pr-with-jira/SKILL.md) | KATA ticket + GitHub PR link workflow |
| kata-sprint-ticket-factory | [`.claude/skills/kata-sprint-ticket-factory/SKILL.md`](.claude/skills/kata-sprint-ticket-factory/SKILL.md) | Sprint batch ticket creation |

**Note**: The `.claude/commands/` directory is not used. All workflow text lives in `SKILL.md` files under `.claude/skills/`.

### Workspaces (`/workspaces/`)

Persistent meeting artifacts organized by ISO week and date. Structure is `2026.WW/YYYY-MM-DD/{meeting-slug}/` where each meeting directory contains: `transcript.md`, `analysis.md`, `tickets.md`, JIRA metadata JSON files, and chat history.

### MCP Integrations

Defined in `~/.claude/settings.json`:

| Server key | Transport | Purpose | Tool prefix |
|---|---|---|---|
| `github` | Docker (github-mcp-server) | GitHub issues, PRs, context | `mcp__github__*` |
| `buildkite` | Docker (buildkite-mcp-server) | CI/CD pipelines | `mcp__buildkite__*` |
| `atlassian-mcp-jira-api-token` | SSE (mcp.atlassian.com) | KATA JIRA + Confluence | `mcp__kata-atlassian__*` |
| `avp-atlassian` | HTTP (mcp.atlassian.com) | AVP JIRA + Confluence | `mcp__avp-atlassian__*` |
| `Slack` | SSE (mcp.slack.com) | Slack messaging | `mcp__Slack__*` |
| `google-drive` | npx (@piotr-agier/google-drive-mcp) | Google Drive file access | `mcp__google-drive__*` |

**KATA Cloud ID**: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`
**AVP Cloud ID**: `6461690f-d275-4167-8055-cc3dc06e03f2` (site: `appliedintuition.atlassian.net`)

## Key Conventions

- **Workspace naming**: `2026.WW/YYYY-MM-DD/{slug}` (year.week prefix, then date directory with meeting slug subdirectory, lowercase, hyphens, max 60 chars for slug)
- **Ticket titles**: Imperative voice, 10-255 characters
- **KATA priorities**: P0-P3; **AVP priorities**: Highest/High/Medium/Low/Lowest
- **Story points**: Default to 0 (always requires explicit estimation)
- **Assignees**: Single person per task; default to "Unassigned"
- **Slack dates**: DD/MM/YYYY format

## Release Mapping (KATA)

Defined in `.claude/skills/jira-task-creation-KATA/release-mapping.json`:

| Release | Fix Version ID | Date |
|---------|----------------|------|
| 25.1 | 10000 | 2025-09-26 |
| 25.2 | 10001 | 2025-12-26 |
| 25.3 | 10036 | 2026-04-03 |
| 26.1 | 10002 | 2026-06-26 |
| 26.2 | 10003 | 2026-09-18 |
