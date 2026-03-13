# TickTick Sync Skill

Automatically sync your daily todos to TickTick using their Open API. This skill integrates with the daily-todos skill to create organized tasks in TickTick with proper priority mapping and metadata.

## Features

- **Automatic Sync**: Syncs both Slack items and JIRA tickets to TickTick
- **Smart Organization**: Creates daily projects with proper task categorization
- **Priority Mapping**: Maps P0/P1 → High, P2 → Medium, P3+ → Low priority
- **Rich Metadata**: Includes meeting context, assignees, and links in task descriptions
- **Duplicate Prevention**: Avoids creating duplicate tasks on repeated syncs
- **Error Handling**: Robust error handling with clear status reporting

## Setup

### 1. TickTick Developer Account

1. Go to [TickTick Developer Center](https://developer.ticktick.com/manage)
2. Register for a developer account
3. Create a new application
4. Note your `client_id` and `client_secret`

### 2. OAuth Authentication

Run the authentication setup script:

```bash
python3 .cursor/skills/ticktick-sync/scripts/auth_setup.py
```

This will guide you through:
- OAuth 2.0 authorization flow
- Obtaining access token
- Validating token permissions

### 3. Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .cursor/skills/ticktick-sync/env.example .cursor/skills/ticktick-sync/.env
   ```

2. Edit `.env` and add your access token:
   ```bash
   TICKTICK_ACCESS_TOKEN=your_actual_token_here
   ```

## Usage

### Via Daily Todos Integration

Generate and sync todos in one command:
```bash
bash .cursor/skills/daily-todos/scripts/generate_todos.sh --sync-ticktick
```

### Standalone Sync

Sync existing todos to TickTick:
```bash
python3 .cursor/skills/ticktick-sync/scripts/sync_todos.py
```

Sync specific date:
```bash
python3 .cursor/skills/ticktick-sync/scripts/sync_todos.py 2026-03-15
```

### Via Agent

Simply ask the agent:
- "Sync my daily todos to TickTick"
- "Create TickTick tasks from today's todos"
- "Send my action items to TickTick"

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TICKTICK_ACCESS_TOKEN` | - | Your TickTick API access token (required) |
| `TICKTICK_PROJECT_NAME` | "Daily Todos" | Base name for daily projects |
| `TICKTICK_SYNC_ENABLED` | true | Enable/disable sync functionality |
| `TICKTICK_BATCH_SIZE` | 10 | Number of tasks to create per API call |
| `TICKTICK_AUTO_CLEANUP` | true | Auto-cleanup old projects |
| `TICKTICK_DEBUG` | false | Enable debug logging |
| `TICKTICK_DRY_RUN` | false | Test mode without creating tasks |

### Project Organization

- **Project Name**: "Daily Todos - YYYY-MM-DD"
- **Task Titles**: Include priority and type prefixes
- **Task Content**: Rich descriptions with context and links
- **Tags**: Automatic tagging by type (slack/jira) and metadata

## Task Format

### Slack Items
```
Title: [P1] Schedule manager planning meetings with system engineering
Content: 
Meeting: 2026-03-10-katana-applied-sdv-sw-office-hours
Assigned: AlexD
Slack: https://appliedint.slack.com/archives/search?q=...
Tags: slack, meeting-scheduling
```

### JIRA Tickets
```
Title: [KATA-2573] Define mandatory hardware diagnostics requirements
Content:
Status: Backlog
Points: 0.1
JIRA: https://appliedint-katana.atlassian.net/browse/KATA-2573
Tags: jira, points-0.1
```

## Troubleshooting

### Authentication Issues

1. **Invalid Token**: Run `auth_setup.py` to refresh token
2. **Expired Token**: Tokens expire, re-run OAuth flow
3. **Insufficient Permissions**: Ensure `tasks:read` and `tasks:write` scopes

### API Issues

1. **Rate Limiting**: Script automatically handles rate limits
2. **Network Errors**: Retries with exponential backoff
3. **Project Creation**: Ensures project exists before creating tasks

### Sync Issues

1. **Duplicates**: Script checks existing tasks by title
2. **Missing Data**: Validates todo data before sync
3. **Partial Failures**: Reports which tasks succeeded/failed

## Dependencies

- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management
- Standard library modules (json, datetime, pathlib, etc.)

## API Reference

Uses TickTick Open API v1:
- Base URL: `https://api.ticktick.com/open/v1`
- Authentication: Bearer token in Authorization header
- Endpoints: Projects, Tasks, Batch operations

For full API documentation, see: https://developer.ticktick.com/docs