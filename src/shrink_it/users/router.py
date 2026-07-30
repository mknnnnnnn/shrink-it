from fastapi import APIRouter, Depends, status
from .schemas import UserResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth.dependencies import require_admin
from . import service

router = APIRouter(tags=["users"], prefix="/users")

# Only admin endpoints


@router.get("", response_model=list[UserResponse])
def users_get(db: Session = Depends(get_db), user=Depends(require_admin)):
    return service.user_get(db=db)


@router.get("/{id}", response_model=UserResponse | None)
def user_get_by_id(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return service.user_get_by_id(id=id, db=db)


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return service.user_delete(id=id, db=db)


@router.patch("/{id}/active-status/{status}", response_model=UserResponse)
def user_active_status(
    id: int, status: bool, db: Session = Depends(get_db), user=Depends(require_admin)
):
    return service.user_active_status(id=id, active_status=status, db=db)


@router.patch("/{id}/admin-status/{status}", response_model=UserResponse)
def user_admin_status(
    id: int, status: bool, db: Session = Depends(get_db), user=Depends(require_admin)
):
    return service.user_admin_status(id=id, admin_status=status, db=db)
