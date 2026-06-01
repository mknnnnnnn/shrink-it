from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from .service import (
    url_create as url_create_service,
    url_get_by_short_code as url_get_by_short_code_service,
    url_get as url_get_service,
    url_deactivate as url_deactivate_service,
    url_activate as url_activate_service,
    change_max_click as change_max_click_service,
    change_expire_date as change_expire_date_service,
    url_delete as url_delete_service,
    generate_qr_code as generate_qr_code_service,
)
from .schemas import *
from ..database import get_db
from ..auth.dependencies import get_current_user, require_admin

router = APIRouter(tags=["urls"], prefix="/urls")


@router.get("/qr")
def generate_qr_code(short_code: str):
    return generate_qr_code_service(short_code=short_code)


@router.post("/create")
def create_url(
    url: URLCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return url_create_service(url=url, db=db)


@router.get("/get", response_model=list[URLResponse])
def get_url(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return url_get_service(db=db)


@router.get("/{short_code}", response_model=URLResponse)
def get_url_by_short_code(
    short_code: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return url_get_by_short_code_service(short_code=short_code, db=db)


@router.patch("/deactivate/{id}", response_model=URLResponse)
def url_deactivate(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return url_deactivate_service(id=id, db=db)


@router.patch("/activate/{id}", response_model=URLResponse)
def url_activate(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return url_activate_service(id=id, db=db)


@router.delete("/delete/{id}")
def url_delete(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return url_delete_service(id=id, db=db)


# Only admin endpoints


@router.patch("/max_click/{id}/{limit}", response_model=URLResponse)
def change_max_click(
    id: int, limit: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    return change_max_click_service(id=id, limit=limit, db=db)


@router.patch(
    "/expire_date/{id}/{expire_date}",
    response_model=URLResponse,
)
def change_expire_date(
    id: int,
    expire_date: datetime,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return change_expire_date_service(id=id, expire_date=expire_date, db=db)
