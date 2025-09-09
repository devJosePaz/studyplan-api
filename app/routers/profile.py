from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Profile
from app.schemas import ProfileIn, ProfileOut, MapsOut
from app.deps import get_current_user
from app.ml.pipeline import ESTILOS_MAP, NIVEIS_MAP, CONH_MAP, OBJ_MAP

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/maps", response_model=MapsOut)
def get_maps():
    return {
        "estilos": ESTILOS_MAP,
        "niveis": NIVEIS_MAP,
        "conhecimento": CONH_MAP,
        "objetivos": OBJ_MAP
    }

@router.post("", response_model=ProfileOut)
def create_profile(payload: ProfileIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    prof = Profile(user_id=user.id, **payload.model_dump())
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return ProfileOut(id=prof.id, **payload.model_dump())

@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    prof = db.get(Profile, profile_id)
    if not prof or prof.user_id != user.id:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return ProfileOut(
        id=prof.id,
        estilo_aprendizado=prof.estilo_aprendizado,
        tolerancia_dificuldade=prof.tolerancia_dificuldade,
        nivel_foco=prof.nivel_foco,
        resiliencia_estudo=prof.resiliencia_estudo,
        conhecimento_tema=prof.conhecimento_tema,
        tempo_semanal=prof.tempo_semanal,
        objetivo_estudo=prof.objetivo_estudo,
        texto_livre=prof.texto_livre or ""
    )
