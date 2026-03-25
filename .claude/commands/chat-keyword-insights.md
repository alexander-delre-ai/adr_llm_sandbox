---
description: Extracts keywords, JIRA tickets, questions, debugging sessions, and recurring themes from Cursor agent transcripts across adr-llm-sandbox, core-stack, and vehicle-os-katana workspaces, plus Slack #ext-program-katana-sdv. Generates daily insights report in insights/YYYY-MM-DD.md.
---

# Chat Keyword Insights

## Instructions

Generate a daily keyword insights report from today's chat activity across all workspaces.

### Step 1: Run the Python extraction on transcripts

The script automatically scans transcripts from all three workspaces:
- `adr-llm-sandbox` (this repo)
- `core-stack` (`~/applied/core-stack`)
- `vehicle-os-katana` (`~/applied/vehicle-os-katana`)

```bash
python3 /home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/extract_keywords.py \
    --date "$(date +%Y-%m-%d)" \
    --insights-dir /home/alexanderdelre/adr_llm_sandbox/insights
```

### Step 2: Fetch Slack #ext-program-katana-sdv messages

The channel is a Slack Connect channel and does not appear in channel search. Use keyword-based search to find today's messages.

1. Search for today's messages using `slack_search_public_and_private`:
   - query: `"in:ext-program-katana-sdv after:YYYY-MM-DD"` (use today's date)
   - If no results, try broader: `"katana SDV after:YYYY-MM-DD"`
   - Set `sort` to `"timestamp"`, `sort_dir` to `"desc"`, `limit` to `20`
   - Set `response_format` to `"detailed"`, `include_context` to `false`

2. If messages are found, extract the text from each result and save as JSON:
   - Write to `/tmp/slack-chat-insights-YYYY-MM-DD.json`
   - Format: `[{"text": "message text", "user": "U12345", "ts": "1234567890.123456"}, ...]`

3. Re-run extraction with Slack data:

```bash
python3 /home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/extract_keywords.py \
    --date "$(date +%Y-%m-%d)" \
    --slack-file "/tmp/slack-chat-insights-$(date +%Y-%m-%d).json" \
    --insights-dir /home/alexanderdelre/adr_llm_sandbox/insights
```

### Step 3: Include Claude chat (optional)

If the user provides pasted Claude chat text or a file path:

1. Save the content to `/tmp/claude-chat-insights-YYYY-MM-DD.txt`
2. Re-run with the `--claude-file` flag added to the command above.

### Step 4: Present the report

Read the generated report from `insights/YYYY-MM-DD.md` and present a summary highlighting:
- JIRA tickets referenced (with clickable links)
- Top 10 most frequent topics/keywords
- Any open (unresolved) questions
- Debugging sessions and their resolutions
- Recurring themes trending across the week
- Which workspaces generated the most activity

### Scheduling

Also runs automatically via cron at 6:00 PM PT weekdays (transcripts only, no Slack):

```bash
/home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/run_daily.sh
```

### Output

Reports in `insights/YYYY-MM-DD.md` contain:
- **Sources** -- workspace-level breakdown of sessions processed
- **JIRA Tickets** -- all KATA/AVP tickets referenced, with clickable links and source attribution
- **Topics & Technologies** -- keyword frequency table (domain terms, tools, protocols)
- **Questions** -- user questions with resolved/open status
- **Debugging & Errors** -- error sessions with context and resolution
- **Recurring Themes** -- keywords appearing 3+ days in the last 7
- **Session Summaries** -- per-session overview with workspace labels

### Workspaces Scanned

| Workspace | Transcript Path |
|-----------|----------------|
| adr-llm-sandbox | `~/.cursor/projects/home-alexanderdelre-adr-llm-sandbox/agent-transcripts` |
| core-stack | `~/.cursor/projects/home-alexanderdelre-applied-core-stack/agent-transcripts` |
| vehicle-os-katana | `~/.cursor/projects/home-alexanderdelre-applied-vehicle-os-katana/agent-transcripts` |

### Domain Keywords

Curated dictionary at `.cursor/skills/chat-keyword-insights/data/domain-keywords.json`. Add new domain terms by editing that file.

## Usage Examples

**Generate today's insights**:
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
