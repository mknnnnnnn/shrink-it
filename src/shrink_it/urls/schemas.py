from pydantic import BaseModel, HttpUrl, ConfigDict, Field
from datetime import datetime


class URLCreate(BaseModel):
    original_url: HttpUrl
    short_code: str | None = None


class URLResponse(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str = Field(default=None, min_length=3, max_length=10)
    created_at: datetime
    expires_at: datetime | None = None
    click_count: int | None = None
    click_max: int | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
