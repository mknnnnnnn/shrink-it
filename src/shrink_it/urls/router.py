from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .service import (
    url_create as url_create_service,
    url_get_by_short_code as url_get_by_short_code_service,
    url_get as url_get_service,
    url_deactivate as url_deactivate_service,
    url_activate as url_activate_service,
    change_max_click as change_max_click_service,
    change_expire_date as change_expire_date_service,
    url_delete as url_delete_service,
)
from .schemas import *
from ..database import get_db

router = APIRouter(tags=["urls"], prefix="/urls")


@router.post("/create")
def create_url(url: URLCreate, db: Session = Depends(get_db)):
    return url_create_service(url=url, db=db)


@router.get("/get", response_model=list[URLResponse])
def get_url(db: Session = Depends(get_db)):
    return url_get_service(db=db)


@router.get("/{short_code}", response_model=URLResponse)
def get_url_by_short_code(shore_code: str, db: Session = Depends(get_db)):
    return url_get_by_short_code_service(short_code=shore_code, db=db)


@router.delete("/delete/{id}")
def url_delete(id: int, db: Session = Depends(get_db)):
    return url_delete_service(id=id, db=db)


@router.patch("/deactivate/{id}", response_model=URLResponse)
def url_deactivate(id: int, db: Session = Depends(get_db)):
    return url_deactivate_service(id=id, db=db)


@router.patch("/activate/{id}", response_model=URLResponse)
def url_activate(id: int, db: Session = Depends(get_db)):
    return url_activate_service(id=id, db=db)


@router.patch("/max_click/{id}/{limit}", response_model=URLResponse)
def change_max_click(id: int, limit: int, db: Session = Depends(get_db)):
    return change_max_click_service(id=id, limit=limit, db=db)


@router.patch("/expire_date/{id}/{expire_date}", response_model=URLResponse)
def change_expire_date(id: int, expire_date: datetime, db: Session = Depends(get_db)):
    return change_expire_date_service(id=id, expire_date=expire_date, db=db)
