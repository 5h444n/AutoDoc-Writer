"""
Unit tests for security utilities.

Tests encryption and decryption of sensitive data.
"""
import pytest
from app.core.security import encrypt_token, decrypt_token


class TestTokenEncryption:
    """Test token encryption functionality."""

    def test_encrypt_token_produces_different_output(self):
        """Test that encryption produces output different from input."""
        # Arrange
        token = "ghp_test123456789"
        
        # Act
        encrypted = encrypt_token(token)
        
        # Assert
        assert encrypted != token
        assert len(encrypted) > 0

    def test_decrypt_token_reverses_encryption(self):
        """Test that decryption reverses encryption."""
        # Arrange
        token = "ghp_test123456789"
        encrypted = encrypt_token(token)
        
        # Act
        decrypted = decrypt_token(encrypted)
        
        # Assert
        assert decrypted == token

    def test_encrypt_decrypt_roundtrip(self):
        """Test full encryption/decryption roundtrip."""
        # Arrange
        test_tokens = [
            "ghp_short",
            "ghp_verylongtoken1234567890abcdefghijklmnopqrstuvwxyz",
            "gho_tokenwithnumbers123456",
            "test_special!@#$%chars",
        ]
        
        # Act & Assert
        for token in test_tokens:
            encrypted = encrypt_token(token)
            decrypted = decrypt_token(encrypted)
            assert decrypted == token, f"Roundtrip failed for token: {token}"

    def test_encrypt_empty_string(self):
        """Test encryption of empty string."""
        # Act
        encrypted = encrypt_token("")
        
        # Assert
        assert encrypted == ""

    def test_decrypt_empty_string(self):
        """Test decryption of empty string."""
        # Act
        decrypted = decrypt_token("")
        
        # Assert
        assert decrypted == ""

    def test_encrypt_none_returns_none(self):
        """Test encryption of None returns None."""
        # Act
        encrypted = encrypt_token(None)
        
        # Assert
        assert encrypted is None

    def test_decrypt_none_returns_none(self):
        """Test decryption of None returns None."""
        # Act
        decrypted = decrypt_token(None)
        
        # Assert
        assert decrypted is None

    def test_encrypted_tokens_are_different_each_time(self):
        """Test that encrypting the same token twice produces different ciphertexts."""
        # Arrange
        token = "ghp_test123456789"
        
        # Act
        encrypted1 = encrypt_token(token)
        encrypted2 = encrypt_token(token)
        
        # Assert
        # Due to Fernet's timestamp-based encryption, each encryption should be unique
        assert encrypted1 != encrypted2
        
        # But both should decrypt to the same value
        assert decrypt_token(encrypted1) == token
        assert decrypt_token(encrypted2) == token

    def test_encrypted_token_cannot_be_decrypted_as_plain_text(self):
        """Test that encrypted tokens don't contain plain text."""
        # Arrange
        token = "ghp_secrettoken123"
        
        # Act
        encrypted = encrypt_token(token)
        
        # Assert
        # Encrypted token should not contain the original token
        assert token not in encrypted
        assert "ghp_" not in encrypted

    def test_decrypt_invalid_token_raises_error(self):
        """Test that decrypting an invalid token raises an error."""
        # Arrange
        invalid_token = "this_is_not_an_encrypted_token"
        
        # Act & Assert
        with pytest.raises(Exception):
            decrypt_token(invalid_token)

    def test_encryption_is_deterministic_with_same_key(self):
        """Test that encryption uses consistent key from settings."""
        # Arrange
        token = "ghp_test123"
        
        # Act
        encrypted1 = encrypt_token(token)
        decrypted1 = decrypt_token(encrypted1)
        
        encrypted2 = encrypt_token(token)
        decrypted2 = decrypt_token(encrypted2)
        
        # Assert - both should decrypt correctly even if ciphertext differs
        assert decrypted1 == token
        assert decrypted2 == token
