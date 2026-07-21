from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user_schema import UserCreate, UserResponse, Token
from app.services.user_service import register_user, login_user

# Create Router
router = APIRouter()


# ==========================
# Register User
# ==========================
@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    return register_user(user, db)


# ==========================
# Login User
# ==========================
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login user and generate JWT token.

    Note:
    Swagger shows 'username', but you should enter the user's EMAIL.
    """

    return login_user(
        form_data.username,   # Email
        form_data.password,
        db
    )