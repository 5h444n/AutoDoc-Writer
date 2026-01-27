import hmac
import hashlib
from typing import Iterable

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.repository import Repository
from app.models.user import User
from app.services.repo_doc_service import update_repo_from_push

router = APIRouter()


def _verify_signature(payload: bytes, signature_header: str) -> None:
    if not settings.GITHUB_WEBHOOK_SECRET:
        return
    if not signature_header or not signature_header.startswith("sha256="):
        raise HTTPException(status_code=401, detail="Missing webhook signature")
    expected = "sha256=" + hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected, signature_header):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")


def _process_push_event(
    repo_full_name: str,
    head_sha: str,
    changed_files: Iterable[str],
    removed_files: Iterable[str],
):
    db: Session = SessionLocal()
    try:
        repo = db.query(Repository).filter(Repository.full_name == repo_full_name).first()
        if not repo:
            repo_name = repo_full_name.split("/")[-1]
            repo = db.query(Repository).filter(Repository.name == repo_name).first()
        if not repo or not repo.docs_active:
            return

        user = db.query(User).filter(User.id == repo.owner_id).first()
        if not user or not user.access_token:
            return

        update_repo_from_push(
            db=db,
            repo=repo,
            access_token=user.access_token,
            changed_files=changed_files,
            removed_files=removed_files,
            head_sha=head_sha,
        )
    finally:
        db.close()


@router.post("/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None),
):
    payload = await request.body()
    _verify_signature(payload, x_hub_signature_256)

    if x_github_event == "ping":
        return {"status": "ok"}

    if x_github_event != "push":
        return {"status": "ignored"}

    data = await request.json()
    repo_full_name = data.get("repository", {}).get("full_name")
    head_sha = data.get("after")
    if not repo_full_name or not head_sha:
        raise HTTPException(status_code=400, detail="Invalid webhook payload")

    changed_files = set()
    removed_files = set()
    for commit in data.get("commits", []) or []:
        changed_files.update(commit.get("added", []) or [])
        changed_files.update(commit.get("modified", []) or [])
        removed_files.update(commit.get("removed", []) or [])

    changed_files = changed_files - removed_files

    background_tasks.add_task(
        _process_push_event,
        repo_full_name,
        head_sha,
        list(changed_files),
        list(removed_files),
    )

    return {"status": "queued"}
