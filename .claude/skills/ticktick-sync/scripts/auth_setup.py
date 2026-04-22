#!/usr/bin/env python3
"""
TickTick authentication setup and validation script.
Guides users through OAuth 2.0 flow and validates access tokens.
"""

import os
import sys
import json
import webbrowser
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ticktick_client import TickTickClient, TickTickAPIError
except ImportError:
    print("Error: Could not import TickTick client. Make sure ticktick_client.py is in the same directory.")
    sys.exit(1)


class TickTickAuthSetup:
    """Helper class for TickTick authentication setup."""
    
    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.env_file = self.skill_dir / '.env'
        self.env_example_file = self.skill_dir / 'env.example'
    
    def print_banner(self):
        """Print setup banner."""
        print("=" * 60)
        print("           TickTick Authentication Setup")
        print("=" * 60)
        print()
    
    def check_existing_token(self) -> Optional[str]:
        """Check if there's an existing valid token."""
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if line.startswith('TICKTICK_ACCESS_TOKEN='):
                            token = line.split('=', 1)[1].strip().strip('"\'')
                            if token and token != 'your_access_token_here':
                                return token
            except Exception as e:
                print(f"Warning: Could not read existing .env file: {e}")
        return None
    
    def validate_token(self, token: str) -> bool:
        """Validate access token."""
        print(f"Validating access token...")
        
        try:
            client = TickTickClient(token)
            user_info = client.get_user_info()
            
            print(f"✅ Token is valid!")
            print(f"   User: {user_info.get('username', 'Unknown')}")
            print(f"   Email: {user_info.get('email', 'Unknown')}")
            return True
            
        except TickTickAPIError as e:
            print(f"❌ Token validation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during validation: {e}")
            return False
    
    def show_oauth_instructions(self):
        """Show OAuth 2.0 setup instructions."""
        print("🔐 TickTick OAuth 2.0 Setup Instructions")
        print("-" * 40)
        print()
        print("1. Go to TickTick Developer Center:")
        print("   https://developer.ticktick.com/manage")
        print()
        print("2. Sign in with your TickTick account")
        print()
        print("3. Create a new application:")
        print("   - Click 'Create App'")
        print("   - Enter app name: 'Daily Todos Sync'")
        print("   - Enter description: 'Sync daily todos to TickTick'")
        print("   - Leave 'App Service URL' field EMPTY (this is not the redirect URI)")
        print("   - CRITICAL: In the 'OAuth redirect URL' field (at bottom), enter EXACTLY: http://localhost:5466/callback")
        print("   - Do NOT use https, do NOT add trailing slash, do NOT use different port")
        print("   - IMPORTANT: Make sure to SAVE the app after entering the OAuth redirect URL")
        print("   - VERIFY: After saving, the 'OAuth redirect URL' field should show: http://localhost:5466/callback")
        print()
        print("4. Note your Client ID and Client Secret")
        print()
        print("5. VERIFY the redirect URI is saved:")
        print("   - Go back to your app in the developer console")
        print("   - Check that 'http://localhost:5466/callback' appears in the redirect URI field")
        print("   - If it's empty, re-enter it and save again")
        print()
        print("6. Get authorization code:")
        print("   - Go to: https://ticktick.com/oauth/authorize")
        print("   - Add parameters:")
        print("     ?client_id=YOUR_CLIENT_ID")
        print("     &scope=tasks:read+tasks:write")
        print("     &redirect_uri=http://localhost:5466/callback")
        print("     &response_type=code")
        print()
        print("7. After authorization, you'll get a code in the redirect URL")
        print()
        print("8. Exchange code for access token:")
        print("   - Make POST request to: https://ticktick.com/oauth/token")
        print("   - Headers: Authorization: Basic base64(client_id:client_secret)")
        print("   - Body: grant_type=authorization_code&code=YOUR_CODE&redirect_uri=http://localhost:5466/callback")
        print()
    
    def get_authorization_url(self, client_id: str) -> str:
        """Generate OAuth authorization URL."""
        params = {
            'client_id': client_id,
            'scope': 'tasks:read tasks:write',
            'redirect_uri': 'http://localhost:5466/callback',
            'response_type': 'code',
            'state': 'ticktick_sync_setup'  # CSRF protection
        }
        
        base_url = 'https://ticktick.com/oauth/authorize'
        return f"{base_url}?{urllib.parse.urlencode(params)}"
    
    def interactive_setup(self):
        """Interactive OAuth setup process."""
        print("🚀 Interactive OAuth Setup")
        print("-" * 25)
        print()
        
        # Get client credentials
        print("Enter your TickTick app credentials:")
        client_id = input("Client ID: ").strip()
        if not client_id:
            print("❌ Client ID is required")
            return False
        
        client_secret = input("Client Secret: ").strip()
        if not client_secret:
            print("❌ Client Secret is required")
            return False
        
        # Generate authorization URL
        auth_url = self.get_authorization_url(client_id)
        
        print()
        print("📱 Opening authorization URL in browser...")
        print(f"URL: {auth_url}")
        print()
        
        try:
            webbrowser.open(auth_url)
        except Exception as e:
            print("Could not open browser automatically. Please copy the URL above.")
        
        print("After authorizing, you'll be redirected to a localhost URL like:")
        print("http://localhost:5466/callback?code=YOUR_CODE&state=ticktick_sync_setup")
        print()
        print("⚠️  IMPORTANT: The page will show 'ERR_EMPTY_RESPONSE' - this is NORMAL!")
        print("   There's no server running, so the browser can't load the page.")
        print("   Just copy the 'code' value from the URL bar (everything after 'code=' until '&').")
        print()
        print("Example: If URL is http://localhost:5466/callback?code=ABC123&state=...")
        print("         Then copy: ABC123")
        print()
        print("If you see a different OAuth error, copy the entire error message.")
        print()
        
        auth_code_or_error = input("Authorization code (or paste error message if you got one): ").strip()
        if not auth_code_or_error:
            print("❌ Authorization code is required")
            return False
        
        # Check if user pasted an error message instead of auth code
        if "error" in auth_code_or_error.lower():
            print("❌ Detected OAuth error in your input:")
            print(f"   {auth_code_or_error}")
            print()
            print("This confirms the redirect URI is not properly configured.")
            print("Please double-check your TickTick app settings.")
            return False
        
        auth_code = auth_code_or_error
        
        # Exchange code for token
        print("🔄 Exchanging code for access token...")
        
        token = self.exchange_code_for_token(client_id, client_secret, auth_code)
        
        if token:
            print("✅ Successfully obtained access token!")
            return self.save_token(token)
        else:
            print("❌ Failed to obtain access token")
            return False
    
    def exchange_code_for_token(self, client_id: str, client_secret: str, auth_code: str) -> Optional[str]:
        """Exchange authorization code for access token."""
        import requests
        import base64
        
        # Prepare authentication
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        # Prepare request
        url = 'https://ticktick.com/oauth/token'
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': 'http://localhost:5466/callback'
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                return token_data.get('access_token')
            else:
                print(f"❌ Token exchange failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error during token exchange: {e}")
            return None
    
    def manual_token_entry(self):
        """Manual token entry for users who have tokens already."""
        print("🔑 Manual Token Entry")
        print("-" * 20)
        print()
        print("If you already have a TickTick access token, enter it below.")
        print("You can obtain one through the OAuth flow or TickTick Developer Console.")
        print()
        
        token = input("Access Token: ").strip()
        if not token:
            print("❌ Access token is required")
            return False
        
        if self.validate_token(token):
            return self.save_token(token)
        else:
            return False
    
    def save_token(self, token: str) -> bool:
        """Save token to .env file."""
        try:
            # Create .env file from example if it doesn't exist
            if not self.env_file.exists() and self.env_example_file.exists():
                with open(self.env_example_file, 'r') as src:
                    content = src.read()
                with open(self.env_file, 'w') as dst:
                    dst.write(content)
            
            # Update or create .env file
            env_content = []
            token_updated = False
            
            if self.env_file.exists():
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if line.startswith('TICKTICK_ACCESS_TOKEN='):
                            env_content.append(f'TICKTICK_ACCESS_TOKEN={token}\n')
                            token_updated = True
                        else:
                            env_content.append(line)
            
            if not token_updated:
                env_content.append(f'TICKTICK_ACCESS_TOKEN={token}\n')
            
            with open(self.env_file, 'w') as f:
                f.writelines(env_content)
            
            print(f"✅ Token saved to {self.env_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving token: {e}")
            return False
    
    def test_api_access(self, token: str):
        """Test API access with various operations."""
        print("🧪 Testing API Access")
        print("-" * 19)
        print()
        
        try:
            client = TickTickClient(token)
            
            # Test 1: Test basic API connectivity with projects
            print("1. Testing API connectivity...")
            
            
            # Test 2: List projects
            print("2. Testing project access...")
            
            try:
                projects = client.get_projects()
                print(f"   ✅ Found {len(projects)} projects")
                
            except Exception as e:
                print(f"   ❌ API test failed: {e}")
                return
            
            # Test 3: Create test project (and delete it)
            print("3. Testing project creation...")
            test_project = client.create_project("TickTick Sync Test")
            project_id = test_project.get('id')
            print(f"   ✅ Created test project: {project_id}")
            
            # Test 4: Create test task
            print("4. Testing task creation...")
            test_task = {
                'title': 'Test Task - Safe to Delete',
                'content': 'This is a test task created during setup',
                'priority': 1
            }
            created_task = client.create_task(project_id, test_task)
            print(f"   ✅ Created test task: {created_task.get('id')}")
            
            # Cleanup: Delete test task and project
            print("5. Cleaning up test data...")
            if created_task.get('id'):
                client.delete_task(created_task['id'])
            client._make_request('DELETE', f'/project/{project_id}')
            print("   ✅ Cleanup completed")
            
            print()
            print("🎉 All API tests passed! TickTick integration is ready.")
            return True
            
        except Exception as e:
            print(f"   ❌ API test failed: {e}")
            return False
    
    def run_setup(self):
        """Run the complete setup process."""
        self.print_banner()
        
        # Check for existing token
        existing_token = self.check_existing_token()
        if existing_token:
            print("🔍 Found existing access token")
            if self.validate_token(existing_token):
                print("✅ Existing token is valid!")
                
                # Ask if user wants to test API
                test_api = input("\nRun API tests? (y/n): ").lower().startswith('y')
                if test_api:
                    self.test_api_access(existing_token)
                
                print("\n🎉 Setup complete! You can now sync todos to TickTick.")
                return True
            else:
                print("❌ Existing token is invalid. Setting up new token...")
        
        # Setup new token
        print("\nChoose setup method:")
        print("1. Interactive OAuth setup (recommended)")
        print("2. Manual token entry")
        print("3. Show OAuth instructions only")
        print()
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            success = self.interactive_setup()
        elif choice == '2':
            success = self.manual_token_entry()
        elif choice == '3':
            self.show_oauth_instructions()
            return True
        else:
            print("❌ Invalid choice")
            return False
        
        if success:
            # Test the new token
            token = self.check_existing_token()
            if token:
                test_api = input("\nRun API tests? (y/n): ").lower().startswith('y')
                if test_api:
                    self.test_api_access(token)
            
            print("\n🎉 Setup complete! You can now sync todos to TickTick.")
            print(f"Configuration saved to: {self.env_file}")
        
        return success


def main():
    """Main entry point."""
    setup = TickTickAuthSetup()
    
    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()