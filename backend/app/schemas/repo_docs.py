from typing import Optional

from pydantic import BaseModel


class RepoDocsActivateRequest(BaseModel):
    repo_full_name: str
    style: Optional[str] = "plainText"
    complexity: Optional[int] = None
    force: bool = False


class RepoDocsGenerateRequest(BaseModel):
    repo_full_name: str
    style: Optional[str] = "plainText"
    complexity: Optional[int] = None
    force: bool = False


class RepoDocsResponse(BaseModel):
    repo_full_name: str
    style: str
    complexity: int
    generated_at: str
    content: str
