from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..auth.dependencies import get_current_user, require_admin
from ..database import get_db
from . import service
from .schemas import UpdateUser, UpdateUserPassword, UserResponse

router = APIRouter(tags=["users"], prefix="/users")

# User endpoints


@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def update_password(
    password: UpdateUserPassword,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.update_password(id=user.id, password=password, db=db)


# Admin endpoints


@router.get("", response_model=list[UserResponse])
def users_get(db: Session = Depends(get_db), user=Depends(require_admin)):
    return service.user_get(db=db)


@router.get("/{id}", response_model=UserResponse)
def user_get_by_id(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return service.user_get_by_id(id=id, db=db)


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


@router.patch("/{id}", response_model=UserResponse)
def update_user(
    id: int,
    user: UpdateUser,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return service.user_update(id=id, user=user, db=db)


@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    service.user_delete(id=id, db=db)
