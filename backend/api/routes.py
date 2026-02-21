from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from backend.llm.provider_manager import LLMProviderManager
from fastapi.responses import StreamingResponse
from backend.utils.logger import setup_logger
import time

logger = setup_logger()

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: str | None="auto"
    model: str | None=None
    api_key: str | None=None
    stream: bool=False

@router.post("/chat")
def chat(request: ChatRequest):
    start_time = time.time()
    logger.info("Request received")

    manager = LLMProviderManager(
        provider=request.provider,
        model=request.model,
        api_key=request.api_key
    )

    messages = [{"role":"user", "content": request.message}]

    try:
        #streaming
        if request.stream:
            logger.info("Streaming response working")
            def stream_generator():
                for chunk in manager.generate(messages, stream=True):
                    yield chunk
            return StreamingResponse(stream_generator(), media_type="text/plain")
        
        #normal response
        response = manager.generate(messages)

        duration = round(time.time() - start_time, 2)
        logger.info(f"Provider used: {manager.provider_name}")
        logger.info(f"Response time: {duration}s")

        return response

    except Exception as e:
        logger.error(f"Error in request processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))





@router.get("/models")
def get_modes():
    manager = LLMProviderManager()
    return manager.list_models()