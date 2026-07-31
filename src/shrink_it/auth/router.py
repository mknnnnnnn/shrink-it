from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..users.schemas import UserRegister, UserLogin, UserResponse
from .service import (
    login_user as login_user_service,
    register_user as register_user_service,
)
from .schemas import Token
from .dependencies import get_current_user
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    return register_user_service(user=user, db=db)


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return login_user_service(
        email=form_data.username, password=form_data.password, db=db
    )
