import logging
import threading
import time
import hashlib
import datetime
from typing import Callable, Optional, List, Dict, Any

import google.generativeai as genai
from fastapi import HTTPException
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
import requests

from app.core.config import settings
from app.services.github_service import GitHubService

logger = logging.getLogger(__name__)

# Model selection / config
_model_lock = threading.Lock()
_cached_model_name: Optional[str] = None
_configured = False
_MAX_RETRIES = 3
_BASE_RETRY_DELAY = 1.5
_REQUEST_TIMEOUT = (5, 60)
_PROVIDERS = ("groq", "perplexity", "gemini")

# Simple in-memory cache for summaries (key -> (value, expiry_ts))
_simple_cache: Dict[str, Any] = {}
_DEFAULT_CACHE_TTL = 60 * 60  # 1 hour


def _configure() -> None:
    global _configured
    if _configured:
        return
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    _configured = True


def _get_gemini_model_name() -> str:
    _configure()

    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Server Error: GEMINI_API_KEY is missing.")

    global _cached_model_name
    if _cached_model_name is not None:
        return _cached_model_name

    with _model_lock:
        if _cached_model_name is not None:
            return _cached_model_name

        all_models = list(genai.list_models())
        valid_models = [
            m.name for m in all_models
            if "generateContent" in m.supported_generation_methods
        ]

        if not valid_models:
            raise HTTPException(
                status_code=500,
                detail="Your API Key has no access to any AI models. Check Google AI Studio."
            )

        chosen_model_name = next((m for m in valid_models if "flash" in m), None)
        if not chosen_model_name:
            chosen_model_name = next((m for m in valid_models if "pro" in m), valid_models[0])

        _cached_model_name = chosen_model_name
        return _cached_model_name


def _clean_response(text: str) -> str:
    return text.replace("```json", "").replace("```", "").strip()


def _provider_order():
    raw = (settings.AI_PROVIDER_ORDER or "").strip()
    if not raw:
        return list(_PROVIDERS)
    order = [item.strip().lower() for item in raw.split(",") if item.strip()]
    filtered = [item for item in order if item in _PROVIDERS]
    return filtered or list(_PROVIDERS)


def _openai_compatible_request(
    provider_label: str,
    url: str,
    api_key: str,
    model: str,
    prompt: str,
) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=_REQUEST_TIMEOUT
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502, detail=f"{provider_label} API request failed: {exc}"
        )

    if response.status_code >= 400:
        detail = response.text
        try:
            data = response.json()
            if isinstance(data, dict):
                detail = (
                    data.get("error", {}).get("message")
                    or data.get("message")
                    or detail
                )
        except ValueError:
            pass
        raise HTTPException(
            status_code=response.status_code,
            detail=f"{provider_label} error: {detail}",
        )

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502, detail=f"{provider_label} returned invalid JSON."
        )

    content = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content")
    )
    if not content:
        raise HTTPException(
            status_code=502, detail=f"{provider_label} returned an empty response."
        )
    return _clean_response(content)


def _generate_with_gemini(prompt: str) -> str:
    model_name = _get_gemini_model_name()
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return _clean_response(response.text)


def _retry(call: Callable[[], str], provider_label: str) -> str:
    for attempt in range(_MAX_RETRIES):
        try:
            return call()
        except (ResourceExhausted, ServiceUnavailable):
            if attempt == _MAX_RETRIES - 1:
                raise HTTPException(
                    status_code=429,
                    detail=f"{provider_label} quota exceeded. Try later or update billing.",
                )
            time.sleep(_BASE_RETRY_DELAY * (2 ** attempt))
        except HTTPException as exc:
            if exc.status_code in (429, 503) and attempt < _MAX_RETRIES - 1:
                time.sleep(_BASE_RETRY_DELAY * (2 ** attempt))
                continue
            raise
    raise HTTPException(status_code=500, detail="AI generation failed unexpectedly.")


def generate_text(prompt: str) -> str:
    errors = []
    attempted = False

    for provider in _provider_order():
        if provider == "groq":
            if not settings.GROQ_API_KEY:
                continue
            attempted = True
            try:
                return _retry(
                    lambda: _openai_compatible_request(
                        "Groq",
                        "https://api.groq.com/openai/v1/chat/completions",
                        settings.GROQ_API_KEY,
                        settings.GROQ_MODEL,
                        prompt,
                    ),
                    "Groq",
                )
            except HTTPException as exc:
                errors.append(f"Groq: {exc.detail}")
            except Exception as exc:
                logger.exception("Groq provider failed")
                errors.append(f"Groq: {exc}")
        elif provider == "perplexity":
            if not settings.PERPLEXITY_API_KEY:
                continue
            attempted = True
            try:
                return _retry(
                    lambda: _openai_compatible_request(
                        "Perplexity",
                        "https://api.perplexity.ai/chat/completions",
                        settings.PERPLEXITY_API_KEY,
                        settings.PERPLEXITY_MODEL,
                        prompt,
                    ),
                    "Perplexity",
                )
            except HTTPException as exc:
                errors.append(f"Perplexity: {exc.detail}")
            except Exception as exc:
                logger.exception("Perplexity provider failed")
                errors.append(f"Perplexity: {exc}")
        elif provider == "gemini":
            if not settings.GEMINI_API_KEY:
                continue
            attempted = True
            try:
                return _retry(lambda: _generate_with_gemini(prompt), "Gemini")
            except HTTPException as exc:
                errors.append(f"Gemini: {exc.detail}")
            except Exception as exc:
                logger.exception("Gemini provider failed")
                errors.append(f"Gemini: {exc}")

    if not attempted:
        raise HTTPException(
            status_code=500,
            detail="No AI providers configured. Set GROQ_API_KEY, PERPLEXITY_API_KEY, or GEMINI_API_KEY.",
        )

    raise HTTPException(
        status_code=502,
        detail="All AI providers failed. " + " | ".join(errors),
    )


def _cache_get(key: str):
    entry = _simple_cache.get(key)
    if not entry:
        return None
    value, expiry = entry
    if expiry is None:
        return value
    if time.time() > expiry:
        try:
            del _simple_cache[key]
        except KeyError:
            pass
        return None
    return value


def _cache_set(key: str, value: Any, ttl: Optional[int] = None):
    expiry = None
    if ttl is None:
        ttl = _DEFAULT_CACHE_TTL
    if ttl and ttl > 0:
        expiry = time.time() + ttl
    _simple_cache[key] = (value, expiry)


def _make_cache_key(*parts) -> str:
    m = hashlib.sha256()
    for p in parts:
        if p is None:
            continue
        if not isinstance(p, (str, bytes)):
            p = str(p)
        if isinstance(p, str):
            p = p.encode("utf-8")
        m.update(p)
    return m.hexdigest()


def summarize_text(prompt: str, cache_ttl: Optional[int] = None) -> str:
    """Generate a concise summary for arbitrary text using the configured AI provider.

    This wraps `generate_text` and applies a stable prompt template and optional caching.
    """
    key = _make_cache_key("summarize_text", prompt)
    cached = _cache_get(key)
    if cached:
        return cached

    system_prompt = (
        "You are an assistant that produces short JSON summaries for code repositories and files. "
        "Return a concise JSON object with keys: summary, highlights (list of strings), and estimate_files (int) where applicable. "
        "Keep the output compact and valid JSON only."
    )

    full_prompt = f"{system_prompt}\n\nInput:\n{prompt}\n\nRespond with JSON only."
    result = generate_text(full_prompt)
    _cache_set(key, result, ttl=cache_ttl)
    return result


def summarize_files(files: List[Dict[str, Any]], max_chars: int = 20000, cache_ttl: Optional[int] = None) -> List[str]:
    """Summarize a list of files. Files should be dicts with keys `path` and `content`.

    Large inputs are chunked into groups of approximately `max_chars` characters.
    Returns a list of summary JSON strings (one per chunk).
    """
    if not files:
        return []

    # Build chunks
    chunks: List[List[Dict[str, Any]]] = []
    current: List[Dict[str, Any]] = []
    current_size = 0
    for f in files:
        c = f.get("content") or ""
        entry_size = len(c)
        if entry_size > max_chars and current:
            chunks.append(current)
            current = [f]
            current_size = entry_size
            continue
        if current_size + entry_size > max_chars and current:
            chunks.append(current)
            current = [f]
            current_size = entry_size
        else:
            current.append(f)
            current_size += entry_size
    if current:
        chunks.append(current)

    summaries: List[str] = []
    for chunk in chunks:
        combined = "\n\n".join([f"=== {f.get('path')} ===\n{(f.get('content') or '')}" for f in chunk])
        key = _make_cache_key("summarize_files", combined)
        cached = _cache_get(key)
        if cached:
            summaries.append(cached)
            continue

        prompt = (
            "You are an assistant that summarizes multiple source files. For each file, produce a small JSON entry with file, summary, and notable_findings. "
            "Return a JSON array of entries."
            f"\n\nFiles:\n{combined}\n\nRespond with JSON only."
        )
        summary = generate_text(prompt)
        _cache_set(key, summary, ttl=cache_ttl)
        summaries.append(summary)

    return summaries


def summarize_repository(access_token: str, repo_full_name: str, max_files: int = 200, max_chars: int = 20000, cache_ttl: Optional[int] = None) -> Dict[str, Any]:
    """Produce a repository-level summary by fetching files from GitHub and summarizing them.

    - Filters common source file extensions.
    - Limits number of files and total characters to avoid huge payloads.
    Returns a dict with keys: repo, summaries (list), metadata.
    """
    key = _make_cache_key("summarize_repo", repo_full_name)
    cached = _cache_get(key)
    if cached:
        return cached

    tree = GitHubService.get_repo_tree(access_token, repo_full_name)
    # filter for likely source/docs files
    exts = {".py", ".md", ".txt", ".js", ".ts", ".java", ".rs", ".go", ".cpp", ".c", ".json", ".yml", ".yaml"}
    files: List[Dict[str, Any]] = []
    collected_chars = 0
    for node in tree:
        path = node.get("path")
        if not path:
            continue
        if len(files) >= max_files:
            break
        if any(path.endswith(ext) for ext in exts):
            content, sha = GitHubService.get_file_content(access_token, repo_full_name, path)
            if content is None:
                continue
            content = content[: max_chars] if len(content) > max_chars else content
            files.append({"path": path, "content": content})
            collected_chars += len(content)
            if collected_chars > max_chars * 5:
                break

    summaries = summarize_files(files, max_chars=max_chars, cache_ttl=cache_ttl)

    result = {
        "repo": repo_full_name,
        "file_count": len(files),
        "summaries": summaries,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

    _cache_set(key, result, ttl=cache_ttl)
    return result
