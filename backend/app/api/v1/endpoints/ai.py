from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.ai_service import generate_text
from app.core.prompts import DocumentationPrompts
from app.core.validators import InputValidator
from app.core.logger import setup_logger, log_error, log_request
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = setup_logger(__name__)


class GenerateReq(BaseModel):
    code: str
    style: str = "plain"
    filename: str | None = None


@router.post("/preview")
@limiter.limit("20/minute")  # AI calls are expensive, limit to 20/min
async def generate_preview(
    request: GenerateReq,
    req: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Generates AI documentation for a code snippet.
    
    Supports three styles:
    - plain: Friendly, conversational explanations
    - research: Formal academic documentation
    - latex: Publication-ready LaTeX format
    
    Rate limit: 20 requests per minute
    """
    try:
        # Log the request
        log_request(logger, "POST", "/ai/preview", current_user.id)
        
        # Validate inputs
        style = InputValidator.validate_documentation_style(request.style)
        code = InputValidator.sanitize_text_input(request.code, max_length=50000)
        
        if request.filename:
            filename = InputValidator.validate_file_path(request.filename)
        else:
            filename = None
        
        # Get appropriate system prompt for style
        system_instruction = DocumentationPrompts.get_prompt(style)
        
        # Build user prompt with code
        user_prompt = DocumentationPrompts.build_user_prompt(code, style, filename)
        
        # Generate documentation
        logger.info(f"Generating {style} documentation for user {current_user.id}")
        clean_text = generate_text(user_prompt, system_instruction=system_instruction)
        
        # Validate output
        if not DocumentationPrompts.validate_output(clean_text, style):
            logger.warning(f"Generated output failed validation for style: {style}")
        
        logger.info(f"Successfully generated {len(clean_text)} characters of documentation")
        
        return {"ai_response": clean_text, "style": style}
        
    except HTTPException:
        raise
    except ValueError as e:
        log_error(logger, e, "Validation error in AI preview")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log_error(logger, e, "AI Service Error in preview generation")
        raise HTTPException(status_code=500, detail="AI Service Error. Please try again later.")
