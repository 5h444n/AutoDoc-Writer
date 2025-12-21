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
    # TODO: Refactor architecture to eliminate this circular dependency
    from app.models.user import User
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # Find user by access token
    user = db.query(User).filter(User.access_token == token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
