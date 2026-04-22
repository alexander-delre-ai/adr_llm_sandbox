# TickTick Sync Quick Setup Guide

## Prerequisites

1. **TickTick Account**: You need a TickTick account (free or premium)
2. **Python 3.7+**: Required for running the sync scripts
3. **Internet Connection**: For API calls to TickTick

## Step-by-Step Setup

### 1. Install Dependencies

The skill uses standard Python libraries, but you may need to install `requests` if not available:

```bash
pip install requests python-dotenv
```

### 2. TickTick Developer Setup

1. Go to [TickTick Developer Center](https://developer.ticktick.com/manage)
2. Sign in with your TickTick account
3. Click "Create App" and fill in:
   - **App Name**: Daily Todos Sync
   - **Description**: Sync daily todos to TickTick
   - **OAuth Redirect URI**: `http://localhost:5466/callback`
4. Save your **Client ID** and **Client Secret**

### 3. Get Access Token

Run the authentication setup script:

```bash
cd /home/alexanderdelre/adr_llm_sandbox
python3 .claude/skills/ticktick-sync/scripts/auth_setup.py
```

Follow the interactive prompts to:
- Enter your Client ID and Client Secret
- Complete OAuth authorization in browser
- Validate your access token

### 4. Test the Integration

Test that everything works:

```bash
# Generate todos and sync to TickTick
bash .claude/skills/daily-todos/scripts/generate_todos.sh --sync-ticktick
```

## Configuration Options

Edit `.claude/skills/ticktick-sync/.env` to customize:

```bash
# Required
TICKTICK_ACCESS_TOKEN=your_token_here

# Optional customization
TICKTICK_PROJECT_NAME=Daily Todos
TICKTICK_BATCH_SIZE=10
TICKTICK_AUTO_CLEANUP=true

# Debug options
TICKTICK_DEBUG=false
TICKTICK_DRY_RUN=false
```

## Usage Examples

### Via Daily Todos Integration

```bash
# Generate today's todos and sync
bash .claude/skills/daily-todos/scripts/generate_todos.sh --sync-ticktick

# Generate specific date and sync
bash .claude/skills/daily-todos/scripts/generate_todos.sh 2026-03-15 --sync-ticktick
```

### Standalone Sync

```bash
# Sync today's todos
python3 .claude/skills/ticktick-sync/scripts/sync_todos.py

# Sync specific date
python3 .claude/skills/ticktick-sync/scripts/sync_todos.py 2026-03-15

# Test mode (no actual changes)
python3 .claude/skills/ticktick-sync/scripts/sync_todos.py --dry-run
```

### Via Agent

Just ask the agent:
- "Sync my daily todos to TickTick"
- "Generate and sync today's todos to TickTick"
- "Create TickTick tasks from my action items"

## Troubleshooting

### Authentication Issues

**Problem**: "Authentication failed" error
**Solution**: 
1. Run `python3 .claude/skills/ticktick-sync/scripts/auth_setup.py`
2. Get a fresh access token
3. Make sure token has `tasks:read` and `tasks:write` scopes

### No Todos Found

**Problem**: "No todos found to sync"
**Solution**:
1. Make sure you have workspace directories with meeting data
2. Check that action items are assigned to "AlexD" or unassigned
3. Run daily-todos generation first: `bash .claude/skills/daily-todos/scripts/generate_todos.sh`

### API Errors

**Problem**: TickTick API errors or rate limiting
**Solution**:
1. Check your internet connection
2. Verify TickTick service status
3. Try again in a few minutes (rate limiting)
4. Use `--debug` flag for more information

### Duplicate Tasks

**Problem**: Tasks being created multiple times
**Solution**: The sync automatically checks for duplicates by title. If you see duplicates, they may have slightly different titles.

## Advanced Configuration

### Custom Project Names

You can customize the project naming pattern by editing the sync script or using environment variables:

```bash
TICKTICK_PROJECT_NAME="Work Todos"
# Creates projects like "Work Todos - 2026-03-12"
```

### Batch Size Tuning

Adjust batch size for better performance:

```bash
TICKTICK_BATCH_SIZE=5   # Smaller batches (more reliable)
TICKTICK_BATCH_SIZE=20  # Larger batches (faster)
```

### Automatic Cleanup

Control old project cleanup:

```bash
TICKTICK_AUTO_CLEANUP=true   # Delete projects older than 30 days
TICKTICK_AUTO_CLEANUP=false  # Keep all projects
```

## Getting Help

1. **Check logs**: Use `--debug` flag for detailed output
2. **Test mode**: Use `--dry-run` to test without making changes
3. **Validate setup**: Re-run `auth_setup.py` to test authentication
4. **Check TickTick**: Verify tasks in TickTick web/mobile app

## File Structure

```
.claude/skills/ticktick-sync/
├── README.md             # Detailed documentation (slash command: .claude/commands/ticktick-sync.md)
├── SETUP.md              # This quick setup guide
├── env.example           # Environment template
├── .env                  # Your configuration (created during setup)
└── scripts/
    ├── ticktick_client.py    # TickTick API client
    ├── task_mapper.py        # Todo to task conversion
    ├── sync_todos.py         # Main sync logic
    └── auth_setup.py         # Authentication setup
```