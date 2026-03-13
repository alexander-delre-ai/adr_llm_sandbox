#!/usr/bin/env python3
"""
Clear the duplicate tracking file for TickTick sync.
Use this if you need to reset duplicate detection.
"""

import os
from pathlib import Path

def clear_duplicates():
    """Clear the duplicate tracking file."""
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    duplicate_file = skill_dir / '.task_duplicates.json'
    
    if duplicate_file.exists():
        try:
            os.remove(duplicate_file)
            print("✅ Cleared duplicate tracking file")
            print(f"📂 Removed: {duplicate_file}")
        except Exception as e:
            print(f"❌ Error clearing duplicate file: {e}")
    else:
        print("ℹ️  No duplicate tracking file found")

if __name__ == "__main__":
    clear_duplicates()