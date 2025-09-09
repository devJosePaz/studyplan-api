from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.deps import get_current_user
from app.models import Plan, Profile
from app.schemas import PlanOut, PredictIn, PredictOut
from app.ml.pipeline import load_pipeline, feature_importances

router = APIRouter(prefix="/plan", tags=["plan"])
pipe_obj = load_pipeline()  # carregado 1x

def predict_numeric(payload: PredictIn):
    pipe = pipe_obj["pipe"]
    le = pipe_obj["label_encoder"]

    X = [{
        "estilo_aprendizado": payload.estilo_aprendizado,
        "tolerancia_dificuldade": payload.tolerancia_dificuldade,
        "nivel_foco": payload.nivel_foco,
        "resiliencia_estudo": payload.resiliencia_estudo,
        "conhecimento_tema": payload.conhecimento_tema,
        "tempo_semanal": payload.tempo_semanal,
        "objetivo_estudo": payload.objetivo_estudo
    }]
    class_id = int(pipe.predict(X)[0])
    tipo_label = str(le.inverse_transform([class_id])[0])
    # top5 importâncias
    pairs = feature_importances(pipe_obj)[:5]
    top5 = [{k: float(v)} for k, v in pairs]
    return class_id, tipo_label, top5

@router.post("/predict", response_model=PredictOut)
def only_predict(payload: PredictIn):
    class_id, tipo_label, top5 = predict_numeric(payload)
    return PredictOut(class_id=class_id, tipo_label=tipo_label, top5=top5)

@router.post("/generate/{profile_id}", response_model=PlanOut)
def generate_from_profile(profile_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    prof = db.get(Profile, profile_id)
    if not prof or prof.user_id != user.id:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    class_id, tipo_label, top5 = predict_numeric(
        PredictIn(
            estilo_aprendizado=prof.estilo_aprendizado,
            tolerancia_dificuldade=prof.tolerancia_dificuldade,
            nivel_foco=prof.nivel_foco,
            resiliencia_estudo=prof.resiliencia_estudo,
            conhecimento_tema=prof.conhecimento_tema,
            tempo_semanal=prof.tempo_semanal,
            objetivo_estudo=prof.objetivo_estudo,
            texto_livre=prof.texto_livre or ""
        )
    )

    # salva plano
    top5_str = "; ".join([f"{list(d.keys())[0]}:{list(d.values())[0]:.4f}" for d in top5])
    plan = Plan(
        user_id=user.id,
        profile_id=prof.id,
        class_id=class_id,
        tipo_label=tipo_label,
        importances_top5=top5_str,
        meta_json={}
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)

    return PlanOut(
        plan_id=plan.id,
        class_id=class_id,
        tipo_label=tipo_label,
        top5=top5,
        profile_id=prof.id
    )

@router.get("/{plan_id}", response_model=PlanOut)
def get_plan(plan_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    plan = db.get(Plan, plan_id)
    if not plan or plan.user_id != user.id:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    # reconstrói top5 como lista
    items = []
    if plan.importances_top5:
        for kv in plan.importances_top5.split(";"):
            kv = kv.strip()
            if not kv:
                continue
            k, v = kv.split(":")
            items.append({k: float(v)})

    return PlanOut(
        plan_id=plan.id,
        class_id=plan.class_id,
        tipo_label=plan.tipo_label,
        top5=items,
        profile_id=plan.profile_id
    )
