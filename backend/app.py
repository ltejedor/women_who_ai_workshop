from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    Endpoint to handle chat messages.
    Expects a JSON payload with a 'message' field.
    """
    user_message = message.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required.")

    # Simple echo response for demonstration
    bot_response = f"You said: {user_message}"

    return JSONResponse(content={"response": bot_response})