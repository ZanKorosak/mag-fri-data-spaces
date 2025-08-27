from fastapi import FastAPI
from src.routers.files import router as files_router
from src.routers.files import router as legacy_files_router
import src.utils.logging_config
import logging

app = FastAPI()

app.include_router(files_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}