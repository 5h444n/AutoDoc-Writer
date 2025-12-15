from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app.db.base import Base
from app.core.security import encrypt_token, decrypt_token


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    github_username = Column(String, unique=True, index=True)
    _access_token = Column("access_token", String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- ADD THIS LINE --- TANIM
    repos = relationship("Repository", back_populates="owner")

    @hybrid_property
    def access_token(self) -> str:
        """Decrypts and returns the access token."""
        if self._access_token:
            return decrypt_token(self._access_token)
        return None

    @access_token.setter
    def access_token(self, value: str):
        """Encrypts and stores the access token."""
        if value:
            self._access_token = encrypt_token(value)
        else:
            self._access_token = None