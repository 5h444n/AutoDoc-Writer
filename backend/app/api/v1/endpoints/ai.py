import google.generativeai as genai
import os
import warnings
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# SILENCE THE WARNING: This hides the deprecation message so terminal stays clean
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="google.generativeai")

router = APIRouter()

# Global In-Memory History Storage
HISTORY_DB = []

# 1. Configure Global Auth
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env file")
else:
    genai.configure(api_key=api_key)

# Define Input Model
class GenerateReq(BaseModel):
    code: str
    style: str = "standard"

# The Generation Endpoint
@router.post("/preview")
async def generate_preview(request: GenerateReq):
    """
    Generates a preview using the Legacy Google Generative AI SDK.
    """
    if not api_key:
        raise HTTPException(status_code=500, detail="Server Error: GEMINI_API_KEY is missing.")

    try:
        # 2. Initialize the Reliable Model (Flash Latest)
        model = genai.GenerativeModel("models/gemini-flash-latest")

        system_instruction = "You are an expert technical writer."
        if request.style == "latex":
            system_instruction += " Output purely mathematical logic in LaTeX format."
        else:
            system_instruction += " Explain the logic clearly in 2 sentences."

        prompt = f"""
        {system_instruction}
        
        Analyze this code:
        {request.code}
        """
        
        # 3. Generate Content
        response = model.generate_content(prompt)
        
        # 4. Extract Text
        generated_text = response.text
        
        # Clean up text
        clean_text = generated_text.replace("```json", "").replace("```", "").strip()
        
        return {"ai_response": clean_text}

    except Exception as e:
        print(f"❌ AI Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")


class RepoGenerateReq(BaseModel):
    repo_url: str
    style: str = "plain"
    instructions: str = ""

@router.post("/generate")
async def generate_repo_docs(request: RepoGenerateReq):
    """
    Generates documentation for a full repository and saves to history.
    """
    if not api_key:
        raise HTTPException(status_code=500, detail="Server Error: GEMINI_API_KEY is missing.")

    try:
        # 2. Initialize the Reliable Model (Flash Latest)
        model = genai.GenerativeModel("models/gemini-flash-latest")

        prompt = f"""
        You are an expert technical writer.
        Task: Generate comprehensive documentation for the repository at: {request.repo_url}
        
        Style: {request.style}
        Custom Instructions: {request.instructions}
        
        Please provide a detailed documentation structure and overview.
        """
        
        response = model.generate_content(prompt)
        generated_text = response.text
        
        clean_text = generated_text.replace("```json", "").replace("```", "").strip()
        
        # Save to History
        history_item = {
            "id": str(uuid.uuid4()),
            "repo_name": request.repo_url, 
            "style": request.style,
            "timestamp": datetime.now().isoformat(),
            "status": "Success"
        }
        HISTORY_DB.insert(0, history_item) # Add to top of list
        
        return {"documentation": clean_text}

    except Exception as e:
        print(f"❌ AI Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")

@router.get("/history")
async def get_history():
    """
    Returns the global generation history.
    """
    return HISTORY_DB