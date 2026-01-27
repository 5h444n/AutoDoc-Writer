"""
Authentication utilities for user verification.
"""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import TYPE_CHECKING
from app.db.session import get_db

if TYPE_CHECKING:
    from app.models.user import User

# Security scheme for Bearer token authentication
security = HTTPBearer(auto_error=False)


import httpx

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> "User":
    """
    Validates the GitHub access token by calling the GitHub API.
    Then retrieves the user from the local database.
    """
    # Import here to avoid circular dependency
    from app.models.user import User

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    # print(f"DEBUG AUTH: Received token: '{token}'", flush=True)

    # 1. Validate Token with GitHub API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user", 
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
        )
        
        if response.status_code != 200:
            print(f"DEBUG AUTH: GitHub rejected token. Status: {response.status_code}, Body: {response.text}", flush=True)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid GitHub Token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        gh_user_data = response.json()
        gh_username = gh_user_data.get("login")

    # 2. Retrieve User from DB
    user = db.query(User).filter(User.github_username == gh_username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in local database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update token in DB if it changed (optional but good practice)
    # user.access_token = token
    # db.commit()
    
    return user
