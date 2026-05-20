from pydantic import BaseModel, HttpUrl


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    email: HttpUrl
