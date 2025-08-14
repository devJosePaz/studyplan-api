from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_async_session
from app.profile.models import ProfileModel
from app.profile import schemas
from typing import List

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=schemas.ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: schemas.ProfileCreate,
    db: AsyncSession = Depends(get_async_session)
):
    new_profile = ProfileModel(
        study_method=profile_data.study_method,
        study_daily_time=profile_data.study_daily_time,
        study_frequence=profile_data.study_frequence,
        main_motivation=profile_data.main_motivation
    )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    return new_profile

@router.get("/profiles", response_model=List[schemas.ProfileResponse], status_code=status.HTTP_200_OK)
async def list_profiles(
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(ProfileModel))
    profiles = result.scalars().all()

    return profiles

