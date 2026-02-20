from fastapi import FastAPI
from backend.api.routes import router
from dotenv import load_dotenv
from backend.utils.logger import setup_logger
import os

load_dotenv()
logger = setup_logger()

app = FastAPI(title="Multi LLM Adaptor")
app.include_router(router)