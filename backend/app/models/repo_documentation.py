from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class RepoDocumentation(Base):
    __tablename__ = "repo_documentations"
    __table_args__ = (
        UniqueConstraint("repo_id", "style", "complexity", name="uq_repo_docs"),
    )

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), index=True, nullable=False)
    style = Column(String, index=True, nullable=False, default="plainText")
    complexity = Column(Integer, index=True, nullable=False, default=-1)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    repo = relationship("Repository", back_populates="repo_docs")
