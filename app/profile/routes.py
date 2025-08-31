# app/profile/routes.py
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from typing import List

from app.config.database import get_async_session
from app.profile.models import ProfileModel
from app.auth.models import UserModel
from app.profile import schemas

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=schemas.ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: schemas.ProfileCreate,
    db: AsyncSession = Depends(get_async_session),
):
    # 1) usuário existe?
    user = await db.get(UserModel, profile_data.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 2) já existe profile para esse user_id? (1:1 lógico)
    existing = await db.execute(select(ProfileModel).where(ProfileModel.user_id == profile_data.user_id))
    if existing.scalars().first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists for this user")

    # 3) criar
    new_profile = ProfileModel(
        user_id=profile_data.user_id,
        learning_style=getattr(profile_data.learning_style, "value", profile_data.learning_style),
        challenge_tolerance=getattr(profile_data.challenge_tolerance, "value", profile_data.challenge_tolerance),
        focus=getattr(profile_data.focus, "value", profile_data.focus),
        study_resilience=getattr(profile_data.study_resilience, "value", profile_data.study_resilience),
    )

    db.add(new_profile)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Integrity error: {str(e.orig)}")
    await db.refresh(new_profile)

    return new_profile


@router.get("/", response_model=List[schemas.ProfileResponse], status_code=status.HTTP_200_OK)
async def list_profiles(
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(ProfileModel))
    profiles = result.scalars().all()
    return profiles


@router.get("/by-user/{user_id}", response_model=schemas.ProfileResponse, status_code=status.HTTP_200_OK)
async def get_profile_by_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(ProfileModel).where(ProfileModel.user_id == user_id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found for this user")
    return profile
