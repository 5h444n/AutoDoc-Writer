from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.documentation import Documentation
from app.models.user import User
from app.schemas.docs import DocsGenerateRequest, DocsGenerateResponse
from app.services.ai_service import generate_text
from app.services.github_service import GitHubService

router = APIRouter()

MAX_CONTEXT_CHARS = 4000


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"


def _build_commit_context(detail: dict) -> str:
    commit_info = detail.get("commit") or {}
    author_info = commit_info.get("author") or {}
    stats = detail.get("stats") or {}
    files = detail.get("files") or []

    lines = [
        f"Commit message: {commit_info.get('message', '')}",
        f"Author: {author_info.get('name', '')}",
        f"Date: {author_info.get('date', '')}",
        f"Stats: +{stats.get('additions', 0)} -{stats.get('deletions', 0)} ({len(files)} files)",
        "",
        "Files changed:",
    ]

    for file_info in files:
        filename = file_info.get("filename", "")
        additions = file_info.get("additions", 0)
        deletions = file_info.get("deletions", 0)
        lines.append(f"- {filename} (+{additions}/-{deletions})")
        patch = file_info.get("patch")
        if patch:
            lines.append(_truncate(patch, 800))
            lines.append("")

    return _truncate("\n".join(lines), MAX_CONTEXT_CHARS)


def _prompt_for(style: str, context: str, complexity: Optional[int]) -> str:
    complexity_hint = ""
    if complexity is not None:
        complexity = max(0, min(complexity, 100))
        complexity_hint = f" Target complexity: {complexity}/100."

    if style == "plainText":
        instruction = (
            "Write concise plain-English documentation for the commit."
            " Provide a short overview and bullet list of key changes."
        )
    elif style == "research":
        instruction = (
            "Write formal academic-style documentation with section headings."
            " Use passive voice and technical precision."
        )
    elif style == "latex":
        instruction = (
            "Return a LaTeX document body (no Markdown)."
            " Use \\section and \\subsection for structure."
        )
    else:
        instruction = "Write technical documentation."

    return f"""
    You are an expert technical writer.{complexity_hint}
    {instruction}
    Base your response strictly on the commit context below.

    Commit context:
    {context}
    """


@router.post("/generate", response_model=DocsGenerateResponse)
def generate_docs(
    request: DocsGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generates documentation for a commit in one or more styles.
    """
    if not current_user.access_token:
        raise HTTPException(status_code=401, detail="Missing GitHub access token")

    styles = ["plainText", "research", "latex"]
    if request.style:
        if request.style not in styles:
            raise HTTPException(status_code=400, detail="Unsupported style")
        styles = [request.style]

    complexity_value = request.complexity if request.complexity is not None else -1

    cached = {}
    for style in styles:
        cached_doc = db.query(Documentation).filter_by(
            user_id=current_user.id,
            repo_full_name=request.repo_full_name,
            commit_sha=request.commit_sha,
            style=style,
            complexity=complexity_value,
        ).first()
        if cached_doc:
            cached[style] = cached_doc

    if cached and not request.force and len(cached) == len(styles):
        latest_cached = max(
            (doc.updated_at or doc.created_at) for doc in cached.values()
        )
        output = {
            "commit_sha": request.commit_sha,
            "commit_short_sha": request.commit_sha[:7],
            "repo_name": request.repo_full_name.split("/")[-1],
            "repo_full_name": request.repo_full_name,
            "generated_at": (latest_cached or datetime.utcnow()).isoformat() + "Z",
            "plain_text": cached.get("plainText").content if cached.get("plainText") else None,
            "research_style": cached.get("research").content if cached.get("research") else None,
            "latex": cached.get("latex").content if cached.get("latex") else None,
        }
        return output

    detail = GitHubService.get_commit_detail(
        current_user.access_token,
        request.repo_full_name,
        request.commit_sha,
        include_patch=True,
    )
    context = _build_commit_context(detail)

    output = {
        "commit_sha": request.commit_sha,
        "commit_short_sha": request.commit_sha[:7],
        "repo_name": request.repo_full_name.split("/")[-1],
        "repo_full_name": request.repo_full_name,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "plain_text": None,
        "research_style": None,
        "latex": None,
    }

    for style in styles:
        cached_doc = cached.get(style)
        should_generate = request.force or cached_doc is None

        if should_generate:
            prompt = _prompt_for(style, context, request.complexity)
            result = generate_text(prompt)

            if cached_doc:
                cached_doc.content = result
                cached_doc.updated_at = datetime.utcnow()
            else:
                cached_doc = Documentation(
                    user_id=current_user.id,
                    repo_full_name=request.repo_full_name,
                    commit_sha=request.commit_sha,
                    style=style,
                    complexity=complexity_value,
                    content=result,
                )
                db.add(cached_doc)

            cached[style] = cached_doc
        else:
            result = cached_doc.content

        if style == "plainText":
            output["plain_text"] = result
        elif style == "research":
            output["research_style"] = result
        elif style == "latex":
            output["latex"] = result

    db.commit()

    return output
