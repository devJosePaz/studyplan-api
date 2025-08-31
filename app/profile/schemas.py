# app/profile/schemas.py
from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# ===== Enums =====

class LearningStyleEnum(str, Enum):
    teorico = "teorico"
    pratico = "pratico"
    balanceado = "balanceado"
    intensivo = "intensivo"


class ChallengeToleranceEnum(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


class FocusEnum(str, Enum):
    curto = "curto"     # ~25min base
    medio = "medio"     # ~50min base
    longo = "longo"     # ~75min base


class StudyResilienceEnum(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


# ===== Schemas =====

class ProfileCreate(BaseModel):
    user_id: UUID
    learning_style: LearningStyleEnum                # T/P/B/I (fixa o tipo de plano do usuário)
    challenge_tolerance: ChallengeToleranceEnum
    focus: FocusEnum
    study_resilience: StudyResilienceEnum


class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    learning_style: LearningStyleEnum
    challenge_tolerance: ChallengeToleranceEnum
    focus: FocusEnum
    study_resilience: StudyResilienceEnum

    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
