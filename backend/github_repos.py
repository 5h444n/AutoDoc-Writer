from fastapi import APIRouter, HTTPException
from github import Github

router = APIRouter()

@router.get("/get-repos")
def get_repos(access_token: str):
    """
    Returns a list of GitHub repositories for the authenticated user.
    """
    try:
        gh = Github(access_token)
        user = gh.get_user()
        repos = user.get_repos()

        repo_list = []

        for repo in repos:
            repo_list.append({
                "name": repo.name,
                "url": repo.html_url,
                "last_updated": repo.updated_at.isoformat()
            })

        return {
            "total_repos": len(repo_list),
            "repos": repo_list
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
