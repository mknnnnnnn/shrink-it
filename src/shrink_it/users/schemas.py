from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)
    email: EmailStr
    phone_number: str | None = Field(default=None, pattern=r"^\+?[1-9][0-9]+$")


class UpdateUser(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=20)
    last_name: str | None = Field(default=None, min_length=1, max_length=20)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, pattern=r"^\+?[1-9][0-9]+$")


class UpdateUserPassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class UserRegister(UserBase):
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
