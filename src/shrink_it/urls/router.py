from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from . import service
from .schemas import *
from ..database import get_db
from ..auth.dependencies import get_current_user, require_admin

router = APIRouter(tags=["urls"], prefix="/urls")


@router.post("")
def create_url(
    url: URLCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.url_create(url=url, db=db, user_id=user.id)


@router.get("", response_model=list[URLResponse])
def get_url(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service.url_get(user_id=user.id, db=db)


@router.get("/qr")
def generate_qr_code(
    short_code: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.generate_qr_code(short_code=short_code, user_id=user.id, db=db)


@router.get("/code/{short_code}", response_model=URLResponse)
def get_url_by_short_code(
    short_code: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.url_get_by_short_code(short_code=short_code, user_id=user.id, db=db)


@router.patch("/{id}/deactivate", response_model=URLResponse)
def url_deactivate(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.url_deactivate(id=id, user_id=user.id, db=db)


@router.patch("/{id}/activate", response_model=URLResponse)
def url_activate(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.url_activate(id=id, user_id=user.id, db=db)


@router.delete("/{id}")
def url_delete(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service.url_delete(id=id, user_id=user.id, db=db)


# Only admin endpoints


@router.patch("/{id}/max-clicks/{limit}", response_model=URLResponse)
def change_max_click(
    id: int, limit: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    return service.change_max_click(id=id, limit=limit, db=db)


@router.patch(
    "/{id}/expire-date/{expire_date}",
    response_model=URLResponse,
)
def change_expire_date(
    id: int,
    expire_date: datetime,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return service.change_expire_date(id=id, expire_date=expire_date, db=db)
