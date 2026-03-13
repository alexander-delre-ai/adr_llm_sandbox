#!/usr/bin/env python3
"""
Utility script to parse workspace directories and extract action items for AlexD.
Returns structured data for todo list generation.
"""

import os
import json
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

def generate_slack_url(meeting_source: str) -> str:
    """Generate a Slack search URL for the meeting."""
    # Convert meeting source to a searchable format
    # Remove date prefix and convert to search terms
    search_terms = meeting_source.replace('-', ' ').replace('2026 03', '').strip()
    search_terms = ' '.join(search_terms.split()[1:])  # Remove date parts
    
    # URL encode the search terms
    import urllib.parse
    encoded_search = urllib.parse.quote(search_terms)
    
    # Return Slack search URL (this would need to be customized for the actual Slack workspace)
    return f"https://appliedint.slack.com/archives/search?q={encoded_search}"

def parse_action_items_table(content: str, meeting_source: str) -> List[Dict[str, Any]]:
    """Parse action-items.md table format."""
    items = []
    lines = content.split('\n')
    
    # Find table start (header row with |---|)
    table_start = -1
    for i, line in enumerate(lines):
        if '|---|' in line or '| # |' in line.lower():
            table_start = i + 1 if '|---|' in line else i + 1
            break
    
    if table_start == -1:
        return items
    
    # Parse table rows
    for line in lines[table_start:]:
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
            
        # Split by | and clean up
        parts = [part.strip() for part in line.split('|')[1:-1]]  # Remove empty first/last
        if len(parts) >= 3:  # At least #, What, Who
            try:
                item_num = parts[0]
                what = parts[1]
                who = parts[2] if len(parts) > 2 else "Unassigned"
                priority = parts[3] if len(parts) > 3 else "Medium"
                due = parts[4] if len(parts) > 4 else ""
                theme = parts[5] if len(parts) > 5 else ""
                
                # Only include items for AlexD or unassigned
                if 'alexd' in who.lower() or who.lower() in ['unassigned', '']:
                    items.append({
                        'type': 'slack',
                        'description': what,
                        'assignee': who,
                        'priority': priority,
                        'due': due,
                        'theme': theme,
                        'meeting_source': meeting_source,
                        'item_number': item_num,
                        'slack_url': generate_slack_url(meeting_source)
                    })
            except (IndexError, ValueError):
                continue
    
    return items

def parse_tickets_yaml(content: str, meeting_source: str) -> List[Dict[str, Any]]:
    """Parse tickets.md YAML blocks."""
    items = []
    
    # Find YAML blocks between ```yaml and ```
    yaml_blocks = re.findall(r'```yaml\n(.*?)\n```', content, re.DOTALL)
    
    for yaml_content in yaml_blocks:
        try:
            data = yaml.safe_load(yaml_content)
            if isinstance(data, dict):
                assignee = data.get('assignee', 'Unassigned')
                
                # Only include items for AlexD or unassigned
                if 'alexd' in assignee.lower() or assignee.lower() in ['unassigned', '']:
                    item_type = data.get('tracking', 'jira')
                    item = {
                        'type': item_type,
                        'description': data.get('description', ''),
                        'assignee': assignee,
                        'priority': data.get('priority', 'P2'),
                        'parent_id': data.get('parent_id', 'TBD'),
                        'release': data.get('release', 'TBD'),
                        'story_points': data.get('story_points', 0),
                        'meeting_source': meeting_source
                    }
                    
                    # Add Slack URL for slack-tracked items
                    if item_type == 'slack':
                        item['slack_url'] = generate_slack_url(meeting_source)
                    
                    items.append(item)
        except yaml.YAMLError:
            continue
    
    return items

def parse_jira_tickets(jira_dir: Path, meeting_source: str) -> List[Dict[str, Any]]:
    """Parse JIRA ticket JSON files."""
    items = []
    
    if not jira_dir.exists():
        return items
    
    for json_file in jira_dir.glob('*.json'):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            assignee = data.get('assignee') or 'Unassigned'
            
            # Only include items for AlexD or unassigned
            if assignee == 'Unassigned' or 'alexd' in str(assignee).lower():
                items.append({
                    'type': 'jira',
                    'ticket_key': data.get('ticket_key', ''),
                    'summary': data.get('summary', ''),
                    'description': data.get('description', ''),
                    'web_url': data.get('web_url', ''),
                    'priority': data.get('priority', 'P2'),
                    'status': data.get('status', 'Unknown'),
                    'assignee': assignee,
                    'story_points': data.get('story_points', 0),
                    'meeting_source': data.get('meeting_source', meeting_source),
                    'created_date': data.get('created_date', '')
                })
        except (json.JSONDecodeError, IOError):
            continue
    
    return items

def scan_workspaces(workspaces_dir: str = "/home/alexanderdelre/adr_llm_sandbox/workspaces", target_date: str = None) -> Dict[str, List[Dict[str, Any]]]:
    """Scan workspace directories and extract action items for a specific date."""
    workspaces_path = Path(workspaces_dir)
    all_items = {'slack': [], 'jira': []}
    
    if not workspaces_path.exists():
        return all_items
    
    for workspace_dir in workspaces_path.iterdir():
        if not workspace_dir.is_dir():
            continue
        
        meeting_name = workspace_dir.name
        
        # Filter by date if target_date is provided
        if target_date:
            # Check if workspace directory name starts with the target date
            if not meeting_name.startswith(target_date):
                continue
        
        # Parse action-items.md
        action_items_file = workspace_dir / 'action-items.md'
        if action_items_file.exists():
            try:
                with open(action_items_file, 'r') as f:
                    content = f.read()
                items = parse_action_items_table(content, meeting_name)
                for item in items:
                    if item['type'] == 'slack':
                        all_items['slack'].append(item)
                    else:
                        all_items['jira'].append(item)
            except IOError:
                pass
        
        # Parse tickets.md
        tickets_file = workspace_dir / 'tickets.md'
        if tickets_file.exists():
            try:
                with open(tickets_file, 'r') as f:
                    content = f.read()
                items = parse_tickets_yaml(content, meeting_name)
                for item in items:
                    if item['type'] == 'slack':
                        all_items['slack'].append(item)
                    else:
                        all_items['jira'].append(item)
            except IOError:
                pass
        
        # Parse JIRA tickets
        jira_dir = workspace_dir / 'jira-tickets'
        items = parse_jira_tickets(jira_dir, meeting_name)
        all_items['jira'].extend(items)
    
    return all_items

def categorize_slack_items(slack_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize Slack items by theme/type."""
    categories = {
        'Meeting Scheduling': [],
        'JIRA & Access Management': [],
        'Documentation & Requirements': [],
        'Technical Implementation': [],
        'Testing & Quality': [],
        'Other': []
    }
    
    for item in slack_items:
        description = item.get('description', '').lower()
        theme = item.get('theme', '').lower()
        
        if any(keyword in description for keyword in ['schedule', 'meeting', 'coordination']):
            categories['Meeting Scheduling'].append(item)
        elif any(keyword in description for keyword in ['jira', 'access', 'admin', 'permission', 'filter']):
            categories['JIRA & Access Management'].append(item)
        elif any(keyword in description for keyword in ['document', 'requirement', 'example', 'guidance']):
            categories['Documentation & Requirements'].append(item)
        elif any(keyword in description for keyword in ['implementation', 'interface', 'gateway', 'connector', 'hardware']):
            categories['Technical Implementation'].append(item)
        elif any(keyword in description for keyword in ['test', 'mock', 'runtime', 'diagnostic']):
            categories['Testing & Quality'].append(item)
        else:
            categories['Other'].append(item)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def generate_todo_markdown(items: Dict[str, List[Dict[str, Any]]], date: Optional[str] = None) -> str:
    """Generate organized markdown todo list."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    human_date = datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')
    
    slack_items = items.get('slack', [])
    jira_items = items.get('jira', [])
    all_items = slack_items + jira_items
    
    # Calculate summary stats
    total_count = len(all_items)
    high_priority = len([item for item in all_items if item.get('priority', '').startswith('P0') or item.get('priority', '').startswith('P1') or 'high' in item.get('priority', '').lower()])
    medium_priority = len([item for item in all_items if item.get('priority', '').startswith('P2') or 'medium' in item.get('priority', '').lower()])
    low_priority = total_count - high_priority - medium_priority
    
    markdown = f"""# 📋 Daily Todos - {human_date}

**Progress**: 0/{total_count} completed (0%) | 🔴 {high_priority} High | 🟡 {medium_priority} Medium | 🟢 {low_priority} Low

---

## 🔴 High Priority Items (P0/P1)

"""
    
    # High Priority Section
    high_priority_items = [item for item in all_items if item.get('priority', '').startswith('P0') or item.get('priority', '').startswith('P1') or 'high' in item.get('priority', '').lower()]
    
    if high_priority_items:
        for item in sorted(high_priority_items, key=lambda x: (x.get('type', ''), x.get('priority', ''))):
            item_type = "💬" if item.get('type') == 'slack' else "🎫"
            priority = item.get('priority', 'High')
            
            if item.get('type') == 'slack':
                description = item.get('description', 'No description')
                assignee = item.get('assignee', 'Unassigned')
                meeting = item.get('meeting_source', 'Unknown meeting')
                slack_url = item.get('slack_url', '')
                meeting_link = f"[{meeting}]({slack_url})" if slack_url else meeting
                
                markdown += f"- [ ] {item_type} **{priority}** {description}\n"
                markdown += f"      *Assigned to: {assignee}* • {meeting_link}\n\n"
            else:
                ticket_key = item.get('ticket_key', 'NO-KEY')
                summary = item.get('summary', 'No summary')
                story_points = item.get('story_points', 0)
                web_url = item.get('web_url', '')
                status = item.get('status', 'Unknown')
                
                ticket_link = f"[{ticket_key}]({web_url})" if web_url and ticket_key != 'NO-KEY' else ticket_key
                markdown += f"- [ ] {item_type} **{ticket_link}** {summary}\n"
                markdown += f"      *Priority: {priority} • Points: {story_points} • Status: {status}*\n\n"
    else:
        markdown += "No high priority items.\n\n"
    
    # Medium Priority Section
    markdown += "## 🟡 Medium Priority Items (P2)\n\n"
    medium_priority_items = [item for item in all_items if item.get('priority', '').startswith('P2') or 'medium' in item.get('priority', '').lower()]
    
    if medium_priority_items:
        for item in sorted(medium_priority_items, key=lambda x: (x.get('type', ''), x.get('description', ''))):
            item_type = "💬" if item.get('type') == 'slack' else "🎫"
            priority = item.get('priority', 'Medium')
            
            if item.get('type') == 'slack':
                description = item.get('description', 'No description')
                assignee = item.get('assignee', 'Unassigned')
                meeting = item.get('meeting_source', 'Unknown meeting')
                slack_url = item.get('slack_url', '')
                meeting_link = f"[{meeting}]({slack_url})" if slack_url else meeting
                
                markdown += f"- [ ] {item_type} **{priority}** {description}\n"
                markdown += f"      *Assigned to: {assignee}* • {meeting_link}\n\n"
            else:
                ticket_key = item.get('ticket_key', 'NO-KEY')
                summary = item.get('summary', 'No summary')
                story_points = item.get('story_points', 0)
                web_url = item.get('web_url', '')
                status = item.get('status', 'Unknown')
                
                ticket_link = f"[{ticket_key}]({web_url})" if web_url and ticket_key != 'NO-KEY' else ticket_key
                markdown += f"- [ ] {item_type} **{ticket_link}** {summary}\n"
                markdown += f"      *Priority: {priority} • Points: {story_points} • Status: {status}*\n\n"
    else:
        markdown += "No medium priority items.\n\n"
    
    # Low Priority Section
    markdown += "## 🟢 Low Priority Items (P3+)\n\n"
    low_priority_items = [item for item in all_items if not (item.get('priority', '').startswith('P0') or item.get('priority', '').startswith('P1') or item.get('priority', '').startswith('P2') or 'high' in item.get('priority', '').lower() or 'medium' in item.get('priority', '').lower())]
    
    if low_priority_items:
        for item in sorted(low_priority_items, key=lambda x: (x.get('type', ''), x.get('description', ''))):
            item_type = "💬" if item.get('type') == 'slack' else "🎫"
            priority = item.get('priority', 'Low')
            
            if item.get('type') == 'slack':
                description = item.get('description', 'No description')
                assignee = item.get('assignee', 'Unassigned')
                meeting = item.get('meeting_source', 'Unknown meeting')
                slack_url = item.get('slack_url', '')
                meeting_link = f"[{meeting}]({slack_url})" if slack_url else meeting
                
                markdown += f"- [ ] {item_type} **{priority}** {description}\n"
                markdown += f"      *Assigned to: {assignee}* • {meeting_link}\n\n"
            else:
                ticket_key = item.get('ticket_key', 'NO-KEY')
                summary = item.get('summary', 'No summary')
                story_points = item.get('story_points', 0)
                web_url = item.get('web_url', '')
                status = item.get('status', 'Unknown')
                
                ticket_link = f"[{ticket_key}]({web_url})" if web_url and ticket_key != 'NO-KEY' else ticket_key
                markdown += f"- [ ] {item_type} **{ticket_link}** {summary}\n"
                markdown += f"      *Priority: {priority} • Points: {story_points} • Status: {status}*\n\n"
    else:
        markdown += "No low priority items.\n\n"
    
    # Slack Items by Theme
    if slack_items:
        markdown += "---\n\n## 💬 Slack Items by Theme\n\n"
        categorized_slack = categorize_slack_items(slack_items)
        
        for category, category_items in categorized_slack.items():
            markdown += f"### {category} ({len(category_items)} items)\n\n"
            
            for item in sorted(category_items, key=lambda x: x.get('priority', 'P2')):
                priority = item.get('priority', 'Medium')
                description = item.get('description', 'No description')
                assignee = item.get('assignee', 'Unassigned')
                meeting = item.get('meeting_source', 'Unknown meeting')
                slack_url = item.get('slack_url', '')
                meeting_link = f"[{meeting}]({slack_url})" if slack_url else meeting
                
                priority_emoji = "🔴" if priority.startswith('P0') or priority.startswith('P1') or 'high' in priority.lower() else "🟡" if priority.startswith('P2') else "🟢"
                
                markdown += f"- [ ] {priority_emoji} **{priority}** {description}\n"
                markdown += f"      *Assigned to: {assignee}* • {meeting_link}\n\n"
    
    # Summary
    markdown += f"""---

## 📊 Summary

| Priority | Count | Type Breakdown |
|----------|-------|----------------|
| 🔴 High (P0/P1) | {high_priority} | {len([i for i in high_priority_items if i.get('type') == 'slack'])} Slack, {len([i for i in high_priority_items if i.get('type') == 'jira'])} JIRA |
| 🟡 Medium (P2) | {medium_priority} | {len([i for i in medium_priority_items if i.get('type') == 'slack'])} Slack, {len([i for i in medium_priority_items if i.get('type') == 'jira'])} JIRA |
| 🟢 Low (P3+) | {low_priority} | {len([i for i in low_priority_items if i.get('type') == 'slack'])} Slack, {len([i for i in low_priority_items if i.get('type') == 'jira'])} JIRA |
| **📋 Total** | **{total_count}** | **{len(slack_items)} Slack, {len(jira_items)} JIRA** |

### 🎯 Focus Areas
- **Immediate**: {high_priority} high priority items need attention
- **This Week**: {medium_priority} medium priority items for planning
- **Ongoing**: {low_priority} low priority items for future scheduling

---
*Generated on {human_date} • Use checkboxes to track completion*
"""
    
    return markdown

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    date = sys.argv[1] if len(sys.argv) > 1 else None
    workspaces_dir = sys.argv[2] if len(sys.argv) > 2 else "/home/alexanderdelre/adr_llm_sandbox/workspaces"
    
    # Scan workspaces and generate todo list for specific date
    items = scan_workspaces(workspaces_dir, date)
    markdown = generate_todo_markdown(items, date)
    
    print(markdown)