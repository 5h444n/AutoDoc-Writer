import google.generativeai as genai
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# 1. Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env file")
else:
    genai.configure(api_key=api_key)

# 2. Define Input Model
class GenerateReq(BaseModel):
    code: str
    style: str = "standard"

# 3. The Generation Endpoint
@router.post("/preview")
async def generate_preview(request: GenerateReq):
    """
    Automatically finds a working Gemini model and generates a preview.
    """
    if not api_key:
        raise HTTPException(status_code=500, detail="Server Error: GEMINI_API_KEY is missing.")

    try:
        # --- AUTO-DISCOVERY LOGIC (The Fix) ---
        # 1. Ask Google which models are available for this specific API Key
        all_models = list(genai.list_models())
        
        # 2. Filter for models that can generate content (text)
        valid_models = [
            m.name for m in all_models 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        if not valid_models:
             raise HTTPException(status_code=500, detail="Your API Key has no access to any AI models. Check Google AI Studio.")

        # 3. Smart Selection: Prefer 'flash', then 'pro', then whatever is left
        chosen_model_name = next((m for m in valid_models if 'flash' in m), None)
        if not chosen_model_name:
            chosen_model_name = next((m for m in valid_models if 'pro' in m), valid_models[0])

        print(f"🤖 Server selected model: {chosen_model_name}") # This prints to your terminal so you know what worked
        
        # 4. Initialize the chosen model
        model = genai.GenerativeModel(chosen_model_name)
        # -------------------------------------

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
        
        response = model.generate_content(prompt)
        
        # Clean up text
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        
        return {"ai_response": clean_text}

    except Exception as e:
        print(f"❌ AI Error: {e}") # Check your terminal for this if it fails
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")