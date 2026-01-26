from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db.session import get_db
from app.models.repository import Repository
from app.models.user import User
from app.schemas.repo import RepoResponse, RepoToggleRequest
from app.core.auth import get_current_user
from app.services.github_service import GitHubService
from app.core.validators import InputValidator

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# 1. GET Repos (Reads from Database instead of GitHub API)
@router.get("/", response_model=RepoResponse)
@limiter.limit("30/minute")
def read_repos(
    request: Request,
    include_commit_count: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetches repositories from GitHub and merges monitoring status from the database.
    Requires authentication via Bearer token.
    Rate limit: 30 requests per minute.
    """
    repo_status = {repo.name: repo.is_active for repo in current_user.repos}
    repos = GitHubService.get_user_repos(current_user.access_token)

    merged = []
    for repo in repos:
        if repo.get("name") not in repo_status:
            new_repo = Repository(
                name=repo.get("name"),
                url=repo.get("url"),
                last_updated=repo.get("updated_at"),
                owner_id=current_user.id,
            )
            db.add(new_repo)
            repo_status[repo.get("name")] = False

        commit_count = None
        if include_commit_count and repo.get("full_name"):
            commit_count = GitHubService.get_repo_commit_count(
                current_user.access_token, repo["full_name"]
            )

        merged.append({
            "id": repo.get("id"),
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "url": repo.get("url"),
            "description": repo.get("description", ""),
            "language": repo.get("language"),
            "stars": repo.get("stars", 0),
            "last_updated": repo.get("updated_at"),
            "is_active": repo_status.get(repo.get("name"), False),
            "commits": commit_count,
        })

    db.commit()

    return {"total_repos": len(merged), "repos": merged}

# 2. PATCH Toggle (The new Sprint 2 Feature)
@router.patch("/{repo_name}/toggle")
@limiter.limit("60/minute")
def toggle_repo_monitoring(
    request: Request,
    repo_name: str, 
    toggle: RepoToggleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enables or Disables monitoring for a specific repository.
    Requires authentication via Bearer token.
    Users can only toggle their own repositories.
    Rate limit: 60 requests per minute.
    """
    # Validate repository name to prevent injection attacks
    repo_name = InputValidator.validate_repository_name(repo_name)
    
    # Find the specific repo belonging to the authenticated user
    repo = db.query(Repository).filter(
        Repository.name == repo_name,
        Repository.owner_id == current_user.id
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Update the status
    repo.is_active = toggle.is_active
    db.commit()
    db.refresh(repo)
    
    return {"status": "success", "repo": repo.name, "is_active": repo.is_active}
