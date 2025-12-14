from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.repository import Repository
from app.models.user import User
from app.schemas.repo import RepoResponse, RepoToggleRequest

router = APIRouter()

# 1. GET Repos (Reads from Database instead of GitHub API)
@router.get("/", response_model=RepoResponse)
def read_repos(username: str, db: Session = Depends(get_db)):
    """
    Fetches repositories from the local database.
    Requires 'username' because we stored data under the user's account.
    """
    # Find the user by their GitHub username
    user = db.query(User).filter(User.github_username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return the repos (Pydantic will auto-map 'is_active' from the DB)
    return {"total_repos": len(user.repos), "repos": user.repos}

# 2. PATCH Toggle (The new Sprint 2 Feature)
@router.patch("/{repo_name}/toggle")
def toggle_repo_monitoring(
    repo_name: str, 
    username: str, 
    toggle: RepoToggleRequest, 
    db: Session = Depends(get_db)
):
    """
    Enables or Disables monitoring for a specific repository.
    """
    user = db.query(User).filter(User.github_username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Find the specific repo belonging to this user
    repo = db.query(Repository).filter(
        Repository.name == repo_name,
        Repository.owner_id == user.id
    ).first()

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Update the status
    repo.is_active = toggle.is_active
    db.commit()
    db.refresh(repo)
    
    return {"status": "success", "repo": repo.name, "is_active": repo.is_active}