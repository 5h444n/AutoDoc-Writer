import base64
import requests
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from app.core.config import settings

class GitHubService:
    @staticmethod
    def _headers(access_token: str):
        return {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        }

    @staticmethod
    def _raise_for_status(response: requests.Response, context: str) -> None:
        if response.status_code < 400:
            return
        try:
            detail = response.json().get("message", response.text)
        except Exception:
            detail = response.text
        raise HTTPException(
            status_code=400,
            detail=f"{context}: HTTP {response.status_code} - {detail}"
        )

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
        """Fetches all repositories for the logged-in user."""
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
        
        # Return a simplified list of dicts
        return [
            {
                "name": repo["name"],
                "url": repo["html_url"],
                "last_updated": repo["updated_at"]
            }
            for repo in all_repos
        ]

    @staticmethod
    def get_repo_tree(access_token: str, repo_full_name: str, ref: str = "HEAD"):
        """Fetches the repository tree (optionally recursive)."""
        url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{ref}"
        headers = GitHubService._headers(access_token)
        params = {"recursive": "1"}
        response = requests.get(url, headers=headers, params=params)
        GitHubService._raise_for_status(response, "Failed to fetch repository tree")
        return response.json().get("tree", [])

    @staticmethod
    def get_file_content(access_token: str, repo_full_name: str, path: str, ref: str = "HEAD"):
        """Fetches a file's content (base64 decoded) and sha via GitHub contents API."""
        url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}"
        headers = GitHubService._headers(access_token)
        params = {"ref": ref} if ref else None
        response = requests.get(url, headers=headers, params=params)
        GitHubService._raise_for_status(response, "Failed to fetch file content")
        data = response.json()
        if isinstance(data, list):
            return None, None
        content = data.get("content")
        encoding = data.get("encoding")
        sha = data.get("sha")
        if not content:
            return None, sha
        if encoding == "base64":
            try:
                decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
            except Exception:
                return None, sha
            return decoded, sha
        return str(content), sha
