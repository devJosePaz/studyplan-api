import uuid, datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base

class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)
    study_method: Mapped[str] = mapped_column(String(50), nullable=False)
    study_frequence: Mapped[str] = mapped_column(String(50), nullable=False)
    main_motivation: Mapped[str] = mapped_column(String(80), nullable=False)

    create_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user: Mapped["UserModel"] = relationship(back_populates="profile")
    
    




