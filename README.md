# ADR LLM Sandbox

A Cursor-based AI development environment with specialized rules, skills, and commands for meeting analysis, JIRA integration, and team collaboration workflows.

## Overview

This repository contains a structured set of AI agent configurations designed to streamline meeting analysis, task creation, and team coordination processes. The system integrates with JIRA, Slack, and GitHub to provide end-to-end workflow automation.

## 🔧 Rules

The `.cursor/rules/` directory contains workspace-level rules that are always applied:

### Response Formatting (`response_formatting.mdc`)
- **Always Applied**: Yes
- **Purpose**: Enforces consistent response formatting
- **Rule**: Never use em-dashes (—) in responses

## Claude commands and skills assets

Slash commands live in `.claude/commands/`. Scripts, JSON, and data files live in `.claude/skills/`.

### Meeting Analysis Pipeline

#### `/meeting-analysis` (`.claude/commands/meeting-analysis.md`)
- **Purpose**: Analyzes meeting content (transcripts or summaries) to extract structured insights
- **Input**: Full transcripts or AI-generated summaries
- **Output**: Structured `analysis.md` with 6 sections:
  1. Meeting Context
  2. Key Decisions
  3. Discussion Themes
  4. Unresolved Questions
  5. Action Items
  6. Prioritized Action Plan
- **Features**: Handles both full transcripts and Gemini summaries, filters meeting rooms from participants

#### `/meeting-workspace`
- **Purpose**: Creates persistent directory structure for meeting artifacts
- **Directory Pattern**: `workspaces/<YYYY-MM-DD>-<slugified-title>/`
- **Artifacts Saved**:
  - Original content (`transcript.md` or `summary.md`)
  - Analysis (`analysis.md`)
  - Editable tickets (`tickets.md`)
  - Action items (`action-items.md`)
  - JIRA ticket metadata (`jira-tickets/*.json`)
  - Slack message content (`slack-message.md`)
  - Session history (`chat-history.md`)

#### `meeting-summary` (and `meeting-slack-summary`)
- **`/meeting-summary`**: Transcript, file, or Google Doc to `workspaces/.../transcript.md` and `analysis.md` (see `.claude/commands/meeting-summary.md`)
- **`/meeting-slack-summary`**: Slack office-hours message; assets under `.claude/skills/meeting-summary/meeting-slack-summary/` (for example `user-mapping.md`). See `.claude/commands/meeting-slack-summary.md`
- **Slack sub-skill features**:
  - Separates Komatsu vs Applied attendees
  - Uses Slack mentions for Applied team members
  - Includes JIRA ticket links in hyperlink format
  - Sends notification to AlexD

### JIRA Integration

#### `/kata-jira-task-creation`
- **Project**: KATA (prefix: `KATA-`)
- **Mandatory Fields**: `epic_id`, `release`, `name`
- **Priority System**: P0 (critical), P1 (high), P2 (medium), P3 (low)
- **Release Mapping**: Supports Release 25.1-26.2 with custom field IDs
- **MCP Integration**: Uses `user-atlassian-mcp-kata` server
- **Special Epics**:
  - KATA-2226: Documentation tickets
  - KATA-2561: General meeting follow-up

#### `/avp-jira-task-creation`
- **Project**: AVP (prefix: `AVP-`)
- **Mandatory Fields**: `epic_id`, `release`, `name`
- **Priority System**: Highest, High, Medium, Low, Lowest
- **MCP Integration**: Uses `user-atlassian-mcp-applied` server
- **Validation**: Strict epic ID pattern matching

### Legacy Skills

#### Deprecated monolith

- **`meeting-analysis-and-planning`**: Deprecated. Use `/meeting-analysis` and `/meeting-tickets` (see `.claude/skills/meeting-analysis-and-planning/README.md`).

## Orchestrator

### `/meeting-plan` (`.claude/commands/meeting-plan.md`)

- **Purpose**: Full pipeline from content to staged `tickets.md`, then optional JIRA, Slack, TickTick, Google Doc share, workspace bundle
- **Phases**: Phase 1 stages `analysis.md`, `research.md`, `tickets.md`; Phase 2 runs after `continue` or `confirm`
- **Input types**: Google Docs URLs, `temp/` files, inline transcript, combinations

## 🗂️ Directory Structure

```
.claude/
├── commands/           # Slash command definitions (workflow text)
└── skills/             # Scripts, JSON, env.example, user-mapping, etc.

.cursor/
└── rules/              # Workspace rules (always applied)

workspaces/
└── <YYYY-MM-DD>-<meeting-slug>/
    ├── transcript.md OR summary.md
    ├── analysis.md
    ├── tickets.md
    ├── action-items.md
    ├── jira-tickets/
    ├── slack-message.md
    └── chat-history.md

temp/
└── (temporary files for processing)
```

## 🔗 Integrations

### MCP Servers
- **cursor-ide-browser**: Web automation and testing
- **user-github**: GitHub API integration
- **user-atlassian-mcp-kata**: KATA project JIRA integration
- **user-atlassian-mcp-applied**: AVP project JIRA integration
- **user-Slack**: Slack messaging integration
- **user-buildkite**: CI/CD pipeline integration

### External Services
- **JIRA**: Automated ticket creation with proper field mapping
- **Slack**: Office hours thread formatting and notifications
- **GitHub**: Repository management and collaboration
- **Gemini**: Meeting summary processing

## 🚀 Usage Examples

### Meeting Analysis Workflow
```
/meeting-plan
```
1. Provide meeting transcript or summary
2. System creates workspace and analysis
3. Review and edit proposed tickets
4. Confirm to create actual JIRA tickets
5. Receive Slack summary for team notification

### Direct command usage

```
Read and follow .claude/commands/meeting-analysis.md
```

## 📝 File Conventions

- **Slugification**: Lowercase, hyphens for spaces, max 60 chars
- **Date Format**: YYYY-MM-DD for directories, DD/MM/YYYY for Slack
- **Ticket Naming**: Imperative, 10-255 characters
- **Priorities**: P0-P3 for KATA, Highest-Lowest for AVP
- **Assignees**: Single person per task, "Unassigned" if unclear

## 🔄 Workflow Benefits

- ✅ **Review before commit**: See proposed tickets before creation
- ✅ **Clarifying questions**: Ask about unclear priorities or assignments
- ✅ **Collaborative refinement**: Adjust tickets based on discussion
- ✅ **MCP integration**: Create real tickets when ready
- ✅ **Complete automation**: Full workflow from analysis to execution
- ✅ **Persistent workspaces**: All artifacts saved for future reference
- ✅ **Team notifications**: Automated Slack summaries with proper formatting

## 📊 Current Status

- **Active Rules**: 1 (response formatting)
- **Active Skills**: 6 (meeting pipeline + JIRA integration)
- **Active Commands**: multiple (see `.claude/commands/`, for example `meeting-plan`, `meeting-summary`)
- **Supported Projects**: KATA, AVP
- **MCP Servers**: 6 configured and functional
- **Workspace Pattern**: Established and tested

This system provides a complete end-to-end solution for meeting analysis, task creation, and team coordination with full automation capabilities and collaborative review processes.