#!/usr/bin/env python3
"""
Main sync process for syncing daily todos to TickTick.
Handles data loading, project management, task creation, and error reporting.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ticktick_client import TickTickClient, TickTickAPIError
    from task_mapper import (
        batch_map_todos_to_tasks, 
        categorize_todos_by_type,
        filter_todos_by_assignee,
        validate_task_data,
        sanitize_task_data,
        generate_task_summary
    )
except ImportError as e:
    print(f"Error: Could not import required modules: {e}")
    sys.exit(1)

# Add daily-todos script directory to path
daily_todos_script_dir = Path(__file__).parent.parent.parent / 'daily-todos' / 'scripts'
sys.path.insert(0, str(daily_todos_script_dir))

try:
    from parse_workspaces import scan_workspaces
except ImportError:
    print("Error: Could not import daily-todos parse_workspaces module")
    print(f"Expected path: {daily_todos_script_dir}")
    sys.exit(1)


class TickTickSyncManager:
    """Main class for managing TickTick synchronization."""
    
    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.workspace_root = self.skill_dir.parent.parent.parent
        self.config = self.load_config()
        self.client = None
        
        # Sync statistics
        self.stats = {
            'total_todos': 0,
            'tasks_created': 0,
            'tasks_skipped': 0,
            'errors': []
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables and .env file."""
        config = {
            'access_token': None,
            'project_name': 'Daily Todos',
            'sync_enabled': True,
            'batch_size': 10,
            'auto_cleanup': True,
            'debug': False,
            'dry_run': False
        }
        
        # Try to load from .env file
        env_file = self.skill_dir / '.env'
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            
                            if key == 'TICKTICK_ACCESS_TOKEN':
                                config['access_token'] = value
                            elif key == 'TICKTICK_PROJECT_NAME':
                                config['project_name'] = value
                            elif key == 'TICKTICK_SYNC_ENABLED':
                                config['sync_enabled'] = value.lower() in ['true', '1', 'yes']
                            elif key == 'TICKTICK_BATCH_SIZE':
                                config['batch_size'] = int(value)
                            elif key == 'TICKTICK_AUTO_CLEANUP':
                                config['auto_cleanup'] = value.lower() in ['true', '1', 'yes']
                            elif key == 'TICKTICK_DEBUG':
                                config['debug'] = value.lower() in ['true', '1', 'yes']
                            elif key == 'TICKTICK_DRY_RUN':
                                config['dry_run'] = value.lower() in ['true', '1', 'yes']
            except Exception as e:
                print(f"Warning: Error reading .env file: {e}")
        
        # Override with environment variables
        config['access_token'] = os.getenv('TICKTICK_ACCESS_TOKEN', config['access_token'])
        config['project_name'] = os.getenv('TICKTICK_PROJECT_NAME', config['project_name'])
        config['sync_enabled'] = os.getenv('TICKTICK_SYNC_ENABLED', str(config['sync_enabled'])).lower() in ['true', '1', 'yes']
        config['batch_size'] = int(os.getenv('TICKTICK_BATCH_SIZE', str(config['batch_size'])))
        config['auto_cleanup'] = os.getenv('TICKTICK_AUTO_CLEANUP', str(config['auto_cleanup'])).lower() in ['true', '1', 'yes']
        config['debug'] = os.getenv('TICKTICK_DEBUG', str(config['debug'])).lower() in ['true', '1', 'yes']
        config['dry_run'] = os.getenv('TICKTICK_DRY_RUN', str(config['dry_run'])).lower() in ['true', '1', 'yes']
        
        return config
    
    def debug_print(self, message: str):
        """Print debug message if debug mode is enabled."""
        if self.config['debug']:
            print(f"[DEBUG] {message}")
    
    def initialize_client(self) -> bool:
        """Initialize TickTick client and validate authentication."""
        if not self.config['access_token']:
            print("❌ No TickTick access token found.")
            print("Run: python3 .cursor/skills/ticktick-sync/scripts/auth_setup.py")
            return False
        
        if not self.config['sync_enabled']:
            print("ℹ️  TickTick sync is disabled in configuration")
            return False
        
        try:
            self.client = TickTickClient(self.config['access_token'])
            
            # Validate token
            if not self.client.validate_token():
                print("❌ TickTick access token is invalid.")
                print("Run: python3 .cursor/skills/ticktick-sync/scripts/auth_setup.py")
                return False
            
            self.debug_print("TickTick client initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing TickTick client: {e}")
            return False
    
    def load_todos_data(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load todos data from workspace scan."""
        try:
            workspaces_dir = self.workspace_root / 'workspaces'
            self.debug_print(f"Scanning workspaces in: {workspaces_dir}")
            
            # Scan workspaces using daily-todos logic
            items = scan_workspaces(str(workspaces_dir))
            
            # Combine all items
            all_todos = []
            all_todos.extend(items.get('slack', []))
            all_todos.extend(items.get('jira', []))
            
            # Filter for AlexD
            filtered_todos = filter_todos_by_assignee(all_todos, 'AlexD')
            
            self.debug_print(f"Loaded {len(filtered_todos)} todos for AlexD")
            return filtered_todos
            
        except Exception as e:
            print(f"❌ Error loading todos data: {e}")
            return []
    
    def get_or_create_project(self, date: str) -> Optional[Dict[str, Any]]:
        """Get or create daily project for the given date."""
        project_name = f"{self.config['project_name']} - {date}"
        
        try:
            # Check if project already exists
            project = self.client.get_project_by_name(project_name)
            if project:
                self.debug_print(f"Found existing project: {project_name}")
                return project
            
            # Create new project
            if self.config['dry_run']:
                print(f"[DRY RUN] Would create project: {project_name}")
                return {'id': 'dry_run_project_id', 'name': project_name}
            else:
                project = self.client.create_project(project_name)
                print(f"✅ Created TickTick project: {project_name}")
                return project
                
        except Exception as e:
            print(f"❌ Error managing project '{project_name}': {e}")
            return None
    
    def check_existing_tasks(self, project_id: str, tasks: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Check for existing tasks to avoid duplicates."""
        if self.config['dry_run']:
            return tasks, []  # In dry run, assume no existing tasks
        
        try:
            existing_tasks = self.client.get_tasks(project_id)
            existing_titles = {task.get('title', '') for task in existing_tasks}
            
            new_tasks = []
            skipped_tasks = []
            
            for task in tasks:
                task_title = task.get('title', '')
                if task_title in existing_titles:
                    skipped_tasks.append(task)
                    self.debug_print(f"Skipping duplicate task: {task_title}")
                else:
                    new_tasks.append(task)
            
            return new_tasks, skipped_tasks
            
        except Exception as e:
            print(f"❌ Error checking existing tasks: {e}")
            return tasks, []  # On error, proceed with all tasks
    
    def create_tasks_in_batches(self, project_id: str, tasks: List[Dict[str, Any]]) -> int:
        """Create tasks in batches to respect API limits."""
        if not tasks:
            return 0
        
        created_count = 0
        batch_size = self.config['batch_size']
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            
            try:
                if self.config['dry_run']:
                    print(f"[DRY RUN] Would create batch of {len(batch)} tasks")
                    created_count += len(batch)
                else:
                    # Validate and sanitize tasks
                    valid_tasks = []
                    for task in batch:
                        if validate_task_data(task):
                            sanitized_task = sanitize_task_data(task)
                            valid_tasks.append(sanitized_task)
                        else:
                            self.stats['errors'].append(f"Invalid task data: {task.get('title', 'Unknown')}")
                    
                    if valid_tasks:
                        if len(valid_tasks) == 1:
                            # Single task creation
                            result = self.client.create_task(project_id, valid_tasks[0])
                            if result:
                                created_count += 1
                                self.debug_print(f"Created task: {valid_tasks[0]['title']}")
                        else:
                            # Batch creation
                            result = self.client.batch_create_tasks(project_id, valid_tasks)
                            if result:
                                created_count += len(valid_tasks)
                                self.debug_print(f"Created batch of {len(valid_tasks)} tasks")
                
            except Exception as e:
                error_msg = f"Error creating batch {i//batch_size + 1}: {e}"
                print(f"❌ {error_msg}")
                self.stats['errors'].append(error_msg)
        
        return created_count
    
    def cleanup_old_projects(self):
        """Clean up old daily todo projects."""
        if not self.config['auto_cleanup'] or self.config['dry_run']:
            return
        
        try:
            deleted_count = self.client.cleanup_old_projects(days_old=30)
            if deleted_count > 0:
                print(f"🧹 Cleaned up {deleted_count} old projects")
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")
    
    def sync_todos(self, date: Optional[str] = None) -> bool:
        """Main sync process."""
        # Use current date if not specified
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"🔄 Syncing daily todos to TickTick for {date}")
        
        # Initialize client
        if not self.initialize_client():
            return False
        
        # Load todos data
        todos = self.load_todos_data(date)
        if not todos:
            print("ℹ️  No todos found to sync")
            return True
        
        self.stats['total_todos'] = len(todos)
        print(f"📋 Found {len(todos)} todos to sync")
        
        # Get or create project
        project = self.get_or_create_project(date)
        if not project:
            return False
        
        project_id = project['id']
        
        # Convert todos to TickTick tasks
        print("🔄 Converting todos to TickTick tasks...")
        tasks = batch_map_todos_to_tasks(todos)
        
        if not tasks:
            print("❌ No valid tasks could be created from todos")
            return False
        
        # Check for existing tasks to avoid duplicates
        print("🔍 Checking for existing tasks...")
        new_tasks, skipped_tasks = self.check_existing_tasks(project_id, tasks)
        
        self.stats['tasks_skipped'] = len(skipped_tasks)
        
        if skipped_tasks:
            print(f"⏭️  Skipping {len(skipped_tasks)} duplicate tasks")
        
        if not new_tasks:
            print("ℹ️  All tasks already exist in TickTick")
            return True
        
        # Create tasks
        print(f"📝 Creating {len(new_tasks)} new tasks...")
        created_count = self.create_tasks_in_batches(project_id, new_tasks)
        
        self.stats['tasks_created'] = created_count
        
        # Cleanup old projects
        if self.config['auto_cleanup']:
            self.cleanup_old_projects()
        
        return True
    
    def print_summary(self):
        """Print sync summary."""
        print("\n" + "=" * 50)
        print("           SYNC SUMMARY")
        print("=" * 50)
        print(f"📊 Total todos processed: {self.stats['total_todos']}")
        print(f"✅ Tasks created: {self.stats['tasks_created']}")
        print(f"⏭️  Tasks skipped (duplicates): {self.stats['tasks_skipped']}")
        
        if self.stats['errors']:
            print(f"❌ Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more")
        
        if self.config['dry_run']:
            print("\n🧪 DRY RUN MODE - No actual changes were made")
        
        print("=" * 50)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sync daily todos to TickTick')
    parser.add_argument('date', nargs='?', help='Date to sync (YYYY-MM-DD), defaults to today')
    parser.add_argument('--dry-run', action='store_true', help='Test mode without creating tasks')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--no-cleanup', action='store_true', help='Skip cleanup of old projects')
    
    args = parser.parse_args()
    
    # Validate date format if provided
    if args.date:
        try:
            datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)
    
    # Initialize sync manager
    sync_manager = TickTickSyncManager()
    
    # Override config with command line arguments
    if args.dry_run:
        sync_manager.config['dry_run'] = True
    if args.debug:
        sync_manager.config['debug'] = True
    if args.no_cleanup:
        sync_manager.config['auto_cleanup'] = False
    
    try:
        # Run sync
        success = sync_manager.sync_todos(args.date)
        
        # Print summary
        sync_manager.print_summary()
        
        if success:
            if sync_manager.stats['tasks_created'] > 0:
                print(f"\n🎉 Successfully synced {sync_manager.stats['tasks_created']} tasks to TickTick!")
            else:
                print("\n✅ Sync completed - no new tasks to create")
        else:
            print("\n❌ Sync failed")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n❌ Sync cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if sync_manager.config['debug']:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()