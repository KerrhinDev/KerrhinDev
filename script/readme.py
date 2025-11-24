#!/usr/bin/env python3
"""
GitHub Profile README Generator
Automatically updates the README.md with recent GitHub activity
"""

import os
import re
from datetime import datetime
from github import Github

# Configuration
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'KerrhinDev')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
README_PATH = 'README.md'
MAX_REPOS = 3
MAX_COMMITS_PER_REPO = 3

def get_recent_activity():
    """Fetch recent activity from GitHub API"""
    if not AUTH_TOKEN:
        print("Warning: AUTH_TOKEN not set. Using unauthenticated requests (rate limited).")
        g = Github()
    else:
        g = Github(AUTH_TOKEN)
    
    try:
        user = g.get_user(GITHUB_USERNAME)
        repos = list(user.get_repos(sort='pushed', direction='desc'))[:MAX_REPOS]
        
        activity_md = ""
        
        for repo in repos:
            # Determine if repo is public or private
            visibility = "🔓" if not repo.private else "🔒"
            
            activity_md += f"\n### {visibility} [{repo.name}]({repo.html_url})\n\n"
            
            if repo.description:
                activity_md += f"{repo.description}\n\n"
            
            # Get recent commits
            try:
                commits = list(repo.get_commits()[:MAX_COMMITS_PER_REPO])
                
                if commits:
                    for commit in commits:
                        commit_msg = commit.commit.message.split('\n')[0]  # First line only
                        commit_url = commit.html_url
                        activity_md += f"- 📌 [{commit_msg}]({commit_url})\n"
                    activity_md += "\n"
            except Exception as e:
                print(f"Could not fetch commits for {repo.name}: {e}")
                activity_md += "*No recent commits*\n\n"
        
        return activity_md.strip()
    
    except Exception as e:
        print(f"Error fetching activity: {e}")
        return "*Unable to fetch recent activity*"

def update_readme(activity_content):
    """Update README.md with new activity content"""
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            readme = f.read()
        
        # Replace content between markers
        pattern = r'<!-- RECENT_ACTIVITY:START -->.*?<!-- RECENT_ACTIVITY:END -->'
        replacement = f'<!-- RECENT_ACTIVITY:START -->\n{activity_content}\n<!-- RECENT_ACTIVITY:END -->'
        
        updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
        
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_readme)
        
        print("✅ README.md updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        raise

def main():
    """Main function"""
    print(f"🚀 Generating README for {GITHUB_USERNAME}...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # Fetch recent activity
    print("📡 Fetching recent activity from GitHub...")
    activity = get_recent_activity()
    
    # Update README
    print("📝 Updating README.md...")
    update_readme(activity)
    
    print("✨ Done!")

if __name__ == '__main__':
    main()
