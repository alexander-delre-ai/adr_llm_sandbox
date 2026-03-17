# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

An AI workflow automation system for meeting analysis, JIRA ticket creation, and team collaboration. It processes meeting transcripts into structured analysis, staged JIRA ticket proposals, and Slack summaries using Cursor skills and MCP server integrations.

## Global Rules (Always Apply)

- Never use em-dashes in responses
- One story point equals one week of work

## Python Scripts

The only runnable code lives in `.cursor/skills/`:

```bash
# TickTick auth setup
python3 .cursor/skills/ticktick-sync/scripts/auth_setup.py

# TickTick todo sync
python3 .cursor/skills/ticktick-sync/scripts/sync_todos.py

# Daily todo generation (parses workspaces, generates markdown)
bash .cursor/skills/daily-todos/scripts/generate_todos.sh
```

No build system, linter, or test framework is configured.

## Architecture

### Skills (`/.cursor/skills/`)

Reusable AI agent capabilities invoked by name. Each skill has a `SKILL.md` defining inputs, outputs, and step-by-step instructions.

| Skill | Purpose |
|---|---|
| `meeting-analysis` | Extract decisions, action items, themes from transcripts |
| `meeting-workspace` | Create persistent `workspaces/YYYY-MM-DD-{slug}/` directories |
| `meeting-tickets` | Stage editable JIRA ticket proposals in workspace |
| `meeting-slack-summary` | Format and send Slack office hours messages |
| `kata-jira-task-creation` | Create JIRA tickets in KATA project |
| `avp-jira-task-creation` | Create JIRA tickets in AVP project |
| `app-dev-k1-hw-ticket-creation` | K1 hardware batch manager ticket processing |
| `daily-todos` | Generate daily task lists from workspaces |
| `ticktick-sync` | Sync todos to TickTick API |

### Commands (`/.cursor/commands/`)

High-level workflow orchestrators. The main command is `/meeting_plan` which runs in plan mode and chains: analysis → workspace creation → ticket staging → JIRA creation → Slack summary.

### Workspaces (`/workspaces/`)

Persistent meeting artifacts. Each directory is `YYYY-MM-DD-{meeting-slug}/` and contains: `transcript.md`, `analysis.md`, `tickets.md`, JIRA metadata JSON files, and chat history.

### MCP Integrations

- `user-atlassian-mcp-kata` — KATA JIRA project
- `user-atlassian-mcp-applied` — AVP JIRA project
- `user-Slack` — Slack messaging
- `user-github` — GitHub
- `user-buildkite` — CI/CD

## Key Conventions

- **Workspace naming**: `YYYY-MM-DD-{slug}` (lowercase, hyphens, max 60 chars)
- **Ticket titles**: Imperative voice, 10–255 characters
- **KATA priorities**: P0–P3; **AVP priorities**: Highest/High/Medium/Low/Lowest
- **Story points**: Default to 0 (always requires explicit estimation)
- **Assignees**: Single person per task; default to "Unassigned"
- **Slack dates**: DD/MM/YYYY format

## Release Mapping (KATA)

Defined in `.cursor/skills/kata-jira-task-creation/release-mapping.json`:

| Release | Fix Version ID | Date |
|---|---|---|
| 25.1 | 10000 | 2025-09-26 |
| 25.2 | 10001 | 2025-12-26 |
| 25.3 | 10036 | 2026-04-03 |
| 26.1 | 10002 | 2026-06-26 |
| 26.2 | 10003 | 2026-09-18 |
