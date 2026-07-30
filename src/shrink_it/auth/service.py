from ..users.models import User
from ..users.schemas import UserRegister
from .security import hash_password, verify_password, create_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status


def register_user(user: UserRegister, db: Session):

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
        phone_number=user.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(email: str, password: str, db: Session):
    statement = select(User).where(User.email == email)
    db_user = db.scalar(statement)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_token({"email": db_user.email})

    return {"access_token": access_token, "token_type": "bearer"}
