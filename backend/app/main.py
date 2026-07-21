from fastapi import FastAPI
from fastapi import Depends
from app.utils.dependencies import get_current_user
from app.models.user import User
from fastapi import Depends



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

@app.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }