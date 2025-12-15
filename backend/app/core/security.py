"""
Security utilities for encrypting sensitive data.
"""
from cryptography.fernet import Fernet
from app.core.config import settings
import base64
import hashlib


def get_encryption_key() -> bytes:
    """
    Derives a Fernet encryption key from the SECRET_KEY in settings.
    
    Returns:
        bytes: A URL-safe base64-encoded 32-byte key suitable for Fernet.
    """
    # Use SHA256 to derive a 32-byte key from the SECRET_KEY
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    # Fernet requires a URL-safe base64-encoded key
    return base64.urlsafe_b64encode(key)


def encrypt_token(token: str) -> str:
    """
    Encrypts a token using Fernet symmetric encryption.
    
    Args:
        token: The plaintext token to encrypt.
        
    Returns:
        str: The encrypted token as a string.
    """
    if not token:
        return token
    
    fernet = Fernet(get_encryption_key())
    encrypted = fernet.encrypt(token.encode())
    return encrypted.decode()


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypts a token that was encrypted with encrypt_token.
    
    Args:
        encrypted_token: The encrypted token string.
        
    Returns:
        str: The decrypted plaintext token.
    """
    if not encrypted_token:
        return encrypted_token
    
    fernet = Fernet(get_encryption_key())
    decrypted = fernet.decrypt(encrypted_token.encode())
    return decrypted.decode()
