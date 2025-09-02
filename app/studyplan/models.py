# app/studyplan/models.py
import uuid
import datetime
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base


class StudyPlanModel(Base):
    __tablename__ = "study_plans"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # ===== Entradas do plano =====
    theme: Mapped[str] = mapped_column(String(120), nullable=False)     # tema livre
    theme_level: Mapped[str] = mapped_column(String(20), nullable=False)  # iniciante|intermediario|avancado
    week_time: Mapped[int] = mapped_column(Integer, nullable=False)       # minutos por semana
    objective: Mapped[str] = mapped_column(String(30), nullable=False)    # prova|projeto|habito|aprendizado_profundo
    horizon_days: Mapped[int] = mapped_column(Integer, nullable=False, default=7)  # 7|14|28
    start_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)

    # ===== Derivados/calculados =====
    subtype: Mapped[str] = mapped_column(String(3), nullable=False)       # ex.: T1|P2|B3|I1
    block_duration_min: Mapped[int] = mapped_column(Integer, nullable=False)
    sessions_per_week: Mapped[int] = mapped_column(Integer, nullable=False)

    mix: Mapped[dict] = mapped_column(JSONB, nullable=False)              # {"theory_pct": 0.5, "practice_pct": 0.5}
    lanes: Mapped[list] = mapped_column(JSONB, nullable=False)            # [{"lane_id":"d1","label":"Dia 1"}, ...]
    cards: Mapped[list] = mapped_column(JSONB, nullable=False)            # lista de cards (sessões)

    create_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    # Relacionamento com usuário
    user: Mapped["UserModel"] = relationship(back_populates="study_plans")

    __table_args__ = (
        CheckConstraint(
            "theme_level IN ('iniciante','intermediario','avancado')",
            name="ck_study_plans_theme_level",
        ),
        CheckConstraint(
            "objective IN ('prova','projeto','habito','aprendizado_profundo')",
            name="ck_study_plans_objective",
        ),
        CheckConstraint(
            "horizon_days IN (7,14,28)",
            name="ck_study_plans_horizon_days",
        ),
        CheckConstraint(
            "subtype ~ '^(T|P|B|I)[1-3]$'",
            name="ck_study_plans_subtype",
        ),
        CheckConstraint(
            "week_time > 0 AND block_duration_min > 0 AND sessions_per_week > 0",
            name="ck_study_plans_positive_times",
        ),
    )
