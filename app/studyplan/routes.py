from fastapi import APIRouter, Depends, HTTPException, status
from app.studyplan.models import StudyPlanModel
from app.studyplan import schemas
from app.config.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

router = APIRouter(prefix="/study_plans", tags=["Study Plans"])

@router.post("/", response_model=schemas.StudyPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_study_plan(
    study_plan_data: schemas.StudyPlanCreate,
    db: AsyncSession = Depends(get_async_session)
):
    new_study_plan = StudyPlanModel(
        theme=study_plan_data.theme,
        daily_time=study_plan_data.daily_time,
        objective=study_plan_data.objective,
        learning_style=study_plan_data.learning_style
    )

    db.add(new_study_plan)
    await db.commit()
    await db.refresh(new_study_plan)

    return new_study_plan


@router.get("/study-plans", response_model=List[schemas.StudyPlanResponse], status_code=status.HTTP_200_OK)
async def list_study_plans(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(StudyPlanModel))
    study_plans = result.scalars().all()

    return study_plans

    



    
