#!/bin/bash
#
# Generate daily todos for AlexD and sync directly to TickTick Inbox
# Usage: ./generate_todos.sh [YYYY-MM-DD] [--markdown-only]
#

# Parse command line arguments
MARKDOWN_ONLY=false
DATE=""

for arg in "$@"; do
    case $arg in
        --markdown-only)
            MARKDOWN_ONLY=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [YYYY-MM-DD] [--markdown-only]"
            echo "  YYYY-MM-DD     Date to generate todos for (default: today)"
            echo "  --markdown-only Generate markdown file only (skip TickTick sync)"
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

echo "📋 Processing daily todos for $DATE..."

# Default behavior: sync directly to TickTick
if [ "$MARKDOWN_ONLY" = false ]; then
    echo "🔄 Syncing todos directly to TickTick Inbox..."
    
    TICKTICK_SCRIPT="$PROJECT_ROOT/.cursor/skills/ticktick-sync/scripts/sync_todos.py"
    
    if [ -f "$TICKTICK_SCRIPT" ]; then
        python3 "$TICKTICK_SCRIPT" "$DATE"
        SYNC_EXIT_CODE=$?
        
        if [ $SYNC_EXIT_CODE -eq 0 ]; then
            echo "✅ Todos synced directly to TickTick Inbox"
            echo "📱 Check your TickTick app to see the tasks"
        else
            echo "❌ TickTick sync failed (exit code: $SYNC_EXIT_CODE)"
            echo "💡 Run setup: python3 $PROJECT_ROOT/.cursor/skills/ticktick-sync/scripts/auth_setup.py"
            echo ""
            echo "🔄 Falling back to markdown generation..."
            MARKDOWN_ONLY=true
        fi
    else
        echo "❌ TickTick sync script not found: $TICKTICK_SCRIPT"
        echo "💡 Make sure the ticktick-sync skill is properly installed"
        echo ""
        echo "🔄 Falling back to markdown generation..."
        MARKDOWN_ONLY=true
    fi
fi

# Fallback or explicit markdown generation
if [ "$MARKDOWN_ONLY" = true ]; then
    # Create todos directory if it doesn't exist
    mkdir -p "$PROJECT_ROOT/todos"
    
    # Generate the todo file
    OUTPUT_FILE="$PROJECT_ROOT/todos/$DATE.md"
    
    echo "📝 Generating markdown todos for $DATE..."
    
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
        echo "💡 To sync to TickTick: run without --markdown-only flag"
    else
        echo "❌ Error generating todos"
        exit 1
    fi
fi