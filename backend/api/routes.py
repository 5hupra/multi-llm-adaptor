from fastapi import APIRouter
from pydantic import BaseModel
from backend.llm.provider_manager import LLMProviderManager

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: str | None="ollama"
    model: str | None=None

@router.post("/chat")
def chat(request: ChatRequest):
    manager = LLMProviderManager(
        provider=request.provider,
        model=request.model
    )

    response = manager.generate([{"role":"user", "content": request.message}])

    return response