from fastapi import Depends, HTTPException, status
from .models import User
from sqlalchemy.orm import Session
from sqlalchemy import select


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

    return {"message": "User has been deleted"}


def user_active_status(id: int, active_status: bool, db: Session):
    db_user = db.get(User, id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db_user.is_active = active_status
    db.commit()

    return {"message": "success"}


def user_admin_status(id: int, admin_status: bool, db: Session):
    user_db = db.get(User, id)

    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_db.is_admin = admin_status
    db.commit()

    return {"message": "success"}


def show_urls(id: int, db: Session):
    pass
