---
name: chat-keyword-insights
description: Extracts keywords, JIRA tickets, questions, debugging sessions, and recurring themes from Cursor agent transcripts across adr-llm-sandbox, core-stack, and vehicle-os-katana workspaces, plus Slack #ext-program-katana-sdv and optional Claude chats. Runs at 6pm PT weekdays via cron, or on-demand. Reports in insights/.
---

# Daily Chat Keyword Insights

## Instructions

This skill processes the day's chat activity across three Cursor workspaces, Slack, and optionally Claude chats to extract structured keyword insights. It identifies JIRA tickets referenced, topics discussed, questions asked (and whether they were resolved), debugging sessions, and themes that recur across multiple days.

### Data Sources

1. **Cursor agent transcripts** -- `.jsonl` files from three workspaces, filtered by modification date:
   - `adr-llm-sandbox` -- this repo (`~/.cursor/projects/home-alexanderdelre-adr-llm-sandbox/agent-transcripts`)
   - `core-stack` -- `~/applied/core-stack` (`~/.cursor/projects/home-alexanderdelre-applied-core-stack/agent-transcripts`)
   - `vehicle-os-katana` -- `~/applied/vehicle-os-katana` (`~/.cursor/projects/home-alexanderdelre-applied-vehicle-os-katana/agent-transcripts`)
2. **Slack `#ext-program-katana-sdv`** -- Slack Connect channel; searched via `slack_search_public_and_private` MCP tool (on-demand only)
3. **Claude chats** -- optional pasted text or file path when running the on-demand command

### Workflow

1. **Collect sources**: Gather today's agent transcripts and Slack messages
2. **Parse content**: Extract user/assistant text from JSONL, strip XML metadata tags
3. **Extract keywords**: Match against domain dictionary + regex patterns for JIRA keys, file paths, tool names
4. **Detect questions**: Find interrogative user messages, check resolution status via assistant response heuristics
5. **Detect debugging**: Identify error patterns, group into sessions, capture resolutions
6. **Analyze trends**: Compare today's keywords against the last 7 days of reports
7. **Generate report**: Write `insights/YYYY-MM-DD.md`

### Scheduling

Runs automatically via cron at **6:00 PM PT, weekdays only** (`0 18 * * 1-5`).

Entrypoint: `.cursor/skills/chat-keyword-insights/scripts/run_daily.sh`

The cron job:
1. Runs `extract_keywords.py` on today's transcripts
2. Fetches Slack `#ext-program-katana-sdv` messages for the day
3. Merges results into `insights/YYYY-MM-DD.md`
4. Logs output to `insights/.logs/YYYY-MM-DD.log`

### On-Demand Usage

Also available as an interactive command. When invoked:
1. Runs the extraction pipeline on today's data
2. Calls `slack_read_channel` via MCP for richer Slack data
3. Accepts optional pasted Claude chat content
4. Writes or overwrites `insights/YYYY-MM-DD.md`

### Output Format

Reports are written to `insights/YYYY-MM-DD.md` with these sections:

- **Sources** -- workspace-level breakdown of sessions processed
- **JIRA Tickets** -- all KATA/AVP tickets referenced, with clickable links and source attribution
- **Topics & Technologies** -- keyword frequency table with source attribution
- **Questions** -- user questions with resolved/open status
- **Debugging & Errors** -- error sessions with context and resolution
- **Recurring Themes** -- keywords appearing 3+ days in the last 7, with trend direction
- **Session Summaries** -- per-transcript overview with workspace labels

### Domain Keywords

The file `data/domain-keywords.json` contains a curated dictionary of domain terms grouped by category. The extractor uses this for matching alongside dynamic regex patterns. Users can extend it by adding terms to the appropriate category.

Categories: jira, hardware, tools, protocols, processes, teams, concepts.

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract_keywords.py` | Main extraction engine (stdlib Python) |
| `scripts/run_daily.sh` | Cron entrypoint / shell wrapper |

### File Locations

| Path | Purpose |
|------|---------|
| `insights/YYYY-MM-DD.md` | Daily keyword reports |
| `insights/.logs/YYYY-MM-DD.log` | Cron run logs |
| `.cursor/skills/chat-keyword-insights/data/domain-keywords.json` | Domain term dictionary |

### Error Handling

- Skips transcripts that fail to parse with a warning in the log
- Continues if Slack fetch fails (reports transcript-only results)
- Creates the insights directory if missing
- Overwrites existing report for the same date

## Usage Examples

**Automatic (cron)**:
Reports appear in `insights/` each weekday evening. Check the latest:
```
cat insights/$(date +%Y-%m-%d).md
```

**On-demand via command**:
```
Generate today's chat keyword insights
```

**On-demand with Claude chat input**:
```
Generate chat keyword insights -- here's my Claude chat from today: [paste]
```

**Check recent trends**:
```
Show me the recurring themes from this week's chat insights
```
