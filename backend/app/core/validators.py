"""Input validation utilities for AutoDoc Writer.

This module provides comprehensive input validation to prevent:
- SQL Injection
- XSS attacks
- Path traversal
- Command injection
- Invalid/malicious input
"""

import re
from typing import Optional
from fastapi import HTTPException


class InputValidator:
    """Validates and sanitizes user inputs."""
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|SCRIPT)\b)",
        r"(--|;|\/\*|\*\/|xp_|sp_)",
        r"('|(\\')|(\")|(\\\")|(;)|(--)|(\#))",
    ]
    
    # XSS patterns
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"onerror\s*=",
        r"onload\s*=",
        r"<iframe",
        r"<object",
        r"<embed",
    ]
    
    # Path traversal patterns
    PATH_TRAVERSAL_PATTERNS = [
        r"\.\./",
        r"\.\.",
        r"~\/",
        r"%2e%2e",
        r"\.\.\\",
    ]
    
    # Command injection patterns
    COMMAND_INJECTION_PATTERNS = [
        r"`",
        r"\$\(",
        r"\|\s*\w+",
        r";\s*\w+",
        r"&&\s*\w+",
    ]
    
    @staticmethod
    def validate_github_token(token: str) -> str:
        """Validate GitHub access token format.
        
        Args:
            token: GitHub access token
            
        Returns:
            Sanitized token
            
        Raises:
            HTTPException: If token is invalid
        """
        if not token or not isinstance(token, str):
            raise HTTPException(status_code=401, detail="Invalid access token")
        
        # Remove whitespace
        token = token.strip()
        
        # GitHub tokens should be alphanumeric with underscores
        if not re.match(r"^[a-zA-Z0-9_\-]+$", token):
            raise HTTPException(
                status_code=401, 
                detail="Access token contains invalid characters"
            )
        
        # GitHub tokens have minimum length
        if len(token) < 20:
            raise HTTPException(status_code=401, detail="Access token too short")
        
        return token
    
    @staticmethod
    def validate_repository_name(repo_name: str) -> str:
        """Validate GitHub repository name.
        
        Args:
            repo_name: Repository name (e.g., "owner/repo")
            
        Returns:
            Sanitized repository name
            
        Raises:
            HTTPException: If repository name is invalid
        """
        if not repo_name or not isinstance(repo_name, str):
            raise HTTPException(status_code=400, detail="Invalid repository name")
        
        repo_name = repo_name.strip()
        
        # GitHub repo format: owner/repo or just repo
        # Allow alphanumeric, hyphens, underscores, dots, and one slash
        if not re.match(r"^[a-zA-Z0-9\-_.]+(/[a-zA-Z0-9\-_.]+)?$", repo_name):
            raise HTTPException(
                status_code=400,
                detail="Repository name contains invalid characters"
            )
        
        if len(repo_name) > 200:
            raise HTTPException(status_code=400, detail="Repository name too long")
        
        return repo_name
    
    @staticmethod
    def validate_file_path(file_path: str) -> str:
        """Validate file path to prevent path traversal attacks.
        
        Args:
            file_path: File path within repository
            
        Returns:
            Sanitized file path
            
        Raises:
            HTTPException: If path is invalid or contains traversal attempts
        """
        if not file_path or not isinstance(file_path, str):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        file_path = file_path.strip()
        
        # Check for path traversal attempts
        for pattern in InputValidator.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, file_path, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Path traversal attempt detected"
                )
        
        # Ensure path doesn't start with /
        if file_path.startswith("/"):
            file_path = file_path[1:]
        
        # Validate characters
        if not re.match(r"^[a-zA-Z0-9\-_./]+$", file_path):
            raise HTTPException(
                status_code=400,
                detail="File path contains invalid characters"
            )
        
        if len(file_path) > 500:
            raise HTTPException(status_code=400, detail="File path too long")
        
        return file_path
    
    @staticmethod
    def validate_documentation_style(style: str) -> str:
        """Validate documentation style parameter.
        
        Args:
            style: Documentation style (plain, research, latex)
            
        Returns:
            Sanitized style string
            
        Raises:
            HTTPException: If style is invalid
        """
        if not style or not isinstance(style, str):
            raise HTTPException(status_code=400, detail="Invalid documentation style")
        
        style = style.strip().lower()
        
        valid_styles = ["plain", "research", "latex"]
        if style not in valid_styles:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid style. Must be one of: {', '.join(valid_styles)}"
            )
        
        return style
    
    @staticmethod
    def sanitize_text_input(text: str, max_length: int = 10000) -> str:
        """Sanitize general text input.
        
        Args:
            text: User input text
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
            
        Raises:
            HTTPException: If text contains malicious patterns
        """
        if not text or not isinstance(text, str):
            raise HTTPException(status_code=400, detail="Invalid text input")
        
        # Check length
        if len(text) > max_length:
            raise HTTPException(
                status_code=400,
                detail=f"Text exceeds maximum length of {max_length}"
            )
        
        # Check for SQL injection
        for pattern in InputValidator.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Potentially malicious SQL patterns detected"
                )
        
        # Check for XSS
        for pattern in InputValidator.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Potentially malicious script patterns detected"
                )
        
        # Check for command injection
        for pattern in InputValidator.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, text):
                raise HTTPException(
                    status_code=400,
                    detail="Potentially malicious command patterns detected"
                )
        
        return text.strip()
    
    @staticmethod
    def validate_authorization_header(authorization: Optional[str]) -> str:
        """Validate and extract token from Authorization header.
        
        Args:
            authorization: Authorization header value
            
        Returns:
            Extracted access token
            
        Raises:
            HTTPException: If authorization header is invalid
        """
        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="Missing Authorization header"
            )
        
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization format. Expected: Bearer <token>"
            )
        
        token = authorization.replace("Bearer ", "", 1).strip()
        
        return InputValidator.validate_github_token(token)
