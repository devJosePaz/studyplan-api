from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: str, expires_data: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_data
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt






