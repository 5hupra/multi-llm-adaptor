from fastapi import APIRouter
from pydantic import BaseModel
from backend.llm.provider_manager import LLMProviderManager

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: str | None="auto"
    model: str | None=None
    api_key: str | None=None

@router.post("/chat")
def chat(request: ChatRequest):
    manager = LLMProviderManager(
        provider=request.provider,
        model=request.model,
        api_key=request.api_key
    )

    response = manager.generate([{"role":"user", "content": request.message}])

    return response