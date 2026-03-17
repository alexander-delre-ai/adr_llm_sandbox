#!/usr/bin/env python3
"""
Task mapping logic to convert daily todos to TickTick task format.
Handles both Slack items and JIRA tickets with proper formatting and metadata.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from ticktick_client import map_priority, format_task_content, generate_task_tags

MAX_TITLE_WORDS = 15


def create_concise_title(text: str) -> str:
    """
    Create a concise, action-oriented title from the full description.
    Aims for 15 words or less while preserving the key action and context.
    Uses intelligent parsing to create meaningful titles similar to the examples.
    """
    words = text.split()
    if len(words) <= MAX_TITLE_WORDS:
        return text
    
    text_lower = text.lower()
    
    # Pattern matching based on the examples provided
    # Example 1: "Document the purpose..." -> "add documentation for test_only targets..."
    if text_lower.startswith('document '):
        # Convert "Document X" to "add documentation for X"
        # Find the main subject after "document the purpose and usage of"
        if 'purpose and usage of' in text_lower:
            after_purpose = text[text_lower.find('purpose and usage of') + len('purpose and usage of'):].strip()
            subject_words = after_purpose.split()
            # Take key terms, but include important technical terms
            key_terms = []
            for word in subject_words:
                if word.lower() in ['in', 'the', '.', 'consult', 'with']:
                    break
                key_terms.append(word)
            if key_terms:
                # Include more terms for technical documentation
                key_phrase = ' '.join(key_terms[:10])  # Allow up to 10 words for the subject
                title = f"add documentation for {key_phrase}"
                # Ensure we don't exceed 15 words total
                if len(title.split()) <= MAX_TITLE_WORDS:
                    return title
                else:
                    # Truncate if too long
                    return f"add documentation for {' '.join(key_terms[:8])}"
        else:
            # Generic document case
            subject = ' '.join(words[1:8])  # Skip "Document" and take next 7 words
            return f"add documentation for {subject}"
    
    # Example 2: "Verify if Komatsu should have..." -> "Verify if Komatsu can have..."
    elif text_lower.startswith('verify '):
        # For verify statements, keep the core question but simplify
        if 'should have' in text_lower:
            # Replace "should have" with "can have" and truncate at natural break
            modified = text.replace('should have', 'can have')
            # Find natural break point
            for break_phrase in [' and confirm', ' and get', '. Get', '. Consult']:
                if break_phrase in modified:
                    return modified[:modified.find(break_phrase)]
            # Fallback: take first part
            return ' '.join(modified.split()[:10])
        else:
            # Generic verify case
            return ' '.join(words[:12])
    
    # Handle other common action verbs
    elif any(text_lower.startswith(verb + ' ') for verb in ['create', 'schedule', 'coordinate', 'check', 'set up', 'work with', 'share', 'follow up']):
        # For other action verbs, take the action + main object
        # Find natural break points
        for break_phrase in ['. ', ' and ', ' to ', ' for ', ' with ']:
            if break_phrase in text:
                first_part = text[:text.find(break_phrase)]
                if len(first_part.split()) <= MAX_TITLE_WORDS:
                    return first_part
        # Fallback: take first 12 words for action items
        return ' '.join(words[:12])
    
    # Default case: try to find natural break points
    # Look for sentence endings, conjunctions, or prepositional phrases
    break_points = ['. ', ' and ', ' to ', ' for ', ' with ', ' in ', ' on ', ' at ']
    
    for break_phrase in break_points:
        if break_phrase in text:
            first_part = text[:text.find(break_phrase)]
            if 5 <= len(first_part.split()) <= MAX_TITLE_WORDS:
                return first_part
    
    # Final fallback: just take first 15 words
    return ' '.join(words[:MAX_TITLE_WORDS])


def map_slack_item_to_task(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Slack action item to TickTick task format.
    Title: Concise action-oriented title (15 words or less)
    Content: Full original description + meeting metadata
    """
    full_description = item.get('description', 'No description')
    
    # Create concise title
    title = create_concise_title(full_description)
    
    # Build detailed content with full description and metadata
    content_parts = [full_description]
    content_parts.append('')
    meeting_source = item.get('meeting_source', 'Unknown')
    content_parts.append(f"Meeting: {meeting_source}")
    content_parts.append(f"Assigned: {item.get('assignee', 'Unassigned')}")

    task_data = {
        'title': title,
        'content': '\n'.join(content_parts),
        'priority': map_priority(item.get('priority', 'P2')),
        'tags': generate_task_tags(item),
        'isAllDay': False,
        'timeZone': 'America/Los_Angeles',
    }

    priority = item.get('priority', '').lower()
    if priority in ['p0', 'p1', 'high']:
        due_date = datetime.now() + timedelta(days=1)
        task_data['dueDate'] = due_date.isoformat()

    if 'schedule' in full_description.lower() or 'meeting' in full_description.lower():
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
    Title: Concise action-oriented title (15 words or less)
    Content: Full description + metadata
    """
    full_text = item.get('description') or item.get('summary', 'Unknown task')
    title = create_concise_title(full_text)
    priority_str = item.get('priority', 'P2')

    content_parts = [full_text, '']
    content_parts.append(f"Assigned: {item.get('assignee', 'Unassigned')}")

    return {
        'title': title,
        'content': '\n'.join(content_parts),
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
    
    # Title length check (reasonable limit for concise titles)
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