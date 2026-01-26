"""Logging configuration for AutoDoc Writer.

This module provides centralized logging configuration with:
- Console output for development
- File output for production
- Structured log formatting
- Rotating file handlers
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from app.core.config import settings


# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance.
    
    Args:
        name: Logger name (usually __name__ of the calling module)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set log level based on environment
    if settings.ENV == "production":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.ENV != "production" else logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation (always enabled)
    log_file = LOGS_DIR / f'autodoc_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error file handler (errors only)
    error_log_file = LOGS_DIR / f'errors_{datetime.now().strftime("%Y%m%d")}.log'
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10_000_000,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    return logger


def log_request(logger: logging.Logger, method: str, endpoint: str, user_id: int = None):
    """Log an API request.
    
    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        user_id: Optional user ID
    """
    user_info = f"user_id={user_id}" if user_id else "anonymous"
    logger.info(f"{method} {endpoint} - {user_info}")


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log an error with context.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context about where/why the error occurred
    """
    error_msg = f"{context}: {type(error).__name__}: {str(error)}" if context else f"{type(error).__name__}: {str(error)}"
    logger.error(error_msg, exc_info=True)


def log_security_event(logger: logging.Logger, event: str, details: dict = None):
    """Log a security-related event.
    
    Args:
        logger: Logger instance
        event: Description of security event
        details: Additional details about the event
    """
    details_str = f" - {details}" if details else ""
    logger.warning(f"SECURITY: {event}{details_str}")
