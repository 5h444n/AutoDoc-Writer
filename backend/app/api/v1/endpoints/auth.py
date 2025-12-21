from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.github_service import GitHubService
from app.db.session import get_db
from app.models.user import User
from app.models.repository import Repository

router = APIRouter()

@router.get("/login")
def login():
    """
    Redirects the user to GitHub's OAuth login page.
    """
    return GitHubService.get_login_redirect()

@router.get("/callback")
def callback(code: str, db: Session = Depends(get_db)):
    """
    Processes the GitHub callback:
    1. Exchanges code for token.
    2. Fetches user profile & repos.
    3. Saves User and Repositories to the database.
    """
    # 1. Exchange code for access token
    try:
        token = GitHubService.exchange_code_for_token(code)
    except Exception as e:
         raise HTTPException(status_code=400, detail=f"Token Exchange Failed: {str(e)}")
    
    # 2. Get GitHub Username
    gh_username = GitHubService.get_user_profile(token)
    
    if not gh_username:
        raise HTTPException(status_code=400, detail="Could not fetch GitHub profile")

    # 3. Find or Create User in Database
    user = db.query(User).filter(User.github_username == gh_username).first()
    if not user:
        user = User(github_username=gh_username, access_token=token)
        db.add(user)
    else:
        # Update the access token for existing users
        user.access_token = token
    
    db.commit()
    db.refresh(user)

    # 4. Fetch Repos from GitHub
    repos = GitHubService.get_user_repos(token)

    # 5. Sync Repos to Database (Using correct ["key"] syntax)
    for repo_data in repos:
        # Check if repo already exists
        existing_repo = db.query(Repository).filter(
            Repository.name == repo_data["name"],  # Fixed: uses ["name"]
            Repository.owner_id == user.id
        ).first()

        if not existing_repo:
            new_repo = Repository(
                name=repo_data["name"],       # Fixed
                url=repo_data["url"], 
                last_updated=repo_data["last_updated"],  # <--- ADD THIS LINE        # Fixed
                owner_id=user.id
            )
            db.add(new_repo)
    
    db.commit()

    return {
        "message": "Login successful",
        "username": user.github_username,
        "repos_synced": len(repos)
    }