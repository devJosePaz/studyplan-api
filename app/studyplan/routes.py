# app/studyplan/routes.py
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.config.database import get_async_session
from app.studyplan.models import StudyPlanModel
from app.studyplan import schemas
from app.auth.models import UserModel

router = APIRouter(prefix="/study_plans", tags=["Study Plans"])


@router.post("/", response_model=schemas.StudyPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_study_plan(
    study_plan_data: schemas.StudyPlanCreate,
    user_id: UUID = Query(..., description="User ID (MVP)"),
    db: AsyncSession = Depends(get_async_session),
):
    # valida usuário
    user = await db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # cria somente os campos declarados no modelo (sem geração de estrutura aqui)
    new_plan = StudyPlanModel(
        user_id=user_id,
        theme=study_plan_data.theme,
        theme_level=getattr(study_plan_data, "theme_level", None),
        week_time=study_plan_data.week_time,
        objective=study_plan_data.objective,
        # se seu modelo tiver estes campos (opcional no MVP):
        horizon_days=getattr(study_plan_data, "horizon_days", 7) if hasattr(StudyPlanModel, "horizon_days") else None,
        start_date=getattr(study_plan_data, "start_date", None) if hasattr(StudyPlanModel, "start_date") else None,
    )

    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan


@router.get("/", response_model=List[schemas.StudyPlanResponse], status_code=status.HTTP_200_OK)
async def list_study_plans(
    db: AsyncSession = Depends(get_async_session),
    user_id: UUID | None = Query(None, description="Opcional: filtrar por usuário"),
):
    qry = select(StudyPlanModel)
    if user_id:
        qry = qry.where(StudyPlanModel.user_id == user_id)

    result = await db.execute(qry)
    plans = result.scalars().all()
    return plans


@router.get("/{plan_id}", response_model=schemas.StudyPlanResponse, status_code=status.HTTP_200_OK)
async def get_study_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    plan = await db.get(StudyPlanModel, plan_id)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study plan not found")
    return plan
