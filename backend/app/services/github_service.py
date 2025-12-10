from github import Github, Auth
from app.schemas.repo import RepoBase

class GitHubService:
    @staticmethod
    def get_user_repos(access_token: str):
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