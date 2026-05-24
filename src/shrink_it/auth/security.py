from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ..config import ALGORITHM, SECRET, ACCESS_TOKEN_EXPIRE
from jose import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET, ALGORITHM)

    return encoded_jwt

