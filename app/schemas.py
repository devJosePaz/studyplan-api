from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any

# Auth
class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Profile in/out (tudo numérico)
class ProfileIn(BaseModel):
    estilo_aprendizado: int = Field(ge=0, le=3)
    tolerancia_dificuldade: int = Field(ge=0, le=2)
    nivel_foco: int = Field(ge=0, le=2)
    resiliencia_estudo: int = Field(ge=0, le=2)
    conhecimento_tema: int = Field(ge=0, le=2)
    tempo_semanal: int = Field(ge=1, le=200)
    objetivo_estudo: int = Field(ge=0, le=3)
    texto_livre: Optional[str] = ""

class ProfileOut(ProfileIn):
    id: int

# Plano
class PlanOut(BaseModel):
    plan_id: int
    class_id: int                 # 0..N-1 do modelo
    tipo_label: str               # ex: "T2"
    top5: List[Dict[str, float]]  # pares feat: importance
    profile_id: int

# Predição sem persistir
class PredictIn(ProfileIn):
    pass

class PredictOut(BaseModel):
    class_id: int
    tipo_label: str
    top5: List[Dict[str, float]]

# Mapas (opcional para debug/FE)
class MapsOut(BaseModel):
    estilos: Dict[int, str]
    niveis: Dict[int, str]
    conhecimento: Dict[int, str]
    objetivos: Dict[int, str]
