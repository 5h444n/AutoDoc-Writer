from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from typing import Optional
import hashlib
from app.db.base import Base
from app.core.security import encrypt_token, decrypt_token


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    github_username = Column(String, unique=True, index=True)
    _access_token = Column("access_token", String)
    token_hash = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- ADD THIS LINE --- TANIM
    repos = relationship("Repository", back_populates="owner")

    @hybrid_property
    def access_token(self) -> Optional[str]:
        """Decrypts and returns the access token."""
        if self._access_token:
            return decrypt_token(self._access_token)
        return None

    @access_token.expression
    def access_token(cls):
        """For SQLAlchemy queries, use the encrypted column directly."""
        return cls._access_token

    @access_token.setter
    def access_token(self, value: Optional[str]):
        """Encrypts and stores the access token."""
        if value:
            self._access_token = encrypt_token(value)
            self.token_hash = hashlib.sha256(value.encode()).hexdigest()
        else:
            self._access_token = None
            self.token_hash = None