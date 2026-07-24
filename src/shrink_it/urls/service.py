from fastapi import HTTPException
from fastapi.responses import StreamingResponse
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


def generate_qr_code(short_code: str, db: Session):
    statement = select(URL).where(URL.short_code == short_code)
    db_url = db.scalar(statement)

    img = qrcode.make(db_url.original_url)
    buffer = BytesIO()

    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, status_code=200, media_type="image/png")


def increase_click_count(url: URL, db: Session):
    url.click_count += 1
    db.commit()


def url_create(url: URLCreate, db: Session, user_id: int):
    short_code = url.short_code or generate_code()

    db_url = URL(
        original_url=str(url.original_url), short_code=short_code, user_id=user_id
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def url_get(user_id: int, db: Session):
    statement = select(URL).where(URL.user_id == user_id)
    return db.scalars(statement).all()


def url_delete(id: int, user_id: int, db: Session):
    statement = select(URL).where(URL.user_id == user_id, URL.id == id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    db.delete(db_url)
    db.commit()

    return {"message": "Success"}


def url_get_by_short_code(short_code: str, db: Session):
    statement = select(URL).where(URL.short_code == short_code)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    if db_url.is_active is False:
        raise HTTPException(status_code=400, detail="URL INACTIVE")

    if db_url.click_count is None:
        db_url.click_count = 1
    else:
        increase_click_count(db_url, db)

    if db_url.click_max is not None and db_url.click_count >= db_url.click_max:
        raise HTTPException(status_code=403, detail="UURL CLICK LIMIT HAS BEEN REACHED")

    return db_url


def url_deactivate(id: int, user_id: int, db: Session):
    statement = select(URL).where(URL.id == id, URL.user_id == user_id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    if db_url.is_active is False:
        raise HTTPException(status_code=400, detail="URL INACTIVE")

    db_url.is_active = False
    db.commit()
    db.refresh(db_url)

    return db_url


def url_activate(id: int, user_id: int, db: Session):
    statement = select(URL).where(URL.id == id, URL.user_id == user_id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    if db_url.is_active is True:
        raise HTTPException(status_code=400, detail="URL ACTIVE")

    db_url.is_active = True
    db.commit()
    db.refresh(db_url)

    return db_url


def change_max_click(id: int, limit: int, db: Session):
    db_url = db.get(URL, id)

    if db_url is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")

    db_url.click_max = limit

    db.commit()
    db.refresh(db_url)

    return db_url


def change_expire_date(id: int, expire_date: datetime, db: Session):
    db_url = db.get(URL, id)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    db_url.expires_at = expire_date

    db.commit()
    db.refresh(db_url)

    return db_url
