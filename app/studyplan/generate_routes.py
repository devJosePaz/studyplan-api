from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_async_session
from app.studyplan.models import StudyPlanModel
from app.profile.models import ProfileModel
from app.ai.predictor import predict_level
from app.ai.generator import build_study_plan_structure

router = APIRouter(prefix="/study_plans", tags=["Study Plans - Generate"])

@router.post("/{plan_id}/generate", status_code=status.HTTP_200_OK)
async def generate_plan(plan_id: UUID, db: AsyncSession = Depends(get_async_session)):
    plan = await db.get(StudyPlanModel, plan_id)
    if not plan:
        raise HTTPException(404, "Study plan not found")

    res = await db.execute(select(ProfileModel).where(ProfileModel.user_id == plan.user_id))
    profile = res.scalars().first()
    if not profile:
        raise HTTPException(400, "Profile not found for this user")

    prof_dict = {
        "learning_style": profile.learning_style,
        "focus": profile.focus,
        "challenge_tolerance": profile.challenge_tolerance,
        "study_resilience": profile.study_resilience,
    }
    plan_inputs = {
        "theme": plan.theme,
        "theme_level": plan.theme_level,
        "week_time": plan.week_time,
        "objective": plan.objective,
        "horizon_days": getattr(plan, "horizon_days", 7),
        "start_date": getattr(plan, "start_date", None),
    }

    try:
        level = predict_level(prof_dict, plan_inputs)     # ML AQUI
    except Exception:
        # fallback: pode usar baseline direto se preferir
        from app.ai.generator import build_study_plan_structure
        result = build_study_plan_structure(prof_dict, plan_inputs)
    else:
        result = build_study_plan_structure(prof_dict, plan_inputs)
        # sobrescreve nível pela previsão
        result["subtype"] = result["subtype"][0] + str(level)

    # atualiza registro
    plan.subtype = result["subtype"]
    plan.block_duration_min = result["block_duration_min"]
    plan.sessions_per_week = result["sessions_per_week"]
    plan.mix = result["mix"]
    plan.lanes = result["lanes"]
    plan.cards = result["cards"]

    await db.commit()
    await db.refresh(plan)
    return plan
