import requests
import httpx
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session  # Added this import
from app.core.config import settings
from app.models.user import User

class GitHubService:
    def __init__(self, db: Session):
        """
        FIX 1: Added __init__ to accept the database session.
        This stops the 'TypeError: GitHubService() takes no arguments' crash.
        """
        self.db = db

    # --- Helper Method (FIX 2: This was missing but called in get_commits) ---
    def _get_headers(self, token: str):
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    # --- Existing Static Methods (Kept exactly as you had them) ---
    @staticmethod
    def get_login_redirect():
        url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={settings.GITHUB_CLIENT_ID}"
            f"&redirect_uri={settings.REDIRECT_URI}"
            f"&scope=repo"
        )
        return RedirectResponse(url)

    @staticmethod
    def exchange_code_for_token(code: str) -> str:
        url = "https://github.com/login/oauth/access_token"
        headers = {"Accept": "application/json"}
        data = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.REDIRECT_URI
        }
        
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        
        if "error" in response_data:
            raise HTTPException(status_code=400, detail=response_data["error_description"])
            
        return response_data.get("access_token")

    @staticmethod
    def get_user_profile(access_token: str) -> str:
        url = "https://api.github.com/user"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            try:
                error_detail = response.json().get("message", response.text)
            except Exception:
                error_detail = response.text
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch user profile: HTTP {response.status_code} - {error_detail}"
            )
            
        return response.json().get("login")

    @staticmethod
    def get_user_repos(access_token: str):
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        per_page = 100
        params = {"sort": "updated", "per_page": per_page, "page": 1}
        
        all_repos = []
        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to fetch repositories")
            repos = response.json()
            if not repos:
                break
            all_repos.extend(repos)
            if len(repos) < per_page:
                break
            params["page"] += 1
        
        return [
            {
                "name": repo["name"],
                "url": repo["html_url"],
                "last_updated": repo["updated_at"]
            }
            for repo in all_repos
        ]
    
    # --- Async Method (Updated to be more robust) ---
    async def get_commits(self, user: User, repo_name: str, limit: int = 5):
        """
        Fetches the last few commits for a specific repository.
        """
        # Robustly get the token (handles different naming conventions)
        token = getattr(user, "github_access_token", None) or getattr(user, "access_token", None)
        if not token:
             # Fallback: if no token on user, try to see if it was passed in differently or raise error
             print("Error: User has no GitHub token")
             return []

        # Robustly get the username
        owner = getattr(user, "github_username", None) or getattr(user, "username", None)
        if not owner:
            print("Error: User has no username")
            return []

        async with httpx.AsyncClient() as client:
            url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
            
            response = await client.get(
                url, 
                headers=self._get_headers(token),
                params={"per_page": limit}
            )
            
            if response.status_code != 200:
                print(f"Error fetching commits from {url}: {response.text}")
                return []
                
            data = response.json()
            
            clean_commits = []
            for item in data:
                clean_commits.append({
                    "sha": item.get("sha"),
                    "message": item.get("commit", {}).get("message"),
                    "author_name": item.get("commit", {}).get("author", {}).get("name"),
                    "date": item.get("commit", {}).get("author", {}).get("date"),
                    "url": item.get("html_url")
                })
            
            return clean_commits