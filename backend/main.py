"""
ShadeAI FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router

app = FastAPI(
    title="ShadeAI",
    version="1.0.0",
    description="AI-Based Skin Tone & Undertone Detection for Cosmetic Shade Recommendation"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "ShadeAI API",
        "version": "1.0.0",
        "docs": "/docs"
    }
