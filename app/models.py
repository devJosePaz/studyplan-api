from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    profiles = relationship("Profile", back_populates="user")
    plans = relationship("Plan", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    # valores NUMÉRICOS (0/1/2/3…)
    estilo_aprendizado: Mapped[int] = mapped_column(Integer, nullable=False)   # 0=teorico,1=pratico,2=balanceado,3=intensivo
    tolerancia_dificuldade: Mapped[int] = mapped_column(Integer, nullable=False)  # 0=baixa,1=media,2=alta
    nivel_foco: Mapped[int] = mapped_column(Integer, nullable=False)             # 0/1/2
    resiliencia_estudo: Mapped[int] = mapped_column(Integer, nullable=False)     # 0/1/2
    conhecimento_tema: Mapped[int] = mapped_column(Integer, nullable=False)      # 0=iniciante,1=intermediario,2=avancado
    tempo_semanal: Mapped[int] = mapped_column(Integer, nullable=False)          # horas
    objetivo_estudo: Mapped[int] = mapped_column(Integer, nullable=False)        # 0=prova,1=projeto,2=habito,3=aprendizado_profundo
    texto_livre: Mapped[str] = mapped_column(String(1024), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profiles")
    plan = relationship("Plan", back_populates="profile", uselist=False)

class Plan(Base):
    __tablename__ = "plans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), index=True)

    # saída NUMÉRICA
    class_id: Mapped[int] = mapped_column(Integer, index=True)  # 0..N-1 do modelo
    tipo_label: Mapped[str] = mapped_column(String(16))          # ex: "T1/B3" (para auditoria)
    importances_top5: Mapped[str] = mapped_column(String(1024))  # string simples com pares "feat:score"

    meta_json: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="plans")
    profile = relationship("Profile", back_populates="plan")
