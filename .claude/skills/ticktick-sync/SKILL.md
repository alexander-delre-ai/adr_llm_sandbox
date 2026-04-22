---
name: ticktick-sync
description: Syncs Slack-tracked action items to TickTick Cursor Sync project using their API. Supports two modes - daily-todos sync and meeting action item sync from tickets.md. Tasks use short titles (15 words max) with full descriptions in content.
---

# TickTick Sync

Syncs Slack-tracked action items to your TickTick "Cursor Sync" project using their Open API. Supports two modes: daily-todos batch sync and meeting-specific sync from a `tickets.md` file. Tasks use short titles (15 words max) with full descriptions in content body.

## Instructions

This skill integrates with TickTick's API to create tasks from your daily todos. It handles both Slack action items and JIRA tickets, organizing them in a single TickTick project with appropriate priority levels and metadata.

### Prerequisites

1. **TickTick Developer Account**: Register at the TickTick developer portal
2. **OAuth Application**: Create an application to get client credentials
3. **Access Token**: Obtain an access token through OAuth flow
4. **Environment Setup**: Configure token in `.claude/skills/ticktick-sync/.env` file

### Workflow

1. **Authentication Check**: Validates TickTick access token
2. **Project Management**: Ensures daily project exists or creates new one
3. **Data Parsing**: Extracts todos from daily-todos skill output
4. **Task Mapping**: Converts todos to TickTick task format
5. **Batch Sync**: Creates tasks using TickTick API
6. **Status Reporting**: Reports sync results and any errors

### Task Organization

**Project**: "Cursor Sync" (created automatically if it doesn't exist)

**Task Title Format** (applies to all modes):
- **15 words or less** - intelligently condensed action-oriented titles
- Preserves key action verbs and context (e.g., "Document X" -> "add documentation for X")
- Natural language flow, no priority prefixes or labels
- Full original text preserved in the content/description body

**Task Content Format**:
```
[Full original description text]

Meeting: [meeting-slug or meeting source]
```

**Priority Mapping**: P0/P1 to High, P2 to Medium, P3+ to Low
**Tags**: Theme-based tags for Slack items, meeting slug for meeting items

### Implementation Steps

1. **Setup Authentication**:
   ```bash
   python3 .claude/skills/ticktick-sync/scripts/auth_setup.py
   ```

2. **Configure Environment**:
   - Copy `.claude/skills/ticktick-sync/env.example` to `.claude/skills/ticktick-sync/.env`
   - Add your TickTick access token
   - Configure sync preferences

3. **Sync Daily Todos**:
   ```bash
   # Generate and sync in one command
   bash .claude/skills/daily-todos/scripts/generate_todos.sh --sync-ticktick

   # Or sync existing todos
   python3 .claude/skills/ticktick-sync/scripts/sync_todos.py
   ```

### Error Handling

- **Network Issues**: Retries with exponential backoff
- **Authentication Errors**: Clear error messages with setup guidance
- **API Limits**: Respects rate limiting with appropriate delays
- **Duplicate Prevention**: Checks existing tasks to avoid duplicates
- **Partial Failures**: Reports which tasks succeeded/failed

### Configuration Options

Environment variables in `.claude/skills/ticktick-sync/.env`:
```bash
TICKTICK_ACCESS_TOKEN=your_token_here
TICKTICK_PROJECT_NAME=Daily Todos
TICKTICK_SYNC_ENABLED=true
TICKTICK_BATCH_SIZE=10
TICKTICK_AUTO_CLEANUP=true
```

### Meeting Action Item Sync

Syncs Slack-tracked action items from a meeting's `tickets.md` file to TickTick.

**Filtering rules**:
- Only items with `tracking: slack` are synced
- Only items assigned to AlexD or Unassigned are included
- JIRA-tracked items are skipped (they're tracked in JIRA)

**Running the sync**:
```bash
python3 .claude/skills/ticktick-sync/scripts/sync_meeting_items.py \
  --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md \
  --meeting "<Meeting Title>"
```

**Data flow**: `tickets.md` heading becomes short title (15 words max), YAML `description` field becomes content body, meeting metadata appended.

## Usage Examples

**Sync today's daily todos**:
```
Sync my daily todos to TickTick
```

**Sync meeting action items**:
```bash
python3 .claude/skills/ticktick-sync/scripts/sync_meeting_items.py \
  --tickets workspaces/2026-03-12/sdv-office-hours/tickets.md \
  --meeting "sdv-office-hours"
```

**Dry run** (preview without creating):
```bash
python3 .claude/skills/ticktick-sync/scripts/sync_meeting_items.py \
  --tickets workspaces/<YYYY-MM-DD>/<meeting-slug>/tickets.md \
  --meeting "<Meeting Title>" --dry-run
```

**Setup authentication**:
```
Setup TickTick integration
```

## Integration

This skill integrates with:
- **daily-todos skill**: Syncs generated daily Slack todos to TickTick
- **meeting-plan skill**: After Slack summary is sent, syncs eligible meeting action items to TickTick as follow-up tasks
