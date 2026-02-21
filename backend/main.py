from fastapi import FastAPI
from backend.api.routes import router
from dotenv import load_dotenv
from backend.utils.logger import setup_logger
from fastapi.middleware.cors import CORSMiddleware
import os


load_dotenv()
logger = setup_logger()

app = FastAPI(title="Multi LLM Adaptor")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Adaptor API is running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)