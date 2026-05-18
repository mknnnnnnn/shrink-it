from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ..database import Base
from ..urls.models import URL
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    phone_number: Mapped[str | None] = mapped_column(
        String, nullable=True, default=None, unique=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    urls: Mapped[list["URL"]] = relationship(
        "URL", back_populates="user", cascade="all, delete-orphan"
    )
