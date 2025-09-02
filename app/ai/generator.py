from __future__ import annotations
from datetime import date, timedelta
from math import ceil
from typing import Dict, List, Tuple, Optional

# -------- Helpers de regra determinística (baseline explicável) --------

def _clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))

def _block_duration_min(learning_style: str, focus: str, challenge_tolerance: str) -> int:
    # base por janela de atenção
    base = {"curto": 25, "medio": 50, "longo": 75}.get(focus, 50)
    # ajuste por tolerância a desafio
    if challenge_tolerance == "alta":
        base += 10
    elif challenge_tolerance == "baixa":
        base -= 10
    # ajuste leve pelo estilo (T/P/B/I)
    style_adj = {"teorico": -5, "pratico": +5, "balanceado": 0, "intensivo": +10}.get(learning_style, 0)
    return _clamp(base + style_adj, 25, 90)

def _sessions_per_week(week_time: int, block_min: int) -> int:
    return max(1, round(week_time / max(1, block_min)))

def _level_from_sessions(n: int) -> Tuple[int, str]:
    if n <= 3:
        return 1, "baixa"
    if n <= 6:
        return 2, "media"
    return 3, "alta"

def _letter_for_style(style: str) -> str:
    return {"teorico": "T", "pratico": "P", "balanceado": "B", "intensivo": "I"}.get(style, "B")

def _mix_for_style(style: str) -> Dict[str, float]:
    if style == "teorico":
        return {"theory_pct": 1.0, "practice_pct": 0.0}
    if style == "pratico":
        return {"theory_pct": 0.0, "practice_pct": 1.0}
    if style == "intensivo":
        return {"theory_pct": 0.3, "practice_pct": 0.7}
    return {"theory_pct": 0.5, "practice_pct": 0.5}  # balanceado

def _build_lanes(horizon_days: int) -> List[Dict]:
    return [{"lane_id": f"d{i+1}", "label": f"Dia {i+1}"} for i in range(horizon_days)]

def _composition_hints() -> Dict:
    return {
        "language": "pt-BR",
        "audience_level": "auto",
        "pratica": {
            "level_1": "Gerar 1 exercício guiado curto com passos claros e output esperado.",
            "level_2": "Gerar 1 exercício aplicado + 1 desafio curto.",
            "level_3": "Gerar 1 mini-projeto com marcos e critérios de aceite.",
        },
        "teoria": {
            "level_1": "Gerar 1 tópico com leitura indicada e 3 bullets de síntese.",
            "level_2": "Gerar 1–2 tópicos + 5 bullets de síntese.",
            "level_3": "Gerar 2 tópicos + 1 quiz curto (5 perguntas).",
        },
    }

def _allocate_kinds_per_week(n: int, mix: Dict[str, float]) -> List[str]:
    t = round(n * float(mix["theory_pct"]))
    p = max(0, n - t)
    kinds = ["teoria"] * t + ["pratica"] * p
    # alterna para ficar agradável quando 50/50 (começa com prática)
    kinds.sort(key=lambda k: 0 if k == "pratica" else 1)
    return kinds

def _build_cards(
    n_per_week: int,
    weeks: int,
    start: date,
    horizon_days: int,
    mix: Dict[str, float],
    density_label: str,
    duration_min: int,
    theme: str,
    theme_level: str,
    objective: str,
) -> List[Dict]:
    cards: List[Dict] = []
    hints = _composition_hints()

    for w in range(weeks):
        week_start = start + timedelta(days=w * 7)
        kinds = _allocate_kinds_per_week(n_per_week, mix)
        # espaçar em dias alternados
        day_offsets = list(range(0, 7, max(1, 7 // max(1, n_per_week))))[:n_per_week]
        for i, kind in enumerate(kinds):
            card_index = len(cards) + 1
            day_offset = day_offsets[i] if i < len(day_offsets) else (i % 7)
            card_date = week_start + timedelta(days=day_offset)
            # respeita horizonte
            if (card_date - start).days >= horizon_days:
                break
            cards.append({
                "card_id": f"c{card_index}",
                "lane_id": f"d{(card_date - start).days + 1}",
                "date": card_date,
                "start_time": None,
                "duration_min": duration_min,
                "kind": kind,
                "density_level": density_label,   # baixa|media|alta
                "theme": theme,
                "theme_level": theme_level,
                "objective": objective,
                "composition_hints": hints,
            })
    return cards

# --------- Função pública: gera a ESTRUTURA (sem salvar em DB) ---------

def build_study_plan_structure(
    profile: Dict[str, str],
    plan_inputs: Dict[str, object],
) -> Dict[str, object]:
    """
    profile: {
      'learning_style': 'teorico|pratico|balanceado|intensivo',
      'focus': 'curto|medio|longo',
      'challenge_tolerance': 'baixa|media|alta',
      'study_resilience': 'baixa|media|alta'
    }
    plan_inputs: {
      'theme': str,
      'theme_level': 'iniciante|intermediario|avancado',
      'week_time': int,
      'objective': 'prova|projeto|habito|aprendizado_profundo',
      'horizon_days': int (opcional, default 7),
      'start_date': date (opcional, default hoje)
    }
    """
    learning_style = str(profile["learning_style"])
    focus = str(profile["focus"])
    challenge_tolerance = str(profile["challenge_tolerance"])
    study_resilience = str(profile["study_resilience"])

    theme = str(plan_inputs["theme"])
    theme_level = str(plan_inputs["theme_level"])
    week_time = int(plan_inputs["week_time"])
    objective = str(plan_inputs["objective"])
    horizon_days = int(plan_inputs.get("horizon_days", 7))
    start = plan_inputs.get("start_date") or date.today()

    # 1) bloco, sessões e nível
    block = _block_duration_min(learning_style, focus, challenge_tolerance)
    n = _sessions_per_week(week_time, block)
    level, density_label = _level_from_sessions(n)

    # caps simples
    if theme_level == "iniciante" and level > 2:
        level, density_label = 2, "media"
    if objective == "habito" and level > 2:
        level, density_label = 2, "media"

    # 2) subtipo e mix
    subtype = f"{_letter_for_style(learning_style)}{level}"
    mix = _mix_for_style(learning_style)

    # 3) lanes/cards
    weeks = ceil(horizon_days / 7)
    lanes = _build_lanes(horizon_days)
    cards = _build_cards(
        n_per_week=n,
        weeks=weeks,
        start=start,
        horizon_days=horizon_days,
        mix=mix,
        density_label=density_label,
        duration_min=block,
        theme=theme,
        theme_level=theme_level,
        objective=objective,
    )

    return {
        "subtype": subtype,
        "block_duration_min": block,
        "sessions_per_week": n,
        "mix": mix,
        "lanes": lanes,
        "cards": cards,
        # metadados que o caller pode querer
        "learning_style": learning_style,
        "horizon_days": horizon_days,
        "start_date": start,
    }
