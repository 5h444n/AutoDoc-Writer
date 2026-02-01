from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.commit import CommitListResponse
from app.services.github_service import GitHubService

router = APIRouter()


@router.get("/", response_model=CommitListResponse)
def list_commits(
    repo_full_name: Optional[str] = None,
    per_page: int = 20,
    include_stats: bool = True,
    current_user: User = Depends(get_current_user),
):
    """
    Returns commits for a repository. If no repo is provided, returns recent
    commits across monitored repositories (or all repos if none are monitored).
    
    Query Parameters:
    - repo_full_name: Optional repository in format 'owner/repo' 
    - per_page: Number of commits per page (1-50, default 20)
    - include_stats: Include file change statistics (default true)
    """
    if not current_user.access_token:
        raise HTTPException(status_code=401, detail="Missing GitHub access token")

    per_page = max(1, min(per_page, 50))

    if repo_full_name:
        commits = GitHubService.get_repo_commits(
            current_user.access_token,
            repo_full_name,
            per_page=per_page,
            include_stats=include_stats,
        )
        return {"commits": commits}

    monitored_names = [repo.name for repo in current_user.repos if repo.is_active]
    repos = GitHubService.get_user_repos(current_user.access_token)
    if monitored_names:
        repos = [repo for repo in repos if repo.get("name") in monitored_names]

    combined = []
    per_repo = min(per_page, 5)
    max_repos = 5 if not monitored_names else 10
    for repo in repos[:max_repos]:
        if not repo.get("full_name"):
            continue
        combined.extend(
            GitHubService.get_repo_commits(
                current_user.access_token,
                repo["full_name"],
                per_page=per_repo,
                include_stats=include_stats,
            )
        )

    combined.sort(key=lambda item: item.get("timestamp") or "", reverse=True)
    return {"commits": combined[:per_page]}
