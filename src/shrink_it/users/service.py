from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..auth.security import hash_password, verify_password
from .models import User
from .schemas import UpdateUser, UpdateUserPassword


def user_get(db: Session):
    statement = select(User)
    db_user = db.scalars(statement).all()

    return db_user


def user_get_by_id(id: int, db: Session):
    statement = select(User).where(User.id == id)
    db_user = db.scalar(statement)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


def user_delete(id: int, db: Session):
    db_user = db.get(User, id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if db_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    db.delete(db_user)
    db.commit()


def user_active_status(id: int, active_status: bool, db: Session):
    db_user = db.get(User, id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db_user.is_active = active_status
    db.commit()
    db.refresh(db_user)

    return db_user


def user_admin_status(id: int, admin_status: bool, db: Session):
    user_db = db.get(User, id)

    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_db.is_admin = admin_status
    db.commit()
    db.refresh(user_db)

    return user_db


def user_update(id: int, user: UpdateUser, db: Session):
    statement = select(User).where(User.id == id)

    db_user = db.scalar(statement)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    data = user.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in data.items():
        setattr(db_user, field, value)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or phone number already exists",
        )

    return db_user


def update_password(id: int, password: UpdateUserPassword, db: Session):
    db_user = db.get(User, id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not verify_password(password.current_password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    new_hashed_password = hash_password(password.new_password)

    db_user.password = new_hashed_password

    db.commit()
