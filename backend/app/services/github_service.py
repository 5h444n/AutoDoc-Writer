import requests
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from app.core.config import settings

class GitHubService:
    @staticmethod
    def get_login_redirect():
        """
        Generates the GitHub OAuth redirect URL.
        This was the missing function causing your error.
        """
        url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={settings.GITHUB_CLIENT_ID}"
            f"&redirect_uri={settings.REDIRECT_URI}"
            f"&scope=repo"
        )
        return RedirectResponse(url)

    @staticmethod
    def exchange_code_for_token(code: str) -> str:
        """Exchanges the temporary code for a permanent access token."""
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
        """Fetches the GitHub username using the access token."""
        url = "https://api.github.com/user"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user profile")
            
        return response.json().get("login")

    @staticmethod
    def get_user_repos(access_token: str):
        """Fetches all repositories for the logged-in user."""
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        params = {"sort": "updated", "per_page": 100}
        
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
        
        # Return a simplified list of dicts
        return [
            {
                "name": repo["name"],
                "url": repo["html_url"],
                "last_updated": repo["updated_at"]
            }
            for repo in all_repos
        ]