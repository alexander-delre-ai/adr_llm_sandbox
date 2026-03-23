#!/bin/bash
#
# Daily Chat Keyword Insights - Cron Entrypoint
#
# Runs the keyword extraction pipeline on today's Cursor agent transcripts
# and generates a report in insights/YYYY-MM-DD.md.
#
# Slack messages require the on-demand Cursor/Claude command (MCP-mediated),
# so the cron job processes transcripts only. The on-demand command merges
# Slack data when run interactively.
#
# Usage:
#   ./run_daily.sh [YYYY-MM-DD]
#
# Cron entry (6pm PT weekdays):
#   0 18 * * 1-5 /home/alexanderdelre/adr_llm_sandbox/.cursor/skills/chat-keyword-insights/scripts/run_daily.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/alexanderdelre/adr_llm_sandbox"
INSIGHTS_DIR="$PROJECT_ROOT/insights"
LOGS_DIR="$INSIGHTS_DIR/.logs"
TRANSCRIPTS_DIR="/home/alexanderdelre/.cursor/projects/home-alexanderdelre-adr-llm-sandbox/agent-transcripts"
EXTRACT_SCRIPT="$SCRIPT_DIR/extract_keywords.py"

DATE="${1:-$(date +%Y-%m-%d)}"
LOG_FILE="$LOGS_DIR/$DATE.log"

mkdir -p "$INSIGHTS_DIR" "$LOGS_DIR"

exec > >(tee "$LOG_FILE") 2>&1

echo "=========================================="
echo "Chat Keyword Insights - $DATE"
echo "Started: $(date)"
echo "=========================================="

if [ ! -f "$EXTRACT_SCRIPT" ]; then
    echo "ERROR: Extract script not found: $EXTRACT_SCRIPT"
    exit 1
fi

if [ ! -d "$TRANSCRIPTS_DIR" ]; then
    echo "WARNING: Transcripts directory not found: $TRANSCRIPTS_DIR"
    echo "Attempting to continue with empty transcripts..."
fi

echo ""
echo "Running keyword extraction..."
echo "  Date: $DATE"
echo "  Transcripts: $TRANSCRIPTS_DIR"
echo "  Output: $INSIGHTS_DIR/$DATE.md"
echo ""

python3 "$EXTRACT_SCRIPT" \
    --date "$DATE" \
    --transcripts-dir "$TRANSCRIPTS_DIR" \
    --insights-dir "$INSIGHTS_DIR"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    REPORT="$INSIGHTS_DIR/$DATE.md"
    if [ -f "$REPORT" ]; then
        echo ""
        echo "Report generated successfully: $REPORT"
        echo ""
        echo "--- Report Preview ---"
        head -30 "$REPORT"
        echo "--- End Preview ---"
    else
        echo "WARNING: Script exited 0 but report file not found"
    fi
else
    echo "ERROR: Extraction failed with exit code $EXIT_CODE"
fi

echo ""
echo "Finished: $(date)"
echo "Log: $LOG_FILE"
echo ""
echo "NOTE: Slack messages are only available via the on-demand command"
echo "      (requires Cursor/Claude MCP session for Slack access)."

exit $EXIT_CODE
