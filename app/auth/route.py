from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.models import UserModel
from app.auth import schemas, passw_utils
from app.config.database import get_async_session
from typing import List

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(UserModel).where(UserModel.email == user_data.email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: user already exists.")
    
    new_user = UserModel(
        name=user_data.name,
        email=user_data.email,
        hashed_password=passw_utils.verify_password(user_data.hashed_password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.get("/users", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
async def list_users(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: users not found.")
    
    return users