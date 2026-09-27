"""
main.py
FastAPI entry point for FitBuddy - AI Fitness Plan Generator.
Run with: uvicorn app.main:app --reload
Then visit http://127.0.0.1:8000  (docs at /docs)
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

# Create DB tables on startup
init_db()

# Static assets (images, css if any)
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Register all routes
app.include_router(router)
