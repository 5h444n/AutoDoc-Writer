"""
Unit tests for User model.

Tests user model functionality including token encryption.
"""
import pytest
from app.models.user import User
from app.models.repository import Repository


class TestUserModel:
    """Test User model functionality."""

    def test_user_creation(self):
        """Test creating a user instance."""
        # Act
        user = User()
        user.github_username = "testuser"
        
        # Assert
        assert user.github_username == "testuser"
        assert user.access_token is None

    def test_access_token_encryption(self):
        """Test that access tokens are encrypted at rest."""
        # Arrange
        user = User()
        user.github_username = "testuser"
        token = "ghp_test123456789"
        
        # Act
        user.access_token = token
        
        # Assert
        # The stored value should be encrypted (different from input)
        assert user._access_token != token
        # But the property should return the decrypted value
        assert user.access_token == token

    def test_access_token_setter_and_getter(self):
        """Test access token setter and getter work correctly."""
        # Arrange
        user = User()
        token = "ghp_secrettoken"
        
        # Act
        user.access_token = token
        retrieved_token = user.access_token
        
        # Assert
        assert retrieved_token == token

    def test_access_token_none_handling(self):
        """Test that None tokens are handled correctly."""
        # Arrange
        user = User()
        
        # Act
        user.access_token = None
        
        # Assert
        assert user._access_token is None
        assert user.access_token is None

    def test_access_token_empty_string_handling(self):
        """Test that empty string tokens are treated as None."""
        # Arrange
        user = User()
        
        # Act
        user.access_token = ""
        
        # Assert
        # Empty strings are treated as None (no token)
        assert user._access_token is None
        assert user.access_token is None

    def test_access_token_update(self):
        """Test updating an access token."""
        # Arrange
        user = User()
        old_token = "ghp_oldtoken"
        new_token = "ghp_newtoken"
        
        # Act
        user.access_token = old_token
        old_encrypted = user._access_token
        
        user.access_token = new_token
        new_encrypted = user._access_token
        
        # Assert
        assert user.access_token == new_token
        assert old_encrypted != new_encrypted
        assert user._access_token != new_token

    def test_multiple_users_different_tokens(self):
        """Test that multiple users can have different tokens."""
        # Arrange
        user1 = User()
        user1.github_username = "user1"
        user1.access_token = "ghp_token1"
        
        user2 = User()
        user2.github_username = "user2"
        user2.access_token = "ghp_token2"
        
        # Assert
        assert user1.access_token == "ghp_token1"
        assert user2.access_token == "ghp_token2"
        assert user1._access_token != user2._access_token

    def test_access_token_not_leaked_in_plain_text(self):
        """Test that tokens are not stored in plain text."""
        # Arrange
        user = User()
        sensitive_token = "ghp_supersecret12345"
        
        # Act
        user.access_token = sensitive_token
        
        # Assert
        # The encrypted value should not contain the sensitive token
        assert sensitive_token not in user._access_token
        assert "ghp_" not in user._access_token


class TestUserModelAttributes:
    """Test User model attributes."""

    def test_user_has_required_attributes(self):
        """Test that User model has all required attributes."""
        # Arrange & Act
        user = User()
        
        # Assert
        assert hasattr(user, 'id')
        assert hasattr(user, 'github_username')
        assert hasattr(user, 'access_token')
        assert hasattr(user, '_access_token')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'repos')

    def test_user_table_name(self):
        """Test that User model has correct table name."""
        # Assert
        assert User.__tablename__ == "users"
