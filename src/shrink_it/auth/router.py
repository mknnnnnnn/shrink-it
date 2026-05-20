from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..users.schemas import UserRegister, UserLogin, UserResponse
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    pass


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    pass
