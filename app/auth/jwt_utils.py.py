from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config.settings import settings

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.config.database import get_async_session
from app.auth import models, schemas
from config import settings

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        expire_timestamp = payload.get("exp")
        if expire_timestamp:
            expire_datetime = datetime.fromtimestamp(expire_timestamp, tz=timezone.utc)
            if expire_datetime < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expirado",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        token_data = schemas.TokenData(email=email) 
    except JWTError:
        raise credentials_exception

    user = db.query(models.UserModel).filter(models.UserModel.email == token_data.email).first()
    if user is None:
        raise credentials_exception

    return user
