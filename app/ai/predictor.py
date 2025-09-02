import pathlib
import joblib
import numpy as np

_MODEL_PATH = pathlib.Path(__file__).resolve().parent.parent / "models" / "decision_tree.pkl"
_model = None
_encoder = None  # se usar pipeline, não precisa

def _load():
    global _model
    if _model is None:
        _model = joblib.load(_MODEL_PATH)
    return _model

def _to_features(profile: dict, plan: dict) -> dict:
    # features simples (nominais + numérica)
    return {
        "learning_style": profile["learning_style"],              # teorico|pratico|balanceado|intensivo
        "focus": profile["focus"],                                # curto|medio|longo
        "challenge_tolerance": profile["challenge_tolerance"],    # baixa|media|alta
        "study_resilience": profile["study_resilience"],          # baixa|media|alta
        "theme_level": plan["theme_level"],                       # iniciante|intermediario|avancado
        "objective": plan["objective"],                           # prova|projeto|habito|aprendizado_profundo
        "week_time": int(plan["week_time"]),                      # numérica
    }

def predict_level(profile: dict, plan: dict) -> int:
    """
    Retorna 1, 2 ou 3. Se o modelo não estiver disponível, opcionalmente
    você pode cair no baseline (regras) — aqui eu levanto erro para deixar explícito.
    """
    model = _load()
    x = _to_features(profile, plan)
    # Se treinou com Pipeline (OneHot + Árvores), pode passar dict direto (sklearn >=1.3 com pandas dict->DataFrame)
    # Para ficar robusto a versões, convertamos para vetor ordenado:
    order = ["learning_style","focus","challenge_tolerance","study_resilience","theme_level","objective","week_time"]
    row = [[x[k] for k in order]]
    y_hat = model.predict(row)[0]
    return int(y_hat)
