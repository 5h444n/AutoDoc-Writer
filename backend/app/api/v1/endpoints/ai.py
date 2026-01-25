from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ai_service import generate_text

router = APIRouter()


class GenerateReq(BaseModel):
    code: str
    style: str = "standard"


@router.post("/preview")
async def generate_preview(request: GenerateReq):
    """
    Generates a short AI preview for a code snippet.
    """
    try:
        system_instruction = "You are an expert technical writer."
        if request.style == "latex":
            system_instruction += " Output purely mathematical logic in LaTeX format."
        elif request.style == "research":
            system_instruction += " Use formal academic language and passive voice."
        else:
            system_instruction += " Explain the logic clearly in 2 sentences."

        prompt = f"""
        {system_instruction}

        Analyze this code:
        {request.code}
        """

        clean_text = generate_text(prompt)
        return {"ai_response": clean_text}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="AI Service Error. Please try again later.")
