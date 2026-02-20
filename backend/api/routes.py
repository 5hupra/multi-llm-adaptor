from fastapi import APIRouter
from pydantic import BaseModel
from backend.llm.provider_manager import LLMProviderManager
from fastapi.responses import StreamingResponse

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: str | None="auto"
    model: str | None=None
    api_key: str | None=None
    stream: bool=False

@router.post("/chat")
def chat(request: ChatRequest):
    manager = LLMProviderManager(
        provider=request.provider,
        model=request.model,
        api_key=request.api_key
    )

    messages = [{"role":"user", "content": request.message}]

    #streaming
    if request.stream:
        generator = manager.generate(messages, stream=True)
        return StreamingResponse(generator, media_type="text/plain")
    
    #normal response
    return manager.generate(messages)