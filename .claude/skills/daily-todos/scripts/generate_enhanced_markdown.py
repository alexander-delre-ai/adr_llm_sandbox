#!/usr/bin/env python3
"""
Generate enhanced markdown with better checkbox support and progress tracking.
"""

import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from parse_workspaces import scan_workspaces

def generate_enhanced_markdown(items: Dict[str, List[Dict[str, Any]]], date: Optional[str] = None) -> str:
    """Generate enhanced markdown - now just calls the main function for consistency."""
    from parse_workspaces import generate_todo_markdown
    return generate_todo_markdown(items, date)

if __name__ == "__main__":
    import sys
    
    date = sys.argv[1] if len(sys.argv) > 1 else None
    workspaces_dir = sys.argv[2] if len(sys.argv) > 2 else "/home/alexanderdelre/adr_llm_sandbox/workspaces"
    
    items = scan_workspaces(workspaces_dir)
    markdown = generate_enhanced_markdown(items, date)
    
    print(markdown)