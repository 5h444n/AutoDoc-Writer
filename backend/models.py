from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    github_repo_id = Column(Integer, unique=True, index=True) # ID from GitHub
    name = Column(String)
    url = Column(String)
    is_active = Column(Boolean, default=False) # The toggle for monitoring