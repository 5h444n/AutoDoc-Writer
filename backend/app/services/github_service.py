import base64
import requests
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from app.core.config import settings

class GitHubService:
    REQUEST_TIMEOUT = (5, 20)

    @staticmethod
    def _request(method: str, url: str, **kwargs) -> requests.Response:
        try:
            return requests.request(method, url, timeout=GitHubService.REQUEST_TIMEOUT, **kwargs)
        except requests.Timeout:
            raise HTTPException(status_code=504, detail="GitHub API request timed out")
        except requests.RequestException as exc:
            raise HTTPException(status_code=502, detail=f"GitHub API request failed: {exc}")

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
        """
        url = (
            f"{settings.GITHUB_AUTH_URL}"
            f"?client_id={settings.GITHUB_CLIENT_ID}"
            f"&redirect_uri={settings.REDIRECT_URI}"
            f"&scope=repo"
        )
        return RedirectResponse(url)

    @staticmethod
    def exchange_code_for_token(code: str) -> str:
        """Exchanges the temporary code for a permanent access token."""
        url = settings.GITHUB_TOKEN_URL
        headers = {"Accept": "application/json"}
        data = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.REDIRECT_URI,
        }

        response = GitHubService._request("post", url, headers=headers, data=data)
        response_data = response.json()

        if "error" in response_data:
            raise HTTPException(status_code=400, detail=response_data.get("error_description"))

        return response_data.get("access_token")

    @staticmethod
    def get_user_profile(access_token: str) -> str:
        """Fetches the GitHub username using the access token."""
        url = "https://api.github.com/user"
        headers = GitHubService._headers(access_token)

        response = GitHubService._request("get", url, headers=headers)
        GitHubService._raise_for_status(response, "Failed to fetch user profile")

        return response.json().get("login")

    @staticmethod
    def get_user_details(access_token: str):
        """Fetches the GitHub user details using the access token."""
        url = "https://api.github.com/user"
        headers = GitHubService._headers(access_token)

        response = GitHubService._request("get", url, headers=headers)
        GitHubService._raise_for_status(response, "Failed to fetch user profile")
        data = response.json()

        return {
            "username": data.get("login"),
            "name": data.get("name") or data.get("login"),
            "avatar": data.get("avatar_url"),
            "email": data.get("email"),
        }

    @staticmethod
    def get_user_repos(access_token: str):
        """Fetches all repositories for the logged-in user."""
        url = "https://api.github.com/user/repos"
        headers = GitHubService._headers(access_token)

        per_page = 100
        params = {"sort": "updated", "per_page": per_page, "page": 1}

        all_repos = []
        while True:
            response = GitHubService._request("get", url, headers=headers, params=params)
            GitHubService._raise_for_status(response, "Failed to fetch repositories")
            repos = response.json()
            if not repos:
                break
            all_repos.extend(repos)
            if len(repos) < per_page:
                break
            params["page"] += 1

        return [
            {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "url": repo.get("html_url"),
                "description": repo.get("description") or "",
                "language": repo.get("language") or "Unknown",
                "stars": repo.get("stargazers_count", 0),
                "updated_at": repo.get("updated_at"),
                "pushed_at": repo.get("pushed_at"),
            }
            for repo in all_repos
        ]

    @staticmethod
    def get_repo_tree(access_token: str, repo_full_name: str, ref: str = "HEAD"):
        """Fetches the repository tree (optionally recursive)."""
        url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{ref}"
        headers = GitHubService._headers(access_token)
        params = {"recursive": "1"}
        response = GitHubService._request("get", url, headers=headers, params=params)
        GitHubService._raise_for_status(response, "Failed to fetch repository tree")
        return response.json().get("tree", [])

    @staticmethod
    def get_file_content(access_token: str, repo_full_name: str, path: str, ref: str = "HEAD"):
        """Fetches a file's content (base64 decoded) and sha via GitHub contents API."""
        url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}"
        headers = GitHubService._headers(access_token)
        params = {"ref": ref} if ref else None
        response = GitHubService._request("get", url, headers=headers, params=params)
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

    @staticmethod
    def get_repo_commit_count(access_token: str, repo_full_name: str) -> int:
        """Get total commit count for a repository."""
        url = f"https://api.github.com/repos/{repo_full_name}/commits"
        headers = GitHubService._headers(access_token)
        response = GitHubService._request("get", url, headers=headers, params={"per_page": 1})
        GitHubService._raise_for_status(response, "Failed to fetch commit count")

        link_header = response.headers.get("Link")
        if not link_header:
            return len(response.json())

        for part in link_header.split(","):
            if 'rel="last"' in part:
                url_part = part.split(";")[0].strip().strip("<>")
                if "page=" in url_part:
                    try:
                        page_str = url_part.split("page=")[-1].split("&")[0]
                        return int(page_str)
                    except ValueError:
                        return 0
        return 0

    @staticmethod
    def get_commit_detail(access_token: str, repo_full_name: str, sha: str, include_patch: bool = True):
        """Get detailed information for a specific commit."""
        url = f"https://api.github.com/repos/{repo_full_name}/commits/{sha}"
        headers = GitHubService._headers(access_token)
        response = GitHubService._request("get", url, headers=headers)
        GitHubService._raise_for_status(response, "Failed to fetch commit detail")

        data = response.json()
        if not include_patch:
            for file_info in data.get("files", []):
                file_info.pop("patch", None)
                file_info.pop("raw_url", None)
        return data

    @staticmethod
    def get_repo_commits(access_token: str, repo_full_name: str, per_page: int = 20, include_stats: bool = True):
        """Fetch commits from a repository with optional stats."""
        url = f"https://api.github.com/repos/{repo_full_name}/commits"
        headers = GitHubService._headers(access_token)
        params = {"per_page": per_page}
        response = GitHubService._request("get", url, headers=headers, params=params)
        GitHubService._raise_for_status(response, "Failed to fetch commits")

        commits = response.json()
        results = []
        for item in commits:
            sha = item.get("sha")
            commit_info = item.get("commit") or {}
            author_info = commit_info.get("author") or {}
            user_info = item.get("author") or {}
            author_name = author_info.get("name") or user_info.get("login") or "Unknown"

            entry = {
                "id": sha,
                "sha": sha[:7] if sha else "",
                "full_sha": sha,
                "message": commit_info.get("message") or "",
                "author": author_name,
                "author_avatar": user_info.get("avatar_url"),
                "timestamp": author_info.get("date"),
                "repo_full_name": repo_full_name,
                "repo_name": repo_full_name.split("/")[-1] if repo_full_name else "",
            }

            if include_stats and sha:
                detail = GitHubService.get_commit_detail(
                    access_token, repo_full_name, sha, include_patch=False
                )
                stats = detail.get("stats", {})
                files = detail.get("files", []) or []
                entry.update({
                    "files_changed": len(files),
                    "additions": stats.get("additions", 0),
                    "deletions": stats.get("deletions", 0),
                    "files": [
                        {
                            "filename": f.get("filename"),
                            "additions": f.get("additions", 0),
                            "deletions": f.get("deletions", 0),
                        }
                        for f in files
                    ],
                })

            results.append(entry)

        return results

