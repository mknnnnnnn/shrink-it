from fastapi import HTTPException
from random import choices
import string

from sqlalchemy.orm import Session
from sqlalchemy import select

from .schemas import URLCreate
from .models import URL


def generate_code(length: int = 5) -> str:
    return "".join(choices(string.ascii_letters + string.digits, k=length))


def increase_click_count(url: URL, db: Session):
    url.click_count += 1
    db.commit()


def url_create(url: URLCreate, db: Session):
    short_code = url.short_code or generate_code()

    db_url = URL(
        original_url=str(url.original_url),
        short_code=short_code,
        expires_at=url.expires_at,
        click_max=url.click_max,
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def url_get(db: Session):
    statement = select(URL)
    return db.scalars(statement).all()


def url_get_by_short_code(short_code: str, db: Session):
    statement = select(URL).where(URL.short_code == short_code)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    if db_url.is_active is False:
        raise HTTPException(status_code=400, detail="URL INACTIVE")

    if db_url.click_max is not None and db_url.click_count >= db_url.click_max:
        raise HTTPException(status_code=403, detail="URL click limit has benn reached")

    increase_click_count(db_url, db)

    return db_url


def url_deactivate(id: int, db: Session):
    statement = select(URL).where(URL.id == id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    if db_url.is_active is False:
        raise HTTPException(status_code=400, detail="URL INACTIVE")

    db_url.is_active = False
    db.commit()
    db.refresh(db_url)

    return db_url


def url_activate(id: int, db: Session):
    statement = select(URL).where(URL.id == id)
    db_url = db.scalar(statement)

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL NOT FOUND")

    if db_url.is_active is True:
        raise HTTPException(status_code=400, detail="URL ACTIVE")

    db_url.is_active = True
    db.commit()
    db.refresh(db_url)

    return db_url


# Change click max

# Change expire date

# Delete url
