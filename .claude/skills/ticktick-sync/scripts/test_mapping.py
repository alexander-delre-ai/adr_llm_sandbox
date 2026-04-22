#!/usr/bin/env python3
"""
Test script to validate task mapping logic without requiring TickTick authentication.
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_mapper import (
    map_slack_item_to_task,
    map_jira_item_to_task,
    batch_map_todos_to_tasks,
    generate_task_summary,
    validate_task_data,
    sanitize_task_data
)

def test_slack_mapping():
    """Test Slack item to task mapping."""
    print("🧪 Testing Slack item mapping...")
    
    slack_item = {
        'type': 'slack',
        'description': 'Schedule manager planning meetings with system engineering',
        'assignee': 'AlexD',
        'priority': 'P1',
        'meeting_source': '2026-03-10-katana-applied-sdv-sw-office-hours',
        'slack_url': 'https://appliedint.slack.com/archives/search?q=katana%20applied',
        'theme': 'Meeting Scheduling'
    }
    
    task = map_slack_item_to_task(slack_item)
    
    print(f"  Title: {task['title']}")
    print(f"  Priority: {task['priority']}")
    print(f"  Tags: {task['tags']}")
    print(f"  Content: {task['content'][:100]}...")
    print(f"  Valid: {validate_task_data(task)}")
    print()

def test_jira_mapping():
    """Test JIRA item to task mapping."""
    print("🧪 Testing JIRA item mapping...")
    
    jira_item = {
        'type': 'jira',
        'ticket_key': 'KATA-2573',
        'summary': 'Define mandatory hardware diagnostics requirements for each manager',
        'priority': 'P1',
        'story_points': 0.1,
        'status': 'Backlog',
        'assignee': 'Unassigned',
        'web_url': 'https://appliedint-katana.atlassian.net/browse/KATA-2573',
        'meeting_source': 'Katana Applied SDV SW Office Hours (Mar 10, 2026)'
    }
    
    task = map_jira_item_to_task(jira_item)
    
    print(f"  Title: {task['title']}")
    print(f"  Priority: {task['priority']}")
    print(f"  Tags: {task['tags']}")
    print(f"  Content: {task['content'][:100]}...")
    print(f"  Valid: {validate_task_data(task)}")
    print()

def test_batch_mapping():
    """Test batch mapping of mixed todos."""
    print("🧪 Testing batch mapping...")
    
    todos = [
        {
            'type': 'slack',
            'description': 'Check with Katana team on provisioning a Katana Jira admin',
            'assignee': 'AlexD',
            'priority': 'High',
            'meeting_source': '2026-03-12-katana-jira-setup-sync'
        },
        {
            'type': 'jira',
            'ticket_key': 'KATA-2571',
            'summary': 'Gather dependency information for vehicle managers',
            'priority': 'P1',
            'story_points': 0.1,
            'status': 'Backlog',
            'assignee': 'Unassigned',
            'web_url': 'https://appliedint-katana.atlassian.net/browse/KATA-2571'
        }
    ]
    
    tasks = batch_map_todos_to_tasks(todos)
    summary = generate_task_summary(tasks)
    
    print(f"  Input todos: {len(todos)}")
    print(f"  Output tasks: {len(tasks)}")
    print(f"  Summary: {summary}")
    print()

def test_sanitization():
    """Test task data sanitization."""
    print("🧪 Testing task sanitization...")
    
    # Create a task with potential issues
    problematic_task = {
        'title': 'A' * 250,  # Too long
        'content': 'B' * 6000,  # Too long
        'priority': 99,  # Invalid priority
        'tags': ['valid-tag', 'invalid tag with spaces', 'x' * 60, 123, None]  # Mixed valid/invalid tags
    }
    
    sanitized = sanitize_task_data(problematic_task)
    
    print(f"  Original title length: {len(problematic_task['title'])}")
    print(f"  Sanitized title length: {len(sanitized['title'])}")
    print(f"  Original content length: {len(problematic_task['content'])}")
    print(f"  Sanitized content length: {len(sanitized['content'])}")
    print(f"  Original priority: {problematic_task['priority']}")
    print(f"  Sanitized priority: {sanitized['priority']}")
    print(f"  Original tags: {problematic_task['tags']}")
    print(f"  Sanitized tags: {sanitized['tags']}")
    print(f"  Valid after sanitization: {validate_task_data(sanitized)}")
    print()

def main():
    """Run all tests."""
    print("=" * 60)
    print("           TickTick Task Mapping Tests")
    print("=" * 60)
    print()
    
    test_slack_mapping()
    test_jira_mapping()
    test_batch_mapping()
    test_sanitization()
    
    print("✅ All mapping tests completed successfully!")
    print()
    print("💡 To test with real TickTick integration:")
    print("   1. Run: python3 auth_setup.py")
    print("   2. Run: python3 sync_todos.py --dry-run")

if __name__ == '__main__':
    main()