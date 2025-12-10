from fastapi import APIRouter, HTTPException
from github import Github, Auth

router = APIRouter()

@router.get("/get-repos")
def get_repos(access_token: str):
    """
    Returns a list of GitHub repositories for the authenticated user.
    """
    try:
        auth = Auth.Token(access_token)
        gh = Github(auth=auth)
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
        # Handle exceptions gracefully - avoid JSON serialization errors
        error_msg = getattr(e, 'message', str(e))
        raise HTTPException(status_code=400, detail=f"GitHub API error: {error_msg}")
