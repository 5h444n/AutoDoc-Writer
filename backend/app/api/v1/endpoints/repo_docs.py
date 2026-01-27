from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.repo_documentation import RepoDocumentation
from app.models.repository import Repository
from app.models.user import User
from app.schemas.repo_docs import (
    RepoDocsActivateRequest,
    RepoDocsGenerateRequest,
    RepoDocsResponse,
)
from app.services.repo_doc_service import generate_repo_documentation

router = APIRouter()

_ALLOWED_STYLES = {"plainText", "research", "latex"}


def _find_repo(db: Session, user_id: int, repo_full_name: str) -> Optional[Repository]:
    repo = db.query(Repository).filter(
        Repository.owner_id == user_id,
        Repository.full_name == repo_full_name,
    ).first()
    if repo:
        return repo
    repo_name = repo_full_name.split("/")[-1]
    repo = db.query(Repository).filter(
        Repository.owner_id == user_id,
        Repository.name == repo_name,
    ).first()
    if repo and not repo.full_name:
        repo.full_name = repo_full_name
        db.commit()
    return repo


def _normalize_style(style: Optional[str]) -> str:
    if not style:
        return "plainText"
    if style not in _ALLOWED_STYLES:
        raise HTTPException(status_code=400, detail="Unsupported style")
    return style


@router.post("/activate", response_model=RepoDocsResponse)
def activate_repo_docs(
    request: RepoDocsActivateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.access_token:
        raise HTTPException(status_code=401, detail="Missing GitHub access token")

    repo = _find_repo(db, current_user.id, request.repo_full_name)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    style = _normalize_style(request.style)
    complexity = request.complexity
    repo.docs_active = True
    repo.docs_style = style
    repo.docs_complexity = complexity if complexity is not None else -1
    db.commit()

    doc = generate_repo_documentation(
        db=db,
        repo=repo,
        access_token=current_user.access_token,
        style=style,
        complexity=complexity,
        force=request.force,
    )

    return RepoDocsResponse(
        repo_full_name=repo.full_name or request.repo_full_name,
        style=doc.style,
        complexity=doc.complexity,
        generated_at=(doc.updated_at or doc.created_at).isoformat() + "Z",
        content=doc.content,
    )


@router.post("/generate", response_model=RepoDocsResponse)
def generate_repo_docs(
    request: RepoDocsGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.access_token:
        raise HTTPException(status_code=401, detail="Missing GitHub access token")

    repo = _find_repo(db, current_user.id, request.repo_full_name)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    style = _normalize_style(request.style)
    doc = generate_repo_documentation(
        db=db,
        repo=repo,
        access_token=current_user.access_token,
        style=style,
        complexity=request.complexity,
        force=request.force,
    )

    return RepoDocsResponse(
        repo_full_name=repo.full_name or request.repo_full_name,
        style=doc.style,
        complexity=doc.complexity,
        generated_at=(doc.updated_at or doc.created_at).isoformat() + "Z",
        content=doc.content,
    )


@router.get("/latest", response_model=RepoDocsResponse)
def get_latest_repo_docs(
    repo_full_name: str = Query(...),
    style: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = _find_repo(db, current_user.id, repo_full_name)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    if style:
        style = _normalize_style(style)
        doc = db.query(RepoDocumentation).filter_by(
            repo_id=repo.id, style=style
        ).first()
    else:
        doc = db.query(RepoDocumentation).filter_by(repo_id=repo.id).order_by(
            RepoDocumentation.updated_at.desc()
        ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="No documentation found")

    return RepoDocsResponse(
        repo_full_name=repo.full_name or repo_full_name,
        style=doc.style,
        complexity=doc.complexity,
        generated_at=(doc.updated_at or doc.created_at).isoformat() + "Z",
        content=doc.content,
    )
