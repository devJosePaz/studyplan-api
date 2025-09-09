import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
import joblib
from pathlib import Path

# Codificação NUMÉRICA esperada na API
# (exposição de mapas para FE, se quiser)
ESTILOS_MAP = {0: "teorico", 1: "pratico", 2: "balanceado", 3: "intensivo"}
NIVEIS_MAP = {0: "baixa", 1: "media", 2: "alta"}
CONH_MAP   = {0: "iniciante", 1: "intermediario", 2: "avancado"}
OBJ_MAP    = {0: "prova", 1: "projeto", 2: "habito", 3: "aprendizado_profundo"}

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
MODEL_PATH = Path("pipeline.pkl")

def map_to_label(row):
    estilo_idx = row['estilo_aprendizado']
    tempo = int(row['tempo_semanal'])
    tol = row['tolerancia_dificuldade']
    foco = row['nivel_foco']
    res = row['resiliencia_estudo']
    conhecimento = row['conhecimento_tema']

    # base: T/P/B/I a partir do índice
    base_char = {0: 'T', 1: 'P', 2: 'B', 3: 'I'}[estilo_idx]

    # nivel baseado no tempo
    if tempo <= 3:
        nivel = 1
    elif tempo <= 8:
        nivel = 2
    else:
        nivel = 3

    adj = 0
    # baixa(0)/iniciante(0) -> -1; alta(2)/avancado(2) -> +1
    for v in [tol, foco, res, conhecimento]:
        if v == 2:
            adj += 1
        elif v == 0:
            adj -= 1

    nivel2 = max(1, min(3, nivel + adj))
    return f"{base_char}{nivel2}"

def generate_synthetic(n=1000):
    rows = []
    for _ in range(n):
        row = {
            'estilo_aprendizado': np.random.randint(0,4),
            'tolerancia_dificuldade': np.random.randint(0,3),
            'nivel_foco': np.random.randint(0,3),
            'resiliencia_estudo': np.random.randint(0,3),
            'conhecimento_tema': np.random.randint(0,3),
            'tempo_semanal': np.random.randint(1,21),
            'objetivo_estudo': np.random.randint(0,4),
            'texto_livre': ""
        }
        row['label'] = map_to_label(row)
        rows.append(row)
    return pd.DataFrame(rows)

def build_or_load_pipeline():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)

    df = generate_synthetic(1500)
    features = ['estilo_aprendizado','tolerancia_dificuldade','nivel_foco',
                'resiliencia_estudo','conhecimento_tema','tempo_semanal','objetivo_estudo']
    X = df[features].copy()

    # colunas categóricas numéricas tratadas como categóricas
    cat_cols = ['estilo_aprendizado','tolerancia_dificuldade','nivel_foco',
                'resiliencia_estudo','conhecimento_tema','objetivo_estudo']
    num_cols = ['tempo_semanal']

    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols)
        ]
    )

    le = LabelEncoder()
    y = le.fit_transform(df['label'])

    clf = DecisionTreeClassifier(criterion='gini', max_depth=6, random_state=RANDOM_SEED)
    pipe = Pipeline(steps=[
        ("pre", pre),
        ("clf", clf)
    ])
    pipe.fit(X, y)

    # salvar junto o label encoder e nomes de features para importâncias
    joblib.dump({"pipe": pipe, "label_encoder": le, "cat_cols": cat_cols, "num_cols": num_cols}, MODEL_PATH)
    return {"pipe": pipe, "label_encoder": le, "cat_cols": cat_cols, "num_cols": num_cols}

def load_pipeline():
    obj = build_or_load_pipeline()
    if isinstance(obj, dict) and "pipe" in obj:
        return obj
    return joblib.load(MODEL_PATH)

def feature_importances(pipe_obj):
    pipe = pipe_obj["pipe"]
    cat_cols = pipe_obj["cat_cols"]
    num_cols = pipe_obj["num_cols"]

    # recuperar nomes das features após OHE
    ohe = pipe.named_steps["pre"].named_transformers_["cat"]
    ohe_feats = ohe.get_feature_names_out(cat_cols)
    all_feats = list(ohe_feats) + num_cols

    importances = pipe.named_steps["clf"].feature_importances_
    pairs = sorted(zip(all_feats, importances), key=lambda x: x[1], reverse=True)
    return pairs
