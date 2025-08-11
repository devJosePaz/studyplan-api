import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class StudyPlanModel(Base):
    __tablename__ = "study_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4)
    theme: Mapped[str] = mapped_column(String(80), nullable=False)
    daily_time: Mapped[int] = mapped_column(Integer, nullable=False)
    objective: Mapped[str] = mapped_column(String(80), nullable=False)
    learning_style: Mapped[str] = mapped_column(String(80), nullable=False)
    

