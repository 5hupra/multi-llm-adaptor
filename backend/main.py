from fastapi import FastAPI
from backend.api.routes import router
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI(title="Multi LLM Adaptor")
app.include_router(router)