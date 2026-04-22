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

## Auto-Commit Rule

When any file under `.claude/skills/` or `.cursor/rules/` is created or modified, commit the change immediately after the edit is complete. Use a concise commit message describing what was updated (e.g., "update ticktick-sync scripts to remove assignee from task content"). Do not batch skill or rule changes with unrelated file changes.

## Architecture

### Agent skills (`/.claude/skills/`)

Load the `SKILL.md` for the workflow you need. Paths are relative to the repository root.

| Skill | Primary `SKILL.md` | Purpose |
|-------|--------------------|--------|
| meeting-plan | [`.claude/skills/meeting-plan/SKILL.md`](.claude/skills/meeting-plan/SKILL.md) | Full meeting workflow: analysis, research, tickets, JIRA, Slack, TickTick, doc share |
| batch-meeting-plan | [`.claude/skills/batch-meeting-plan/SKILL.md`](.claude/skills/batch-meeting-plan/SKILL.md) | Parallel Phase 1 `meeting-plan` runs for multiple Google Docs links |
| meeting-summary | [`.claude/skills/meeting-summary/SKILL.md`](.claude/skills/meeting-summary/SKILL.md) | Transcript, file, or Google Doc to `analysis.md` only (no JIRA) |
| meeting-analysis | [`.claude/skills/meeting-analysis/SKILL.md`](.claude/skills/meeting-analysis/SKILL.md) | Extract decisions, action items, themes from transcripts |
| meeting-research | [`.claude/skills/meeting-research/SKILL.md`](.claude/skills/meeting-research/SKILL.md) | Slack, Confluence, JIRA, optional codebase research for meeting questions |
| meeting-workspace | [`.claude/skills/meeting-workspace/SKILL.md`](.claude/skills/meeting-workspace/SKILL.md) | Create persistent `workspaces/YYYY-MM-DD/{slug}/` |
| meeting-tickets | [`.claude/skills/meeting-tickets/SKILL.md`](.claude/skills/meeting-tickets/SKILL.md) | Stage editable JIRA ticket proposals in workspace |
| meeting-slack-summary | [`.claude/skills/meeting-summary/meeting-slack-summary/SKILL.md`](.claude/skills/meeting-summary/meeting-slack-summary/SKILL.md) | Slack office hours DMs to AlexD |
| kata-jira-task-creation | [`.claude/skills/kata-jira-task-creation/SKILL.md`](.claude/skills/kata-jira-task-creation/SKILL.md) | Create JIRA tickets in KATA project |
| avp-jira-task-creation | [`.claude/skills/avp-jira-task-creation/SKILL.md`](.claude/skills/avp-jira-task-creation/SKILL.md) | Create JIRA tickets in AVP project |
| app-dev-k1-hw-ticket-creation | [`.claude/skills/app-dev-k1-hw-ticket-creation/SKILL.md`](.claude/skills/app-dev-k1-hw-ticket-creation/SKILL.md) | K1 hardware batch manager ticket processing |
| daily-todos | [`.claude/skills/daily-todos/SKILL.md`](.claude/skills/daily-todos/SKILL.md) | Generate daily task lists from workspaces |
| ticktick-sync | [`.claude/skills/ticktick-sync/SKILL.md`](.claude/skills/ticktick-sync/SKILL.md) | Sync todos to TickTick API |
| chat-keyword-insights | [`.claude/skills/chat-keyword-insights/SKILL.md`](.claude/skills/chat-keyword-insights/SKILL.md) | Transcript keyword insights to `insights/` |
| create-pr-with-jira | [`.claude/skills/create-pr-with-jira/SKILL.md`](.claude/skills/create-pr-with-jira/SKILL.md) | KATA ticket + GitHub PR link workflow |
| kata-sprint-ticket-factory | [`.claude/skills/kata-sprint-ticket-factory/SKILL.md`](.claude/skills/kata-sprint-ticket-factory/SKILL.md) | Sprint batch ticket creation |
| remarkable-feature-request | [`.claude/skills/remarkable-feature-request/SKILL.md`](.claude/skills/remarkable-feature-request/SKILL.md) | Remarkable device feature requests |
| sync-check | [`.claude/skills/sync-check/SKILL.md`](.claude/skills/sync-check/SKILL.md) | Validate `SKILL.md` references point at existing paths |

**Note**: The `.claude/commands/` directory is not used. All workflow text lives in `SKILL.md` files under `.claude/skills/`.

### Workspaces (`/workspaces/`)

Persistent meeting artifacts organized by date. Structure is `YYYY-MM-DD/{meeting-slug}/` where each meeting directory contains: `transcript.md`, `analysis.md`, `tickets.md`, JIRA metadata JSON files, and chat history.

### MCP Integrations

Defined in `~/.claude/settings.json`:

| Server key | Transport | Purpose | Tool prefix |
|---|---|---|---|
| `github` | Docker (github-mcp-server) | GitHub issues, PRs, context | `mcp__github__*` |
| `buildkite` | Docker (buildkite-mcp-server) | CI/CD pipelines | `mcp__buildkite__*` |
| `atlassian-mcp-jira-api-token` | SSE (mcp.atlassian.com) | KATA JIRA + Confluence | `mcp__kata-atlassian__*` |
| `Slack` | SSE (mcp.slack.com) | Slack messaging | `mcp__Slack__*` |
| `google-drive` | npx (@piotr-agier/google-drive-mcp) | Google Drive file access | `mcp__google-drive__*` |

**KATA Cloud ID**: `eadd00c6-0d3f-4c89-99e3-ad95a0daaa51`

## Key Conventions

- **Workspace naming**: `YYYY-MM-DD/{slug}` (date directory with meeting slug subdirectory, lowercase, hyphens, max 60 chars for slug)
- **Ticket titles**: Imperative voice, 10-255 characters
- **KATA priorities**: P0-P3; **AVP priorities**: Highest/High/Medium/Low/Lowest
- **Story points**: Default to 0 (always requires explicit estimation)
- **Assignees**: Single person per task; default to "Unassigned"
- **Slack dates**: DD/MM/YYYY format

## Release Mapping (KATA)

Defined in `.claude/skills/kata-jira-task-creation/release-mapping.json`:

| Release | Fix Version ID | Date |
|---------|----------------|------|
| 25.1 | 10000 | 2025-09-26 |
| 25.2 | 10001 | 2025-12-26 |
| 25.3 | 10036 | 2026-04-03 |
| 26.1 | 10002 | 2026-06-26 |
| 26.2 | 10003 | 2026-09-18 |
