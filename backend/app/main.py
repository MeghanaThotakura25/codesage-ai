from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base

# Import Routers
from app.routers.auth import router as auth_router
from app.routers.review import router as review_router

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Create FastAPI App
app = FastAPI(
    title="CodeSage AI API",
    description="""
AI-Powered Code Review System built using FastAPI and Google Gemini AI.

## Features
- 🔐 JWT Authentication
- 👤 User Registration & Login
- 🤖 AI-Powered Code Review
- 🗄️ PostgreSQL Database
- 📄 Interactive Swagger Documentation

Tech Stack:
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Google Gemini AI
""",
    version="1.0.0",
)

# Root Endpoint
@app.get("/", tags=["Home"])
def root():
    """
    Welcome endpoint.
    """
    return {
        "message": "Welcome to CodeSage AI 🚀",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health Check Endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """
    Check if the API is running.
    """
    return {
        "status": "Running",
        "application": "CodeSage AI"
    }


# Register Authentication Routes
app.include_router(
    auth_router,
    tags=["Authentication"]
)


# Register AI Review Routes
app.include_router(
    review_router,
    tags=["AI Code Review"]
)