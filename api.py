from fastapi import FastAPI
from pydantic import BaseModel
from core.agent import process_chat

app = FastAPI(title="LiveFX-Converter API", description="FastAPI Backend for Currency Conversions using Agents.")

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint that receives a natural language query,
    processes it via Langchain AI agents, and returns the response.
    """
    try:
        reply = process_chat(request.query)
        return ChatResponse(response=reply)
    except Exception as e:
        return ChatResponse(response=f"Error occurred: {str(e)}")

# Add a simple health check
@app.get("/")
def read_root():
    return {"status": "Backend is running"}
