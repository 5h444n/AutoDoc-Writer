import threading
from typing import Optional

import google.generativeai as genai
from fastapi import HTTPException
from google.api_core.exceptions import ResourceExhausted

from app.core.config import settings

_model_lock = threading.Lock()
_cached_model_name: Optional[str] = None
_configured = False


def _configure() -> None:
    global _configured
    if _configured:
        return
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    _configured = True


def get_model_name() -> str:
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


def generate_text(prompt: str) -> str:
    model_name = get_model_name()
    model = genai.GenerativeModel(model_name)
    try:
        response = model.generate_content(prompt)
    except ResourceExhausted:
        raise HTTPException(
            status_code=429,
            detail="Gemini quota exceeded. Try later or update billing."
        )
    return response.text.replace("```json", "").replace("```", "").strip()
