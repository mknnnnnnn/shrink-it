from pydantic import BaseModel, HttpUrl, ConfigDict, Field
from datetime import datetime


class URLCreate(BaseModel):
    original_url: HttpUrl
    short_code: str | None = None
    expires_at: datetime | None = None
    click_max: int | None = Field(default=None, ge=1)


class URLResponse(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    created_at: datetime
    expires_at: datetime | None = None
    click_count: int | None = None
    click_max: int | None = Field(default=None, ge=1)
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
