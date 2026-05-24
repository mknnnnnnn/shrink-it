from ..config import ALGORITHM, SECRET, ACCESS_TOKEN_EXPIRE
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=[ALGORITHM])

    return encoded_jwt

def decode_token(token: str):
    try:
        decoded_jwt = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return decoded_jwt
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
