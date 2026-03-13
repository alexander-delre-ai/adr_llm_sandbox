#!/usr/bin/env python3
"""
TickTick API client wrapper for task and project management.
Handles authentication, rate limiting, and API interactions.
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path


class TickTickAPIError(Exception):
    """Custom exception for TickTick API errors."""
    pass


class TickTickClient:
    """TickTick API client for managing projects and tasks."""
    
    def __init__(self, access_token: str, base_url: str = "https://api.ticktick.com/open/v1"):
        """
        Initialize TickTick client.
        
        Args:
            access_token: OAuth 2.0 access token
            base_url: API base URL (default: official TickTick API)
        """
        self.access_token = access_token
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'TickTick-Sync-Skill/1.0'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to TickTick API with rate limiting and error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request body data
            params: Query parameters
            
        Returns:
            Response JSON data
            
        Raises:
            TickTickAPIError: On API errors or network issues
        """
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            self.last_request_time = time.time()
            
            # Handle HTTP errors
            if response.status_code == 401:
                raise TickTickAPIError("Authentication failed. Please check your access token.")
            elif response.status_code == 403:
                raise TickTickAPIError("Insufficient permissions. Ensure your token has tasks:read and tasks:write scopes.")
            elif response.status_code == 429:
                # Rate limited - wait and retry once
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params)
            elif response.status_code >= 400:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        error_msg += f": {error_data['message']}"
                except:
                    error_msg += f": {response.text}"
                raise TickTickAPIError(error_msg)
            
            # Parse response
            if response.content:
                return response.json()
            else:
                return {}
                
        except requests.RequestException as e:
            raise TickTickAPIError(f"Network error: {str(e)}")
    
    def validate_token(self) -> bool:
        """
        Validate access token by making a test API call.
        
        Returns:
            True if token is valid, False otherwise
        """
        try:
            # Use projects endpoint instead of user info (which doesn't exist)
            self.get_projects()
            return True
        except TickTickAPIError:
            return False
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get user profile information.
        
        Returns:
            User profile data
        """
        return self._make_request('GET', '/user')
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Get list of all projects.
        
        Returns:
            List of project objects
        """
        response = self._make_request('GET', '/project')
        return response if isinstance(response, list) else []
    
    def create_project(self, name: str, color: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            name: Project name
            color: Project color (optional)
            
        Returns:
            Created project data
        """
        project_data = {
            'name': name,
            'color': color or '#3498db'  # Default blue color
        }
        return self._make_request('POST', '/project', data=project_data)
    
    def get_project_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find project by name.
        
        Args:
            name: Project name to search for
            
        Returns:
            Project data if found, None otherwise
        """
        projects = self.get_projects()
        for project in projects:
            if project.get('name') == name:
                return project
        return None
    
    def ensure_project_exists(self, name: str) -> Dict[str, Any]:
        """
        Ensure project exists, create if it doesn't.
        
        Args:
            name: Project name
            
        Returns:
            Project data (existing or newly created)
        """
        project = self.get_project_by_name(name)
        if project:
            return project
        else:
            return self.create_project(name)
    
    def get_tasks(self, project_id: str = None) -> List[Dict[str, Any]]:
        """
        Get all tasks, optionally filtered by project.
        
        Args:
            project_id: Optional project ID to filter tasks
            
        Returns:
            List of task objects
        """
        params = {}
        if project_id:
            params['projectId'] = project_id
        response = self._make_request('GET', '/task', params=params)
        return response if isinstance(response, list) else []
    
    def create_task(self, project_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a single task in a project.
        
        Args:
            project_id: Target project ID
            task_data: Task data dictionary
            
        Returns:
            Created task data
        """
        # Ensure project_id is included in task data
        task_data['projectId'] = project_id
        return self._make_request('POST', '/task', data=task_data)
    
    def batch_create_tasks(self, project_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple tasks in batch.
        
        Args:
            project_id: Target project ID
            tasks: List of task data dictionaries
            
        Returns:
            Batch operation result
        """
        # Try individual task creation since batch endpoint might not exist
        created_tasks = []
        errors = []
        
        for task in tasks:
            try:
                created_task = self.create_task(project_id, task.copy())
                created_tasks.append(created_task)
            except Exception as e:
                errors.append(str(e))
        
        return {
            'created': created_tasks,
            'errors': errors,
            'success_count': len(created_tasks),
            'error_count': len(errors)
        }
    
    def update_task(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing task.
        
        Args:
            task_id: Task ID to update
            task_data: Updated task data
            
        Returns:
            Updated task data
        """
        return self._make_request('POST', f'/task/{task_id}', data=task_data)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task ID to delete
            
        Returns:
            True if successful
        """
        try:
            self._make_request('DELETE', f'/task/{task_id}')
            return True
        except TickTickAPIError:
            return False
    
    def find_tasks_by_title_prefix(self, project_id: str, prefix: str) -> List[Dict[str, Any]]:
        """
        Find tasks in project with titles starting with given prefix.
        
        Args:
            project_id: Project ID to search in
            prefix: Title prefix to match
            
        Returns:
            List of matching tasks
        """
        tasks = self.get_tasks(project_id)
        return [task for task in tasks if task.get('title', '').startswith(prefix)]
    
    def cleanup_old_projects(self, days_old: int = 30) -> int:
        """
        Clean up old daily todo projects.
        
        Args:
            days_old: Delete projects older than this many days
            
        Returns:
            Number of projects deleted
        """
        projects = self.get_projects()
        deleted_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for project in projects:
            project_name = project.get('name', '')
            if project_name.startswith('Daily Todos - '):
                try:
                    # Extract date from project name
                    date_str = project_name.replace('Daily Todos - ', '')
                    project_date = datetime.strptime(date_str, '%Y-%m-%d')
                    
                    if project_date < cutoff_date:
                        # Delete old project
                        self._make_request('DELETE', f'/project/{project["id"]}')
                        deleted_count += 1
                except (ValueError, KeyError):
                    # Skip projects with invalid date format
                    continue
        
        return deleted_count


def map_priority(priority_str: str) -> int:
    """
    Map priority string to TickTick priority number.
    
    Args:
        priority_str: Priority string (P0, P1, P2, P3, High, Medium, Low)
        
    Returns:
        TickTick priority (0=P0/High, 1=P1/Medium, 2=P2/Low, 3=P3/None)
    """
    priority_lower = priority_str.lower()
    
    if priority_lower in ['p0', 'high', 'critical']:
        return 0  # P0/High
    elif priority_lower in ['p1', 'medium']:
        return 1  # P1/Medium  
    elif priority_lower in ['p2', 'low']:
        return 2  # P2/Low
    else:
        return 3  # P3/None


def format_task_content(item: Dict[str, Any]) -> str:
    """
    Format task content with metadata (no Slack links).
    
    Args:
        item: Todo item data
        
    Returns:
        Formatted content string
    """
    content_parts = []
    
    if item.get('type') == 'slack':
        content_parts.append(f"Meeting: {item.get('meeting_source', 'Unknown')}")
        content_parts.append(f"Assigned: {item.get('assignee', 'Unassigned')}")
        # Note: Slack links removed as requested
        # Theme is handled as tags/labels, not in content
    
    elif item.get('type') == 'jira':
        content_parts.append(f"Status: {item.get('status', 'Unknown')}")
        content_parts.append(f"Story Points: {item.get('story_points', 0)}")
        content_parts.append(f"Assignee: {item.get('assignee', 'Unassigned')}")
        if item.get('web_url'):
            content_parts.append(f"JIRA: {item['web_url']}")
        if item.get('meeting_source'):
            content_parts.append(f"Meeting: {item['meeting_source']}")
    
    return '\n'.join(content_parts)


def generate_task_tags(item: Dict[str, Any]) -> List[str]:
    """
    Generate tags for a task based on item metadata.
    Excludes Slack and priority tags as requested.
    
    Args:
        item: Todo item data
        
    Returns:
        List of tags (minimal set)
    """
    tags = []
    
    # Only add theme tag for Slack items (no type or priority tags)
    if item.get('type') == 'slack' and item.get('theme'):
        theme_tag = item['theme'].lower().replace(' ', '-').replace('&', 'and')
        tags.append(theme_tag)
    
    return tags