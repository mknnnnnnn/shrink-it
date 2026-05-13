from random import choices
import string

from sqlalchemy.orm import Session

from .schemas import URLCreate
from .models import URL


def generate_code(length: int = 5) -> str:
    return "".join(choices(string.ascii_letters + string.digits, k=length))


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
