import logging
import threading
import time
from typing import Callable, Optional

import google.generativeai as genai
from fastapi import HTTPException
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
import requests

from app.core.config import settings

logger = logging.getLogger(__name__)

_model_lock = threading.Lock()
_cached_model_name: Optional[str] = None
_configured = False
_MAX_RETRIES = 3
_BASE_RETRY_DELAY = 1.5
_REQUEST_TIMEOUT = (5, 60)
_PROVIDERS = ("groq", "perplexity", "gemini")


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
