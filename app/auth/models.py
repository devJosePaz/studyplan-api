from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid
import datetime


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    create_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_at: Mapped[datetime]= mapped_column(DateTime, nullable=False, default=datetime.datetime, onupdate=datetime.datetime.utcnow)

    profile: Mapped["ProfileModel"] = relationship(back_populates="user", uselist=False)
    