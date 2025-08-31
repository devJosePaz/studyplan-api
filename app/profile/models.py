# app/profile/models.py
import uuid
import datetime
from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )

    # 1:1 lógico com users (garantido por unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        index=True,
        nullable=False,
    )

    # === Campos do perfil ===
    learning_style: Mapped[str] = mapped_column(String(20), nullable=False)       # teorico|pratico|balanceado|intensivo
    challenge_tolerance: Mapped[str] = mapped_column(String(10), nullable=False)  # baixa|media|alta
    focus: Mapped[str] = mapped_column(String(10), nullable=False)                # curto|medio|longo
    study_resilience: Mapped[str] = mapped_column(String(10), nullable=False)     # baixa|media|alta

    create_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    # Lado do Profile -> User (par de back_populates com UserModel.profile)
    user: Mapped["UserModel"] = relationship(back_populates="profile")

    __table_args__ = (
        CheckConstraint(
            "learning_style IN ('teorico','pratico','balanceado','intensivo')",
            name="ck_profiles_learning_style",
        ),
        CheckConstraint(
            "challenge_tolerance IN ('baixa','media','alta')",
            name="ck_profiles_challenge_tolerance",
        ),
        CheckConstraint(
            "focus IN ('curto','medio','longo')",
            name="ck_profiles_focus",
        ),
        CheckConstraint(
            "study_resilience IN ('baixa','media','alta')",
            name="ck_profiles_study_resilience",
        ),
    )
