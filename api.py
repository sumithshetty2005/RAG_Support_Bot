from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.graph_logic import SupportGraph
import uvicorn
import os

app = FastAPI(title="Customer Support RAG API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = SupportGraph()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    escalated: bool
    needs_confirmation: bool
    context: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = graph.run(request.query)
        return ChatResponse(
            response=result["response"],
            escalated=result.get("escalated", False),
            needs_confirmation=result.get("needs_confirmation", False),
            context=result.get("context", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
