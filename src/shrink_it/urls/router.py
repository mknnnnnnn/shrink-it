from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .service import url_create as url_create_service
from .schemas import *
from ..database import get_db

router = APIRouter(tags=["urls"], prefix="/urls")


@router.post("/create")
def create_url(url: URLCreate, db: Session = Depends(get_db)):
    return url_create_service(url=url, db=db)
