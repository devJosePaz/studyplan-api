from enum import Enum
from typing import List, Optional, Literal
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, Field

# Reaproveita o enum do perfil (learning_style = teorico|pratico|balanceado|intensivo)
from app.profile.schemas import LearningStyleEnum


# ===== Enums do plano =====

class ThemeLevelEnum(str, Enum):
    iniciante = "iniciante"
    intermediario = "intermediario"
    avancado = "avancado"


class ObjectiveEnum(str, Enum):
    prova = "prova"
    projeto = "projeto"
    habito = "habito"
    aprendizado_profundo = "aprendizado_profundo"


class DensityEnum(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


KindLiteral = Literal["teoria", "pratica"]


# ===== Estruturas do Kanban (drag-and-go) =====

class PlanMix(BaseModel):
    theory_pct: float = Field(..., ge=0.0, le=1.0)
    practice_pct: float = Field(..., ge=0.0, le=1.0)


class Lane(BaseModel):
    lane_id: str
    label: str


class Card(BaseModel):
    card_id: str
    lane_id: str
    date: Optional[date] = None          # opcional; front pode só usar lanes
    start_time: Optional[str] = None     # "HH:MM" opcional
    duration_min: int
    kind: KindLiteral                    # "teoria" | "pratica"
    density_level: DensityEnum
    theme: str
    theme_level: ThemeLevelEnum
    objective: ObjectiveEnum
    # Hints para o ChatGPT preencher conteúdo (título, checklist, recursos, etc.)
    composition_hints: Optional[dict] = None


# ===== Schemas de entrada/saída =====

class StudyPlanCreate(BaseModel):
    theme: str
    theme_level: ThemeLevelEnum
    week_time: int = Field(..., ge=1)            # minutos/semana
    objective: ObjectiveEnum
    horizon_days: int = Field(7, ge=1, le=28)    # 7|14|28
    start_date: Optional[date] = None            # se None, backend decide


class StudyPlanResponse(BaseModel):
    id: UUID
    user_id: UUID

    # herdado do perfil do usuário (fixa T/P/B/I)
    learning_style: LearningStyleEnum            # teorico|pratico|balanceado|intensivo
    subtype: str                                 # ex.: "T1", "P2", "B3", "I1"

    # entradas do plano
    theme: str
    theme_level: ThemeLevelEnum
    week_time: int
    objective: ObjectiveEnum
    horizon_days: int
    start_date: Optional[date] = None

    # cálculo/estrutura
    block_duration_min: int
    sessions_per_week: int
    mix: PlanMix
    lanes: List[Lane]
    cards: List[Card]

    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
