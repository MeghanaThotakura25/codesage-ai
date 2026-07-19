from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CodeSage AI Backend"
    }