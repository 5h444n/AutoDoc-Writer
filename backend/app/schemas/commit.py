from typing import List, Optional

from pydantic import BaseModel, Field


class CommitFile(BaseModel):
    filename: Optional[str] = None
    additions: int = 0
    deletions: int = 0


class CommitItem(BaseModel):
    id: Optional[str] = None
    sha: Optional[str] = None
    full_sha: Optional[str] = None
    message: Optional[str] = None
    author: Optional[str] = None
    author_avatar: Optional[str] = None
    repo_name: Optional[str] = None
    repo_full_name: Optional[str] = None
    timestamp: Optional[str] = None
    files_changed: int = 0
    additions: int = 0
    deletions: int = 0
    has_documentation: bool = False
    files: List[CommitFile] = Field(default_factory=list)


class CommitListResponse(BaseModel):
    commits: List[CommitItem]
