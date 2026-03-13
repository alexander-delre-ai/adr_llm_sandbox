#!/bin/bash
#
# Generate daily todos for AlexD
# Usage: ./generate_todos.sh [YYYY-MM-DD] [--sync-ticktick]
#

# Parse command line arguments
SYNC_TICKTICK=false
DATE=""

for arg in "$@"; do
    case $arg in
        --sync-ticktick)
            SYNC_TICKTICK=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [YYYY-MM-DD] [--sync-ticktick]"
            echo "  YYYY-MM-DD     Date to generate todos for (default: today)"
            echo "  --sync-ticktick Sync generated todos to TickTick"
            exit 0
            ;;
        *)
            if [[ $arg =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                DATE="$arg"
            fi
            ;;
    esac
done

# Set default date to today if not provided
DATE=${DATE:-$(date +%Y-%m-%d)}

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/alexanderdelre/adr_llm_sandbox"

# Create todos directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/todos"

# Generate the todo file
OUTPUT_FILE="$PROJECT_ROOT/todos/$DATE.md"

echo "📋 Generating organized daily todos for $DATE..."

# Run the Python script and save to file
python3 "$SCRIPT_DIR/parse_workspaces.py" "$DATE" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Daily todos generated: $OUTPUT_FILE"
    
    # Show summary from the new format
    echo ""
    echo "📊 Summary:"
    grep -A 10 "## 📊 Summary" "$OUTPUT_FILE" | grep "| \*\*📋 Total\*\*" || echo "Summary not found in expected format"
    
    # Show priority breakdown
    echo ""
    echo "🎯 Priority Breakdown:"
    grep "🔴\|🟡\|🟢.*Priority" "$OUTPUT_FILE" | head -3 || echo "Priority breakdown not found"
    
    echo ""
    echo "📂 File location: $OUTPUT_FILE"
    echo "💡 Open in Cursor to use checkboxes and navigate with hyperlinks"
    
    # Sync to TickTick if requested
    if [ "$SYNC_TICKTICK" = true ]; then
        echo ""
        echo "🔄 Syncing todos to TickTick..."
        
        TICKTICK_SCRIPT="$PROJECT_ROOT/.cursor/skills/ticktick-sync/scripts/sync_todos.py"
        
        if [ -f "$TICKTICK_SCRIPT" ]; then
            python3 "$TICKTICK_SCRIPT" "$DATE"
            SYNC_EXIT_CODE=$?
            
            if [ $SYNC_EXIT_CODE -eq 0 ]; then
                echo "✅ TickTick sync completed successfully"
            else
                echo "❌ TickTick sync failed (exit code: $SYNC_EXIT_CODE)"
                echo "💡 Run setup: python3 $PROJECT_ROOT/.cursor/skills/ticktick-sync/scripts/auth_setup.py"
            fi
        else
            echo "❌ TickTick sync script not found: $TICKTICK_SCRIPT"
            echo "💡 Make sure the ticktick-sync skill is properly installed"
        fi
    fi
else
    echo "❌ Error generating todos"
    exit 1
fi