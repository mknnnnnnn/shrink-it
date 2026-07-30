from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse, RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
from random import choices
from datetime import datetime
from io import BytesIO
import string
import qrcode

from sqlalchemy.orm import Session
from sqlalchemy import select

from .schemas import URLCreate
from .models import URL


def generate_code(length: int = 5) -> str:
    return "".join(choices(string.ascii_letters + string.digits, k=length))


def generate_qr_code(short_code: str, user_id: int, db: Session):
    statement = select(URL).where(URL.short_code == short_code, URL.user_id == user_id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    img = qrcode.make(db_url.original_url)
    buffer = BytesIO()

    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(
        buffer, status_code=status.HTTP_201_CREATED, media_type="image/png"
    )


def increase_click_count(url: URL, db: Session):
    url.click_count = (url.click_count or 0) + 1
    db.commit()
    db.refresh(url)


def url_create(url: URLCreate, db: Session, user_id: int):
    short_code = url.short_code or generate_code()

    existing_db_url = db.scalar(select(URL).where(URL.short_code == short_code))

    if existing_db_url:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Short code already exists"
        )

    db_url = URL(
        original_url=str(url.original_url), short_code=short_code, user_id=user_id
    )

    try:
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Short code already exists"
        )

    return db_url


def url_get(user_id: int, db: Session):
    statement = select(URL).where(URL.user_id == user_id)
    return db.scalars(statement).all()


def url_delete(id: int, user_id: int, db: Session):
    statement = select(URL).where(URL.user_id == user_id, URL.id == id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    db.delete(db_url)
    db.commit()


def url_get_by_short_code(short_code: str, db: Session):
    statement = select(URL).where(URL.short_code == short_code)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    if db_url.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="URL inactive"
        )

    click_count = db_url.click_count or 0

    if db_url.click_max is not None and click_count >= db_url.click_max:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="URL click limit has been reached",
        )

    if db_url.expires_at is not None and db_url.expires_at <= datetime.now():
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="URL exipred")

    increase_click_count(db_url, db)

    return RedirectResponse(url=db_url.original_url)


def url_deactivate(id: int, user_id: int, db: Session):
    statement = select(URL).where(URL.id == id, URL.user_id == user_id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    if db_url.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="URL inactive"
        )

    db_url.is_active = False
    db.commit()
    db.refresh(db_url)

    return db_url


def url_activate(id: int, user_id: int, db: Session):
    statement = select(URL).where(URL.id == id, URL.user_id == user_id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    if db_url.is_active is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="URL inactive"
        )

    db_url.is_active = True
    db.commit()
    db.refresh(db_url)

    return db_url


def change_max_click(id: int, limit: int, db: Session):
    db_url = db.get(URL, id)

    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    db_url.click_max = limit

    db.commit()
    db.refresh(db_url)

    return db_url


def change_expire_date(id: int, expire_date: datetime, db: Session):
    db_url = db.get(URL, id)

    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )

    db_url.expires_at = expire_date

    db.commit()
    db.refresh(db_url)

    return db_url
