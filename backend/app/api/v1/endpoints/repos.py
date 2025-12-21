from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.repository import Repository
from app.models.user import User
from app.schemas.repo import RepoResponse, RepoToggleRequest
from app.core.security import get_current_user

router = APIRouter()

# 1. GET Repos (Reads from Database instead of GitHub API)
@router.get("/", response_model=RepoResponse)
def read_repos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetches repositories from the local database for the authenticated user.
    Requires authentication via Bearer token.
    """
    # Return the repos (Pydantic will auto-map 'is_active' from the DB)
    return {"total_repos": len(current_user.repos), "repos": current_user.repos}

# 2. PATCH Toggle (The new Sprint 2 Feature)
@router.patch("/{repo_name}/toggle")
def toggle_repo_monitoring(
    repo_name: str, 
    toggle: RepoToggleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enables or Disables monitoring for a specific repository.
    Requires authentication via Bearer token.
    Users can only toggle their own repositories.
    """
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