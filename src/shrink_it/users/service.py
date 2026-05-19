from fastapi import Depends, HTTPException
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
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    return db_user
