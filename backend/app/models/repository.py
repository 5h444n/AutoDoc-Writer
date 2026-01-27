from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base # Matches your User import

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    full_name = Column(String, index=True)
    url = Column(String)
    last_updated = Column(String)
    
    # Sprint 2 Feature: Monitoring Toggle
    is_active = Column(Boolean, default=False)

    # Repo documentation automation
    docs_active = Column(Boolean, default=False)
    docs_style = Column(String, default="plainText")
    docs_complexity = Column(Integer, default=-1)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="repos")
    repo_docs = relationship("RepoDocumentation", back_populates="repo")
    file_summaries = relationship("FileSummary", back_populates="repo")
