#!/usr/bin/env python3
"""
Task mapping logic to convert daily todos to TickTick task format.
Handles both Slack items and JIRA tickets with proper formatting and metadata.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from ticktick_client import map_priority, format_task_content, generate_task_tags


def map_slack_item_to_task(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Slack action item to TickTick task format.
    
    Args:
        item: Slack item data from daily todos
        
    Returns:
        TickTick task data dictionary
    """
    # Use clean description without priority labels for title
    description = item.get('description', 'No description')
    title = description
    if len(title) > 100:
        title = title[:97] + "..."
    
    # Generate task data
    task_data = {
        'title': title,
        'content': format_task_content(item),
        'priority': map_priority(item.get('priority', 'P2')),
        'tags': generate_task_tags(item),
        'isAllDay': False,
        'timeZone': 'America/Los_Angeles',  # Default timezone
    }
    
    # Add due date for high priority items (today + 1 day)
    priority = item.get('priority', '').lower()
    if priority in ['p0', 'p1', 'high']:
        due_date = datetime.now() + timedelta(days=1)
        task_data['dueDate'] = due_date.isoformat()
    
    # Add start date for scheduled items
    if 'schedule' in description.lower() or 'meeting' in description.lower():
        start_date = datetime.now()
        task_data['startDate'] = start_date.isoformat()
    
    return task_data


def map_jira_item_to_task(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert JIRA ticket to TickTick task format.
    
    Args:
        item: JIRA item data from daily todos
        
    Returns:
        TickTick task data dictionary
    """
    # Use ticket key and summary for title
    ticket_key = item.get('ticket_key', 'NO-KEY')
    summary = item.get('summary', 'No summary')
    title = f"[{ticket_key}] {summary}"
    if len(title) > 100:
        title = title[:97] + "..."
    
    # Generate task data
    task_data = {
        'title': title,
        'content': format_task_content(item),
        'priority': map_priority(item.get('priority', 'P2')),
        'tags': generate_task_tags(item),
        'isAllDay': False,
        'timeZone': 'America/Los_Angeles',  # Default timezone
    }
    
    # Add due date based on priority and story points
    priority = item.get('priority', '').lower()
    story_points = float(item.get('story_points', 0))
    
    if priority in ['p0', 'p1']:
        # High priority: due tomorrow
        due_date = datetime.now() + timedelta(days=1)
        task_data['dueDate'] = due_date.isoformat()
    elif story_points > 0:
        # Use story points to estimate due date (1 point = 1 week)
        days_to_add = max(int(story_points * 7), 3)  # Minimum 3 days
        due_date = datetime.now() + timedelta(days=days_to_add)
        task_data['dueDate'] = due_date.isoformat()
    
    return task_data


def map_todo_item_to_task(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Convert todo item to TickTick task format.
    Only processes Slack items - JIRA tickets are filtered out.
    
    Args:
        item: Todo item data (Slack or JIRA)
        
    Returns:
        TickTick task data dictionary for Slack items, None for JIRA items
    """
    item_type = item.get('type', 'unknown')
    
    if item_type == 'slack':
        return map_slack_item_to_task(item)
    elif item_type == 'jira':
        # Skip JIRA tickets - return None to filter them out
        return None
    else:
        # Generic mapping for unknown types
        return map_generic_item_to_task(item)


def map_generic_item_to_task(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert generic todo item to TickTick task format.
    
    Args:
        item: Generic item data
        
    Returns:
        TickTick task data dictionary
    """
    # Use description or summary for title
    title = item.get('description') or item.get('summary', 'Unknown task')
    priority_str = item.get('priority', 'P2')
    title = f"[{priority_str}] {title}"
    
    if len(title) > 100:
        title = title[:97] + "..."
    
    return {
        'title': title,
        'content': format_task_content(item),
        'priority': map_priority(priority_str),
        'tags': generate_task_tags(item),
        'isAllDay': False,
        'timeZone': 'America/Los_Angeles',
    }


def batch_map_todos_to_tasks(todos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert a list of todo items to TickTick tasks.
    Only processes Slack items - JIRA tickets are filtered out.
    
    Args:
        todos: List of todo items
        
    Returns:
        List of TickTick task data dictionaries (Slack items only)
    """
    tasks = []
    
    for todo in todos:
        try:
            task = map_todo_item_to_task(todo)
            # Only add non-None tasks (filters out JIRA items)
            if task is not None:
                tasks.append(task)
        except Exception as e:
            # Log error but continue with other tasks
            print(f"Warning: Failed to map todo item: {e}")
            print(f"Item data: {todo}")
            continue
    
    return tasks


def categorize_todos_by_type(todos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize todos by type for different processing.
    
    Args:
        todos: List of todo items
        
    Returns:
        Dictionary with 'slack' and 'jira' lists
    """
    categorized = {
        'slack': [],
        'jira': [],
        'other': []
    }
    
    for todo in todos:
        item_type = todo.get('type', 'other')
        if item_type in categorized:
            categorized[item_type].append(todo)
        else:
            categorized['other'].append(todo)
    
    return categorized


def filter_todos_by_priority(todos: List[Dict[str, Any]], min_priority: str = 'P3') -> List[Dict[str, Any]]:
    """
    Filter todos by minimum priority level.
    
    Args:
        todos: List of todo items
        min_priority: Minimum priority to include (P0, P1, P2, P3)
        
    Returns:
        Filtered list of todos
    """
    priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, 'HIGH': 0, 'MEDIUM': 2, 'LOW': 3}
    min_level = priority_order.get(min_priority.upper(), 3)
    
    filtered = []
    for todo in todos:
        priority = todo.get('priority', 'P3').upper()
        todo_level = priority_order.get(priority, 3)
        
        if todo_level <= min_level:
            filtered.append(todo)
    
    return filtered


def filter_todos_by_assignee(todos: List[Dict[str, Any]], assignee: str = 'AlexD') -> List[Dict[str, Any]]:
    """
    Filter todos by assignee.
    
    Args:
        todos: List of todo items
        assignee: Assignee name to filter by
        
    Returns:
        Filtered list of todos
    """
    filtered = []
    assignee_lower = assignee.lower()
    
    for todo in todos:
        todo_assignee = todo.get('assignee', '').lower()
        if assignee_lower in todo_assignee or todo_assignee in ['unassigned', '']:
            filtered.append(todo)
    
    return filtered


def validate_task_data(task: Dict[str, Any]) -> bool:
    """
    Validate TickTick task data before creation.
    
    Args:
        task: Task data dictionary
        
    Returns:
        True if valid, False otherwise
    """
    # Required fields
    if not task.get('title'):
        return False
    
    # Title length check
    if len(task.get('title', '')) > 200:
        return False
    
    # Priority validation
    priority = task.get('priority', 0)
    if not isinstance(priority, int) or priority not in [0, 1, 2, 3]:
        return False
    
    # Tags validation
    tags = task.get('tags', [])
    if not isinstance(tags, list):
        return False
    
    return True


def sanitize_task_data(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize task data to ensure TickTick API compatibility.
    
    Args:
        task: Task data dictionary
        
    Returns:
        Sanitized task data
    """
    sanitized = task.copy()
    
    # Ensure title is not too long
    if len(sanitized.get('title', '')) > 200:
        sanitized['title'] = sanitized['title'][:197] + "..."
    
    # Ensure content is not too long (TickTick limit is around 10000 chars)
    if len(sanitized.get('content', '')) > 5000:
        sanitized['content'] = sanitized['content'][:4997] + "..."
    
    # Ensure tags are strings and not too long
    tags = sanitized.get('tags', [])
    sanitized_tags = []
    for tag in tags:
        if isinstance(tag, str) and len(tag) <= 50:
            # Remove special characters that might cause issues
            clean_tag = ''.join(c for c in tag if c.isalnum() or c in '-_')
            if clean_tag:
                sanitized_tags.append(clean_tag)
    sanitized['tags'] = sanitized_tags[:10]  # Limit number of tags
    
    # Ensure priority is valid
    priority = sanitized.get('priority', 0)
    if priority not in [0, 1, 3, 5]:
        sanitized['priority'] = 0
    
    return sanitized


def generate_task_summary(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary statistics for a list of tasks.
    
    Args:
        tasks: List of task data dictionaries
        
    Returns:
        Summary statistics
    """
    if not tasks:
        return {
            'total_tasks': 0,
            'by_priority': {},
            'by_type': {},
            'has_due_dates': 0
        }
    
    # Count by priority
    priority_counts = {0: 0, 1: 0, 3: 0, 5: 0}
    for task in tasks:
        priority = task.get('priority', 0)
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    # Count by type (from tags)
    type_counts = {}
    for task in tasks:
        tags = task.get('tags', [])
        for tag in tags:
            if tag in ['slack', 'jira']:
                type_counts[tag] = type_counts.get(tag, 0) + 1
                break
    
    # Count tasks with due dates
    due_date_count = sum(1 for task in tasks if task.get('dueDate'))
    
    return {
        'total_tasks': len(tasks),
        'by_priority': {
            'none': priority_counts[0],
            'low': priority_counts[1],
            'medium': priority_counts[3],
            'high': priority_counts[5]
        },
        'by_type': type_counts,
        'has_due_dates': due_date_count
    }