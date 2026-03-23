---
description: Extracts keywords, questions, debugging sessions, and recurring themes from today's Cursor agent transcripts and Slack #ext-program-katana-sdv. Generates a daily insights report in insights/YYYY-MM-DD.md. Also runs automatically at 6pm PT weekdays via cron.
---

# Chat Keyword Insights

## Instructions

Generate a daily keyword insights report from today's chat activity. This command processes Cursor agent transcripts, Slack messages from #ext-program-katana-sdv, and optionally pasted Claude chat content.

### Step 1: Run the Python extraction on transcripts

Run the extraction script on today's agent transcripts:

```bash
python3 /home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/extract_keywords.py \
    --date "$(date +%Y-%m-%d)" \
    --insights-dir /home/alexanderdelre/adr_llm_sandbox/insights
```

This processes all `.jsonl` transcripts modified today and writes the initial report.

### Step 2: Fetch Slack messages

Use the Slack MCP to read recent messages from #ext-program-katana-sdv:

1. First, find the channel ID:
   - Call `slack_search_channels` with query "ext-program-katana-sdv"
   - Note the channel_id from the result

2. Read today's messages:
   - Call `slack_read_channel` with the channel_id
   - Set `oldest` to the start of today (midnight epoch timestamp)
   - Set `limit` to 100

3. Save the Slack messages to a temp file as JSON:
   - Write the messages array to `/tmp/slack-chat-insights-YYYY-MM-DD.json`
   - Format: `[{"text": "message text", "user": "U12345", "ts": "1234567890.123456"}, ...]`

4. Re-run the extraction with Slack data included:

```bash
python3 /home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/extract_keywords.py \
    --date "$(date +%Y-%m-%d)" \
    --slack-file "/tmp/slack-chat-insights-$(date +%Y-%m-%d).json" \
    --insights-dir /home/alexanderdelre/adr_llm_sandbox/insights
```

### Step 3: Include Claude chat (optional)

If the user provides pasted Claude chat text or a file path:

1. Save the content to `/tmp/claude-chat-insights-YYYY-MM-DD.txt`
2. Re-run with the `--claude-file` flag:

```bash
python3 /home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/extract_keywords.py \
    --date "$(date +%Y-%m-%d)" \
    --slack-file "/tmp/slack-chat-insights-$(date +%Y-%m-%d).json" \
    --claude-file "/tmp/claude-chat-insights-$(date +%Y-%m-%d).txt" \
    --insights-dir /home/alexanderdelre/adr_llm_sandbox/insights
```

### Step 4: Present the report

Read the generated report from `insights/YYYY-MM-DD.md` and present a summary to the user, highlighting:
- Top 10 most frequent topics/keywords
- Any open (unresolved) questions
- Debugging sessions and their resolutions
- Recurring themes trending across the week

### Scheduling

This command also runs automatically via cron at 6:00 PM PT on weekdays (transcript-only mode, no Slack). The cron entrypoint is:

```bash
/home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/run_daily.sh
```

Cron logs are at `insights/.logs/YYYY-MM-DD.log`.

### Output

Reports are written to `insights/YYYY-MM-DD.md` with sections for:
- Sources processed
- Topics & Technologies (keyword frequency table)
- Questions (with resolved/open status)
- Debugging & Errors (with context and resolution)
- Recurring Themes (last 7 days, with trend direction)
- Session Summaries (per-transcript overview)

### Domain Keywords

The extraction uses a curated dictionary at `.cursor/skills/chat-keyword-insights/data/domain-keywords.json`. To add new domain terms, edit that file and add terms to the appropriate category.

## Usage Examples

**Generate today's insights** (default):
```
Generate today's chat keyword insights
```

**Generate for a specific date**:
```
Generate chat keyword insights for March 20, 2026
```

**Include Claude chat**:
```
Generate chat keyword insights -- here's my Claude chat: [paste content]
```

**Check trends**:
```
What are the recurring themes from this week's chat insights?
```

**View recent reports**:
```
Show me yesterday's chat insights report
```
