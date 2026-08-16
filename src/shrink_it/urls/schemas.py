from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    short_code: str | None = Field(
        default=None, min_length=3, max_length=10, pattern=r"^[a-zA-Z0-9]+$"
    )


class URLResponse(URLBase):
    id: int
    short_code: str
    created_at: datetime
    expires_at: datetime | None = None
    click_count: int
    click_max: int | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
