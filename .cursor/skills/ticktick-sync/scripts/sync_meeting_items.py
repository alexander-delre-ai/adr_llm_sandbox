#!/usr/bin/env python3
"""
Syncs meeting action items from a tickets.md file to TickTick.
Filters to Slack-tracked items assigned to AlexD or Unassigned.
Reuses ticktick_client.py for API calls and task_mapper.py for validation.

Title format: 15 words or less (condensed from heading).
Content format: full description text, then meeting metadata.
"""

import os
import re
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ticktick_client import TickTickClient, TickTickAPIError, map_priority
from task_mapper import validate_task_data, sanitize_task_data

MAX_TITLE_WORDS = 15
ALEXD_ALIASES = {'alexd', 'alex del re', 'unassigned', ''}


def parse_tickets_md(filepath: str) -> List[Dict[str, Any]]:
    """
    Parse a tickets.md file and extract action items with their YAML fields.
    Returns a list of dicts: title, tracking, priority, assignee, description, etc.
    """
    text = Path(filepath).read_text(encoding='utf-8')
    items: List[Dict[str, Any]] = []

    heading_pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)
    yaml_pattern = re.compile(r'```yaml\s*\n(.*?)```', re.DOTALL)

    headings = list(heading_pattern.finditer(text))

    for i, match in enumerate(headings):
        title = match.group(1).strip()
        if title.lower() == 'instructions':
            continue

        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section = text[start:end]

        yaml_match = yaml_pattern.search(section)
        if not yaml_match:
            continue

        fields = _parse_yaml_block(yaml_match.group(1))
        fields['title'] = title
        items.append(fields)

    return items


def _parse_yaml_block(raw: str) -> Dict[str, str]:
    """Parse a simple YAML block into a dict (flat key: value pairs only)."""
    fields: Dict[str, str] = {}
    for line in raw.strip().splitlines():
        if ':' not in line:
            continue
        key, _, value = line.partition(':')
        fields[key.strip()] = value.strip()
    return fields


def shorten_title(title: str) -> str:
    """Shorten a title to MAX_TITLE_WORDS words, preserving meaning."""
    words = title.split()
    if len(words) <= MAX_TITLE_WORDS:
        return title
    return ' '.join(words[:MAX_TITLE_WORDS])


def filter_for_ticktick(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Keep only Slack-tracked items assigned to AlexD or Unassigned."""
    filtered = []
    for item in items:
        tracking = item.get('tracking', '').lower()
        if tracking != 'slack':
            continue
        assignee = item.get('assignee', '').lower()
        if assignee in ALEXD_ALIASES:
            filtered.append(item)
    return filtered


def map_meeting_item_to_task(item: Dict[str, Any], meeting_title: str,
                             meeting_slug: str) -> Dict[str, Any]:
    """
    Convert a meeting action item to a TickTick task dict.
    Title: condensed to 15 words or less from the heading.
    Content: full description text followed by meeting metadata.
    """
    short_title = shorten_title(item['title'])
    description = item.get('description', '')

    content_parts = []
    if description:
        content_parts.append(description)
    content_parts.append('')
    content_parts.append(f"Meeting: {meeting_slug}")

    tags = []
    if meeting_slug:
        tag = re.sub(r'[^a-z0-9-]', '', meeting_slug.lower())
        if tag:
            tags.append(tag)

    priority_str = item.get('priority', 'P2')
    task = {
        'title': short_title,
        'content': '\n'.join(content_parts),
        'priority': map_priority(priority_str),
        'tags': tags,
        'isAllDay': False,
        'timeZone': 'America/Los_Angeles',
    }

    if priority_str.lower() in ('p0', 'p1'):
        task['dueDate'] = (datetime.now() + timedelta(days=1)).isoformat()

    return task


def check_duplicates(skill_dir: Path,
                     tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter out tasks whose titles already exist in the duplicate tracker."""
    dup_file = skill_dir / '.task_duplicates.json'
    existing_titles: set = set()

    if dup_file.exists():
        try:
            data = json.loads(dup_file.read_text())
            existing_titles = set(data.get('task_titles', []))
        except Exception:
            pass

    new_tasks = [t for t in tasks if t['title'] not in existing_titles]
    new_titles = {t['title'] for t in new_tasks}

    if new_titles:
        try:
            all_titles = existing_titles | new_titles
            dup_file.write_text(json.dumps(
                {'task_titles': sorted(all_titles)}, indent=2))
        except Exception:
            pass

    return new_tasks


def sync(tickets_path: str, meeting_title: str,
         dry_run: bool = False, debug: bool = False) -> Dict[str, Any]:
    """
    Main entry point: parse tickets.md, filter, map, and push to TickTick.
    Returns a summary dict with counts and any errors.
    """
    skill_dir = Path(__file__).resolve().parent.parent
    stats = {
        'total': 0, 'filtered': 0, 'created': 0,
        'skipped_dup': 0, 'errors': []
    }

    items = parse_tickets_md(tickets_path)
    stats['total'] = len(items)
    if debug:
        print(f"[DEBUG] Parsed {len(items)} action items from tickets.md")

    eligible = filter_for_ticktick(items)
    stats['filtered'] = len(eligible)
    if not eligible:
        print("No Slack-tracked AlexD/Unassigned items to sync.")
        return stats

    meeting_slug = re.sub(r'[^a-z0-9]+', '-',
                          meeting_title.lower()).strip('-')

    tasks = [map_meeting_item_to_task(i, meeting_title, meeting_slug)
             for i in eligible]

    new_tasks = check_duplicates(skill_dir, tasks)
    stats['skipped_dup'] = len(tasks) - len(new_tasks)

    if not new_tasks:
        print("All eligible items already exist in TickTick.")
        return stats

    env_file = skill_dir / '.env'
    access_token = None
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith('TICKTICK_ACCESS_TOKEN='):
                access_token = line.split('=', 1)[1].strip().strip('"\'')
    access_token = os.getenv('TICKTICK_ACCESS_TOKEN', access_token)

    if not access_token:
        msg = "No TickTick access token found."
        stats['errors'].append(msg)
        print(f"Error: {msg}")
        return stats

    client = TickTickClient(access_token)
    if not client.validate_token():
        msg = "TickTick access token is invalid."
        stats['errors'].append(msg)
        print(f"Error: {msg}")
        return stats

    project = None
    for p in client.get_projects():
        if p.get('name') == 'Cursor Sync':
            project = p
            break
    if not project:
        if dry_run:
            project = {'id': 'dry-run', 'name': 'Cursor Sync'}
        else:
            project = client.create_project('Cursor Sync')

    project_id = project['id']

    for task in new_tasks:
        if not validate_task_data(task):
            stats['errors'].append(f"Invalid task: {task.get('title')}")
            continue
        sanitized = sanitize_task_data(task)
        if dry_run:
            print(f"[DRY RUN] Would create: {sanitized['title']}")
            stats['created'] += 1
        else:
            try:
                client.create_task(project_id, sanitized)
                stats['created'] += 1
                if debug:
                    print(f"[DEBUG] Created: {sanitized['title']}")
            except TickTickAPIError as e:
                stats['errors'].append(f"{sanitized['title']}: {e}")

    return stats


def print_summary(stats: Dict[str, Any]):
    print("\n" + "=" * 50)
    print("      TICKTICK MEETING SYNC SUMMARY")
    print("=" * 50)
    print(f"Total action items in tickets.md: {stats['total']}")
    print(f"Eligible (Slack + AlexD/Unassigned): {stats['filtered']}")
    print(f"Tasks created: {stats['created']}")
    if stats['skipped_dup']:
        print(f"Skipped (duplicates): {stats['skipped_dup']}")
    if stats['errors']:
        print(f"Errors: {len(stats['errors'])}")
        for err in stats['errors'][:5]:
            print(f"  - {err}")
    print("=" * 50)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Sync meeting action items to TickTick')
    parser.add_argument('--tickets', required=True,
                        help='Path to tickets.md file')
    parser.add_argument('--meeting', required=True,
                        help='Meeting title for task context')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if not Path(args.tickets).exists():
        print(f"Error: tickets file not found: {args.tickets}")
        sys.exit(1)

    stats = sync(args.tickets, args.meeting,
                 dry_run=args.dry_run, debug=args.debug)
    print_summary(stats)
    sys.exit(0 if not stats['errors'] else 1)


if __name__ == '__main__':
    main()
