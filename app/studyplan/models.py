import uuid, datetime
from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

class StudyPlanModel(Base):
    __tablename__ = "study_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    theme: Mapped[str] = mapped_column(String(80), nullable=False) # tema de estudo
    theme_level: Mapped[str] = mapped_column(String(80), nullable=False) # iniciante, intermediário, avançado
    week_time: Mapped[int] = mapped_column(Integer, nullable=False) # hora por semana (mostra o ritmo)
    objective: Mapped[str] = mapped_column(String(80), nullable=False) # aprimoramento, revisão, certificação, projeto, competição
    
    create_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    user: Mapped["UserModel"] = relationship(back_populates="study_plans")

1