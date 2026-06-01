from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .schemas import TokenData
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token
from ..users.models import User
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    decoded_token = decode_token(token)

    email = decoded_token.get("email")

    if email is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = TokenData(email=email)

    statement = select(User).where(User.email == token_data.email)
    db_user = db.scalar(statement)

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return db_user


def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    return user
