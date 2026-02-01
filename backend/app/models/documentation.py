from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class Documentation(Base):
    __tablename__ = "documentations"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "repo_full_name",
            "commit_sha",
            "style",
            "complexity",
            name="uq_docs_cache",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    repo_full_name = Column(String, index=True, nullable=False)
    commit_sha = Column(String, index=True, nullable=False)
    style = Column(String, index=True, nullable=False)
    complexity = Column(Integer, index=True, nullable=False, default=-1)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="docs")
