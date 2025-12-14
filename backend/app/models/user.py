from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    github_username = Column(String, unique=True, index=True)
    access_token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- ADD THIS LINE --- TANIM
    repos = relationship("Repository", back_populates="owner")