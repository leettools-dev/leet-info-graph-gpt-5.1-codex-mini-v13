from fastapi import FastAPI
from pathlib import Path

from backend.app.api.v1.infographic import router as infographic_router

app = FastAPI(title="Research Infographic Studio API", version="0.1.0")

app.include_router(infographic_router, prefix="/api/v1/infographics", tags=["Infographics"])
