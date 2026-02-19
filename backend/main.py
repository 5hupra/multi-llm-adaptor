from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="Multi LLM Adaptor")
app.include_router(router)