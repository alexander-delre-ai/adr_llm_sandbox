#!/bin/bash

# Gemini Notes Processor - Cron Runner
# Cron schedule: 0 9-18 * * 1-5

# Resolve paths relative to this script (works whether executed directly or sourced)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Source an optional shared environment file if present (search up to 5 levels)
ENV_SETUP_PATH="$SCRIPT_DIR/env-setup.sh"
if [[ -f "$ENV_SETUP_PATH" ]]; then
    source "$ENV_SETUP_PATH"
else
    for i in {1..5}; do
        _PARENT="$SCRIPT_DIR$(printf '/..'%.0s $(seq 1 $i))"
        _CANDIDATE="$_PARENT/env-setup.sh"
        if [[ -f "$_CANDIDATE" ]]; then
            source "$_CANDIDATE"
            break
        fi
    done
fi

# Export script name for identification in logs and process lists
export GEMINI_PROCESSOR_SCRIPT_NAME="gemini-notes-processor"

# Ensure the claude binary is on PATH (cron runs with a minimal environment)
export PATH="/home/alexanderdelre/.local/bin:$PATH"

# Set up log file and redirect ALL output (stdout + stderr) through tee
# so every line is captured in the log and still streams to the terminal / cron mail
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%dT%H-%M-%S).log"
exec > >(tee "$LOG_FILE") 2>&1

# ============================================
# Original script content below
# ============================================

set -euo pipefail

echo "[$(date +%H:%M:%S)] gemini-notes-processor: starting"
echo "[$(date +%H:%M:%S)] repo: $REPO_DIR"
echo "[$(date +%H:%M:%S)] log:  $LOG_FILE"

cd "$REPO_DIR"

echo "[$(date +%H:%M:%S)] invoking claude (timeout 15 minutes)..."

# < /dev/null prevents claude from blocking on stdin when run outside a TTY.
# timeout kills the process if MCP servers or the model hang indefinitely.
timeout 900 claude "You are running the gemini-notes-processor automated workflow in the adr_llm_sandbox repository.

Read and follow \`.claude/skills/gemini-notes-processor/SKILL.md\` exactly. Execute the full workflow from Step 1 through Step 6:

1. Load state from \`.claude/skills/gemini-notes-processor/last-run.json\` and \`processed-meetings.json\`
2. Load keyword filter from \`.claude/skills/gmail-inbox/keyword-filter.json\`
3. Search Gmail for new Gemini meeting notes emails since the last run
4. Filter by keywords; skip non-matching threads
5. For each qualifying, unprocessed thread: extract the Google Docs transcript URL, run meeting-plan Phase 1 (analysis.md, research.md, tickets.md), write status.md, apply the Gmail label, and send the Slack DM to alexanderdelre
6. Update last-run.json and processed-meetings.json on disk (do not commit or push to git)

Stop after Phase 1. The only outbound action is the per-meeting Slack DM to AlexD (Step 5f). Do not create JIRA tickets, post to Slack channels, or sync TickTick.

If there are no new meetings matching the keyword filter, still update last-run.json and exit cleanly." \
  < /dev/null

EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 124 ]]; then
  echo "[$(date +%H:%M:%S)] gemini-notes-processor: TIMED OUT after 15m"
else
  echo "[$(date +%H:%M:%S)] gemini-notes-processor: done (exit $EXIT_CODE)"
fi
echo "[$(date +%H:%M:%S)] log: $LOG_FILE"
exit "$EXIT_CODE"
