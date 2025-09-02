import itertools, random, pathlib, joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from app.ai.generator import build_study_plan_structure  # usa baseline p/ rotular

# Espaços de valores (iguais aos enums)
LEARNING_STYLES = ["teorico","pratico","balanceado","intensivo"]
FOCUS = ["curto","medio","longo"]
CHALL = ["baixa","media","alta"]
RESIL = ["baixa","media","alta"]
THEME_LEVEL = ["iniciante","intermediario","avancado"]
OBJECTIVE = ["prova","projeto","habito","aprendizado_profundo"]

def synth_samples(n=5000):
    rows = []
    for _ in range(n):
        profile = {
            "learning_style": random.choice(LEARNING_STYLES),
            "focus": random.choice(FOCUS),
            "challenge_tolerance": random.choice(CHALL),
            "study_resilience": random.choice(RESIL),
        }
        plan = {
            "theme": "placeholder",
            "theme_level": random.choice(THEME_LEVEL),
            "week_time": random.choice([30,60,90,120,150,180,240,300,360]),
            "objective": random.choice(OBJECTIVE),
            "horizon_days": 7,
        }
        # Usa baseline para rotular o 'level'
        st = build_study_plan_structure(profile, plan)
        level = int(st["subtype"][1])  # 'T1' -> 1
        row = {**profile, **{k:v for k,v in plan.items() if k!="theme"}, "level": level}
        rows.append(row)
    return pd.DataFrame(rows)

def main():
    df = synth_samples(5000)
    X = df.drop(columns=["level"])
    y = df["level"]

    cat_cols = ["learning_style","focus","challenge_tolerance","study_resilience","theme_level","objective"]
    num_cols = ["week_time"]

    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols)
    ])

    clf = DecisionTreeClassifier(
        max_depth=6, min_samples_leaf=20, random_state=42
    )

    pipe = Pipeline([("pre", pre), ("clf", clf)])

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipe.fit(Xtr, ytr)
    acc = pipe.score(Xte, yte)
    print(f"Accuracy vs baseline policy: {acc:.3f}")

    out = pathlib.Path(__file__).resolve().parents[1] / "models" / "decision_tree.pkl"
    out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out)
    print(f"Saved model to {out}")

if __name__ == "__main__":
    main()
