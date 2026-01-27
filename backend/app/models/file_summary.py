from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class FileSummary(Base):
    __tablename__ = "file_summaries"
    __table_args__ = (
        UniqueConstraint("repo_id", "path", name="uq_file_summary"),
    )

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repositories.id"), index=True, nullable=False)
    path = Column(String, index=True, nullable=False)
    summary = Column(Text, nullable=False)
    blob_sha = Column(String, index=True)
    last_commit_sha = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    repo = relationship("Repository", back_populates="file_summaries")
