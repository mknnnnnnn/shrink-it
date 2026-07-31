from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING
from ..database import Base

from datetime import datetime

if TYPE_CHECKING:
    from ..urls.models import URL


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    urls: Mapped[list["URL"]] = relationship(
        "URL", back_populates="user", cascade="all, delete-orphan"
    )
