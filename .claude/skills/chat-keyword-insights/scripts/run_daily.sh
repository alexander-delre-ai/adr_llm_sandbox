#!/bin/bash
#
# Daily Chat Keyword Insights - Cron Entrypoint
#
# Scans Cursor agent transcripts from three workspaces:
#   - adr_llm_sandbox
#   - core-stack (~/applied/core-stack)
#   - vehicle-os-katana (~/applied/vehicle-os-katana)
#
# Slack messages require the on-demand Cursor/Claude command (MCP-mediated),
# so the cron job processes transcripts only.
#
# Usage:
#   ./run_daily.sh [YYYY-MM-DD]
#
# Cron entry (6pm PT weekdays), use absolute path to this script on your machine:
#   0 18 * * 1-5 /path/to/adr_llm_sandbox/.claude/skills/chat-keyword-insights/scripts/run_daily.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Repo root: .claude/skills/chat-keyword-insights/scripts -> four parents up
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
INSIGHTS_DIR="$PROJECT_ROOT/insights"
LOGS_DIR="$INSIGHTS_DIR/.logs"
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

echo ""
echo "Running keyword extraction across all workspaces..."
echo "  Date: $DATE"
echo "  Workspaces: adr-llm-sandbox, core-stack, vehicle-os-katana"
echo "  Output: $INSIGHTS_DIR/$DATE.md"
echo ""

python3 "$EXTRACT_SCRIPT" \
    --date "$DATE" \
    --insights-dir "$INSIGHTS_DIR"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    REPORT="$INSIGHTS_DIR/$DATE.md"
    if [ -f "$REPORT" ]; then
        echo ""
        echo "Report generated successfully: $REPORT"
        echo ""
        echo "--- Report Preview ---"
        head -40 "$REPORT"
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
echo "NOTE: Slack #ext-program-katana-sdv messages are only available via"
echo "      the on-demand command (requires Cursor/Claude MCP session)."

exit $EXIT_CODE
