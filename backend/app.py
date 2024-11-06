from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(message: dict):
    """
    Endpoint to prompt Gemini API.
    Expects a JSON body with a "prompt" field.
    Returns the Gemini response.
    """
    try:
        # Get the request body
        prompt = message.get("message")
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        # Configure Gemini with API key from environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="Google API key not found in environment variables"
            )

        genai.configure(api_key=api_key)
        
        # Initialize the model and generate response
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Return the response
        return {
            "status": "success",
            "response": response.text
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )