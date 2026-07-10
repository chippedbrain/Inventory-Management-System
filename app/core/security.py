from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.config import settings

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return hasher.hash(password[:72])

def verify_password(plain: str, hashed: str) -> bool:
    return hasher.verify(plain[:72], hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)