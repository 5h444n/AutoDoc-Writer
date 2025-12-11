from github import Github, Auth
from github.GithubException import GithubException
import requests
from app.schemas.repo import RepoBase

class GitHubService:
    @staticmethod
    def get_user_repos(access_token: str):
        try:
            auth = Auth.Token(access_token)
            gh = Github(auth=auth)
            user = gh.get_user()
            repos = user.get_repos()

            return [
                RepoBase(
                    name=repo.name,
                    url=repo.html_url,
                    last_updated=repo.updated_at.isoformat()
                ) for repo in repos
            ]
        except GithubException as ge:
            # Handle GitHub API errors (authentication, rate limiting, etc.)
            # Optionally log the error here
            raise RuntimeError(f"GitHub API error: {ge.data.get('message', str(ge)) if hasattr(ge, 'data') else str(ge)}")
        except requests.exceptions.RequestException as re:
            # Handle network errors
            # Optionally log the error here
            raise RuntimeError(f"Network error when accessing GitHub API: {str(re)}")
        except Exception as e:
            # Handle any other unforeseen errors
            # Optionally log the error here
            raise RuntimeError(f"Unexpected error when accessing GitHub API: {str(e)}")