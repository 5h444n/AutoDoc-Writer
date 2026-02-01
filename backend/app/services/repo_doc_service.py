import os
from typing import Iterable, List, Optional, Sequence, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.file_summary import FileSummary
from app.models.repo_documentation import RepoDocumentation
from app.models.repository import Repository
from app.services.ai_service import generate_text
from app.services.github_service import GitHubService

MAX_FILES = 60
MAX_FILE_CHARS = 4000
MAX_SUMMARY_CHARS = 12000

_SKIP_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "dist",
    "build",
    "out",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
}

_SKIP_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".svg",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".rar",
    ".7z",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".class",
    ".jar",
    ".lock",
    ".min.js",
    ".min.css",
}

_SKIP_FILENAMES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "pipfile.lock",
}


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"


def _should_skip_path(path: str) -> bool:
    lowered = path.lower()
    if any(part in lowered.split("/") for part in _SKIP_DIRS):
        return True
    filename = os.path.basename(lowered)
    if filename in _SKIP_FILENAMES:
        return True
    _, ext = os.path.splitext(lowered)
    if ext in _SKIP_EXTENSIONS:
        return True
    if filename.endswith(".min.js") or filename.endswith(".min.css"):
        return True
    return False


def _repo_full_name(repo: Repository) -> str:
    if repo.full_name:
        return repo.full_name
    if repo.url and "github.com/" in repo.url:
        return repo.url.split("github.com/")[-1].strip("/")
    raise HTTPException(status_code=400, detail="Repository full_name is missing.")


def _file_summary_prompt(path: str, content: str) -> str:
    return f"""
    You are an expert technical writer.
    Summarize the purpose of this file for a repo-level documentation system.
    Keep it concise (3-6 sentences). Mention key functions, classes, or configs.

    File path: {path}
    File content:
    {content}
    """


def _repo_doc_prompt(style: str, summaries: Sequence[Tuple[str, str]], complexity: Optional[int]) -> str:
    complexity_hint = ""
    if complexity is not None:
        complexity = max(0, min(complexity, 100))
        complexity_hint = f" Target complexity: {complexity}/100."

    if style == "plainText":
        instruction = (
            "Write concise plain-English documentation for the entire repository."
            " Provide a short overview, main components, and usage notes."
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
        instruction = "Write technical documentation for the repository."

    formatted = "\n".join(
        f"File: {path}\nSummary: {summary}\n" for path, summary in summaries
    )
    formatted = _truncate(formatted, MAX_SUMMARY_CHARS)

    return f"""
    You are an expert technical writer.{complexity_hint}
    {instruction}
    Base your response strictly on the file summaries below.

    File summaries:
    {formatted}
    """


def _summarize_file(path: str, content: str) -> str:
    prompt = _file_summary_prompt(path, content)
    return generate_text(prompt)


def _upsert_repo_doc(
    db: Session,
    repo: Repository,
    style: str,
    complexity: int,
    content: str,
) -> RepoDocumentation:
    existing = db.query(RepoDocumentation).filter_by(
        repo_id=repo.id,
        style=style,
        complexity=complexity,
    ).first()
    if existing:
        existing.content = content
        return existing

    doc = RepoDocumentation(
        repo_id=repo.id,
        style=style,
        complexity=complexity,
        content=content,
    )
    db.add(doc)
    return doc


def generate_repo_documentation(
    db: Session,
    repo: Repository,
    access_token: str,
    style: str,
    complexity: Optional[int],
    force: bool = False,
    ref: str = "HEAD",
):
    repo_full_name = _repo_full_name(repo)
    tree = GitHubService.get_repo_tree(access_token, repo_full_name, ref=ref)

    summaries: List[Tuple[str, str]] = []
    processed = 0

    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item.get("path") or ""
        if not path or _should_skip_path(path):
            continue
        if processed >= MAX_FILES:
            break

        blob_sha = item.get("sha")
        existing = db.query(FileSummary).filter_by(repo_id=repo.id, path=path).first()
        if existing and existing.blob_sha == blob_sha and not force:
            summaries.append((path, existing.summary))
            processed += 1
            continue

        content, sha = GitHubService.get_file_content(access_token, repo_full_name, path, ref=ref)
        if not content:
            continue
        content = _truncate(content, MAX_FILE_CHARS)
        summary = _summarize_file(path, content)

        if existing:
            existing.summary = summary
            existing.blob_sha = sha or blob_sha
        else:
            existing = FileSummary(
                repo_id=repo.id,
                path=path,
                summary=summary,
                blob_sha=sha or blob_sha,
            )
            db.add(existing)

        summaries.append((path, summary))
        processed += 1

    if not summaries:
        raise HTTPException(status_code=400, detail="No text files found to document.")

    complexity_value = complexity if complexity is not None else -1
    prompt = _repo_doc_prompt(style, summaries, complexity)
    content = generate_text(prompt)
    doc = _upsert_repo_doc(db, repo, style, complexity_value, content)
    db.commit()
    db.refresh(doc)
    return doc


def update_repo_from_push(
    db: Session,
    repo: Repository,
    access_token: str,
    changed_files: Iterable[str],
    removed_files: Iterable[str],
    head_sha: str,
):
    repo_full_name = _repo_full_name(repo)

    for path in removed_files:
        db.query(FileSummary).filter_by(repo_id=repo.id, path=path).delete()

    for path in changed_files:
        if _should_skip_path(path):
            continue
        content, sha = GitHubService.get_file_content(access_token, repo_full_name, path, ref=head_sha)
        if not content:
            continue
        content = _truncate(content, MAX_FILE_CHARS)
        summary = _summarize_file(path, content)

        existing = db.query(FileSummary).filter_by(repo_id=repo.id, path=path).first()
        if existing:
            existing.summary = summary
            existing.blob_sha = sha
            existing.last_commit_sha = head_sha
        else:
            db.add(
                FileSummary(
                    repo_id=repo.id,
                    path=path,
                    summary=summary,
                    blob_sha=sha,
                    last_commit_sha=head_sha,
                )
            )

    summaries = [
        (item.path, item.summary)
        for item in db.query(FileSummary).filter_by(repo_id=repo.id).order_by(FileSummary.path).all()
    ][:MAX_FILES]

    if summaries:
        style = repo.docs_style or "plainText"
        complexity_value = repo.docs_complexity if repo.docs_complexity is not None else -1
        prompt = _repo_doc_prompt(style, summaries, complexity_value)
        content = generate_text(prompt)
        _upsert_repo_doc(db, repo, style, complexity_value, content)

    db.commit()
