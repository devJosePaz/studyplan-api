from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.models import UserModel
from app.auth import schemas
from app.config.database import get_async_session
from typing import List

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    pass

@router.get("/users", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
async def list_users(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(UserModel))
    users = result.scalars.all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: users not found.")
    
    return users