from fastapi import APIRouter, Depends
from .schemas import UserResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth.dependencies import require_admin
from .service import (
    user_get as user_get_service,
    user_get_by_id as user_get_by_id_service,
    user_delete as user_delete_service,
)

router = APIRouter(tags=["me"], prefix="/me")

# Only admin endpoints


@router.get("/get", response_model=list[UserResponse])
def users_get(db: Session = Depends(get_db), user=Depends(require_admin)):
    return user_get_service(db=db)


@router.get("/get/{id}", response_model=UserResponse | None)
def user_get_by_id(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return user_get_by_id_service(id=id, db=db)


@router.delete("/delete/{id}")
def user_delete(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return user_delete_service(id=id, db=db)
