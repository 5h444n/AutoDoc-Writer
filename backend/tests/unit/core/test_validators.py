"""Tests for input validation utilities."""

import pytest
from fastapi import HTTPException
from app.core.validators import InputValidator


class TestInputValidator:
    """Test suite for InputValidator class."""
    
    def test_validate_github_token_valid(self):
        """Test validation of valid GitHub token."""
        token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
        result = InputValidator.validate_github_token(token)
        assert result == token
    
    def test_validate_github_token_too_short(self):
        """Test rejection of short token."""
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.validate_github_token("short")
        assert exc_info.value.status_code == 401
    
    def test_validate_github_token_invalid_chars(self):
        """Test rejection of token with invalid characters."""
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.validate_github_token("token;DROP TABLE users;--")
        assert exc_info.value.status_code == 401
    
    def test_validate_repository_name_valid(self):
        """Test validation of valid repository name."""
        valid_names = [
            "myrepo",
            "owner/repo",
            "my-repo",
            "my_repo",
            "my.repo"
        ]
        for name in valid_names:
            result = InputValidator.validate_repository_name(name)
            assert result == name
    
    def test_validate_repository_name_invalid(self):
        """Test rejection of invalid repository names."""
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.validate_repository_name("repo; DROP TABLE")
        assert exc_info.value.status_code == 400
    
    def test_validate_file_path_valid(self):
        """Test validation of valid file paths."""
        valid_paths = [
            "src/main.py",
            "docs/README.md",
            "app/core/config.py"
        ]
        for path in valid_paths:
            result = InputValidator.validate_file_path(path)
            assert result == path
    
    def test_validate_file_path_traversal(self):
        """Test rejection of path traversal attempts."""
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32",
            "%2e%2e/secret"
        ]
        for path in malicious_paths:
            with pytest.raises(HTTPException) as exc_info:
                InputValidator.validate_file_path(path)
            assert exc_info.value.status_code == 400
    
    def test_validate_documentation_style_valid(self):
        """Test validation of valid documentation styles."""
        valid_styles = ["plain", "research", "latex"]
        for style in valid_styles:
            result = InputValidator.validate_documentation_style(style)
            assert result == style
    
    def test_validate_documentation_style_invalid(self):
        """Test rejection of invalid documentation style."""
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.validate_documentation_style("invalid_style")
        assert exc_info.value.status_code == 400
    
    def test_sanitize_text_input_valid(self):
        """Test sanitization of valid text input."""
        text = "This is a normal text input"
        result = InputValidator.sanitize_text_input(text)
        assert result == text
    
    def test_sanitize_text_sql_injection(self):
        """Test detection of SQL injection attempts."""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin' --",
            "1; DELETE FROM users"
        ]
        for text in malicious_inputs:
            with pytest.raises(HTTPException) as exc_info:
                InputValidator.sanitize_text_input(text)
            assert exc_info.value.status_code == 400
    
    def test_sanitize_text_xss(self):
        """Test detection of XSS attempts."""
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert(1)",
            "<iframe src='evil.com'></iframe>",
            "<img onerror='alert(1)'>"
        ]
        for text in malicious_inputs:
            with pytest.raises(HTTPException) as exc_info:
                InputValidator.sanitize_text_input(text)
            assert exc_info.value.status_code == 400
    
    def test_sanitize_text_command_injection(self):
        """Test detection of command injection attempts."""
        malicious_inputs = [
            "`rm -rf /`",
            "$(whoami)",
            "; cat /etc/passwd",
            "&& curl evil.com"
        ]
        for text in malicious_inputs:
            with pytest.raises(HTTPException) as exc_info:
                InputValidator.sanitize_text_input(text)
            assert exc_info.value.status_code == 400
    
    def test_sanitize_text_max_length(self):
        """Test text length validation."""
        long_text = "a" * 10001
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.sanitize_text_input(long_text)
        assert exc_info.value.status_code == 400
    
    def test_validate_authorization_header_valid(self):
        """Test validation of valid Authorization header."""
        header = "Bearer ghp_1234567890abcdefghijklmnopqrstuvwxyz"
        result = InputValidator.validate_authorization_header(header)
        assert result == "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
    
    def test_validate_authorization_header_missing(self):
        """Test rejection of missing Authorization header."""
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.validate_authorization_header(None)
        assert exc_info.value.status_code == 401
    
    def test_validate_authorization_header_wrong_format(self):
        """Test rejection of wrong Authorization header format."""
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.validate_authorization_header("Basic abc123")
        assert exc_info.value.status_code == 401
