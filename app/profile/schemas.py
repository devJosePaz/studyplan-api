# app/profile/schemas.py
from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# ===== Enums (valores fechados, fáceis de validar e de usar na árvore) =====

class StyleEnum(str, Enum):
    teorico = "teorico"
    pratico = "pratico"
    balanceado = "balanceado"
    intensivo = "intensivo"


class LearningStyleEnum(str, Enum):
    visual = "visual"
    auditivo = "auditivo"
    leitura = "leitura"
    cinestesico = "cinestesico"


class ChallengeToleranceEnum(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


class FocusEnum(str, Enum):
    # janela de atenção
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
    style: StyleEnum                          # T/P/B/I no perfil do usuário
    learning_style: LearningStyleEnum         # VARK (preferência)
    challenge_tolerance: ChallengeToleranceEnum
    focus: FocusEnum
    study_resilience: StudyResilienceEnum


class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    style: StyleEnum
    learning_style: LearningStyleEnum
    challenge_tolerance: ChallengeToleranceEnum
    focus: FocusEnum
    study_resilience: StudyResilienceEnum

    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
