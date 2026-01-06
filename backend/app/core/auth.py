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


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> "User":
    """
    Validates the access token and returns the authenticated user.
    
    Args:
        credentials: Bearer token from Authorization header
        db: Database session
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Import here to avoid circular dependency with app.models.user
    from app.models.user import User
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # ---------------------------------------------------------
    # FIX: Search in Python instead of SQL
    # (Because the DB cannot decrypt the data to compare it)
    # ---------------------------------------------------------
    users = db.query(User).all()
    
    user = None
    for u in users:
        # u.access_token automatically decrypts the key for us here
        if u.access_token == token:
            user = u
            break
    # ---------------------------------------------------------
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user