from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    bot_response = f"You said: {user_input}"  # Replace with chatbot logic
    return {"reply": bot_response}



