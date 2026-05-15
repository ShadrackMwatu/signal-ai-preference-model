"""Behavioral learning engine for collective aggregate signal intelligence."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.signal_engine.behavioral_signal_taxonomy import classify_behavioral_families, interpret_family_combination
from Behavioral_Signals_AI.storage.storage_manager import ensure_json, read_json, write_json

BEHAVIORAL_MEMORY_PATH = Path(os.getenv("SIGNAL_BEHAVIORAL_INTELLIGENCE_MEMORY", "Behavioral_Signals_AI/outputs/behavioral_intelligence_memory.json"))
DEFAULT_MEMORY = {"clusters": {}, "last_updated": None, "warnings": []}


def load_behavioral_memory(path: str | Path | None = None) -> dict[str, Any]:
    data = read_json(Path(path or BEHAVIORAL_MEMORY_PATH), DEFAULT_MEMORY.copy())
    return data if isinstance(data, dict) else DEFAULT_MEMORY.copy()


def initialize_behavioral_memory(path: str | Path | None = None) -> dict[str, Any]:
    return ensure_json(Path(path or BEHAVIORAL_MEMORY_PATH), DEFAULT_MEMORY.copy())


def update_behavioral_learning(signal: dict[str, Any], source_records: list[dict[str, Any]] | None = None, path: str | Path | None = None, count_appearance: bool = True) -> dict[str, Any]:
    """Update memory and return signal enriched with behavioral intelligence fields."""
    memory = load_behavioral_memory(path)
    clusters = memory.setdefault("clusters", {})
    now = datetime.now(UTC).isoformat()
    source_records = source_records or []
    source_topics = [str(record.get("topic", "")) for record in source_records if record.get("topic")]
    families = classify_behavioral_families(signal, source_topics)
    key = _cluster_key(signal)
    cluster = clusters.setdefault(
        key,
        {
            "signal_cluster": signal.get("semantic_cluster") or signal.get("signal_topic"),
            "behavioral_families": [],
            "first_seen": now,
            "last_seen": now,
            "appearance_count": 0,
            "source_types_seen": [],
            "counties_seen": [],
            "momentum_history": [],
            "persistence_score": 0,
            "geographic_spread_score": 0,
            "cross_source_confirmation_score": 0,
            "historical_recurrence_score": 0,
            "behavioral_intelligence_score": 0,
            "lessons_learned": [],
            "last_adaptation_note": "",
        },
    )
    cluster["last_seen"] = now
    if count_appearance:
        cluster["appearance_count"] = int(cluster.get("appearance_count", 0)) + 1
    cluster["behavioral_families"] = _merge_unique(cluster.get("behavioral_families", []), families)
    cluster["source_types_seen"] = _merge_unique(cluster.get("source_types_seen", []), _source_types(signal, source_records))
    scope = str(signal.get("geographic_scope", "Kenya-wide"))
    if scope and scope != "Kenya-wide":
        cluster["counties_seen"] = _merge_unique(cluster.get("counties_seen", []), [scope])
    cluster["momentum_history"] = _limited(cluster.get("momentum_history", []), signal.get("momentum"), limit=30)

    scores = _compute_scores(signal, cluster)
    cluster.update(scores)
    lesson = _lesson(cluster, signal)
    cluster["lessons_learned"] = _limited(cluster.get("lessons_learned", []), lesson, limit=20)
    cluster["last_adaptation_note"] = _adaptation_note(cluster, signal)
    memory["last_updated"] = now
    write_json(Path(path or BEHAVIORAL_MEMORY_PATH), memory)

    enriched = dict(signal)
    enriched.update(
        {
            "behavioral_families": cluster["behavioral_families"],
            "behavioral_intelligence_score": cluster["behavioral_intelligence_score"],
            "persistence_score": cluster["persistence_score"],
            "geographic_spread_score": cluster["geographic_spread_score"],
            "cross_source_confirmation_score": cluster["cross_source_confirmation_score"],
            "historical_recurrence_score": cluster["historical_recurrence_score"],
            "learning_note": lesson,
            "adaptation_note": cluster["last_adaptation_note"],
            "opportunity_interpretation": interpret_family_combination(cluster["behavioral_families"], enriched),
        }
    )
    adjusted_confidence = _adapt_confidence(enriched)
    enriched["confidence_score"] = adjusted_confidence
    enriched["demand_intelligence_score"] = round(min(100.0, _num(enriched.get("demand_intelligence_score"), _num(enriched.get("priority_score"), 50)) * 0.78 + cluster["behavioral_intelligence_score"] * 0.22), 1)
    enriched["opportunity_intelligence_score"] = round(min(100.0, _num(enriched.get("opportunity_intelligence_score"), _num(enriched.get("priority_score"), 50)) * 0.76 + cluster["behavioral_intelligence_score"] * 0.24), 1)
    return enriched


def _compute_scores(signal: dict[str, Any], cluster: dict[str, Any]) -> dict[str, float]:
    appearances = int(cluster.get("appearance_count", 0))
    source_count = len(cluster.get("source_types_seen", []))
    county_count = len(cluster.get("counties_seen", []))
    historical_match = signal.get("historical_pattern_match") not in {None, "No close historical pattern yet"}
    recurring_stress = any(family in cluster.get("behavioral_families", []) for family in ["Stress", "Affordability"])
    persistence = min(100.0, 18.0 + appearances * 14.0)
    source_confirmation = min(100.0, max(_num(signal.get("multi_source_confirmation_score"), 0), 25.0 + source_count * 24.0))
    spread = 45.0 if str(signal.get("geographic_scope", "Kenya-wide")) == "Kenya-wide" else min(100.0, 25.0 + county_count * 24.0)
    recurrence = min(100.0, (55.0 if historical_match else 12.0) + (appearances * 4.0) + (12.0 if recurring_stress else 0.0))
    momentum = {"Breakout": 88.0, "Rising": 72.0, "Stable": 48.0, "Declining": 25.0}.get(str(signal.get("momentum", "Stable")), 45.0)
    noise_penalty = min(28.0, _num(signal.get("noise_level"), 0) * 0.24)
    one_off_penalty = 16.0 if appearances <= 1 and source_count <= 1 else 0.0
    intelligence = persistence * 0.22 + source_confirmation * 0.22 + spread * 0.16 + recurrence * 0.18 + momentum * 0.18 - noise_penalty - one_off_penalty
    return {
        "persistence_score": round(max(0.0, min(100.0, persistence)), 1),
        "geographic_spread_score": round(max(0.0, min(100.0, spread)), 1),
        "cross_source_confirmation_score": round(max(0.0, min(100.0, source_confirmation)), 1),
        "historical_recurrence_score": round(max(0.0, min(100.0, recurrence)), 1),
        "behavioral_intelligence_score": round(max(0.0, min(100.0, intelligence)), 1),
    }


def _adapt_confidence(signal: dict[str, Any]) -> float:
    base = _num(signal.get("confidence_score"), 50)
    behavioral = _num(signal.get("behavioral_intelligence_score"), 40)
    source = _num(signal.get("cross_source_confirmation_score"), 35)
    persistence = _num(signal.get("persistence_score"), 20)
    confidence = base * 0.70 + behavioral * 0.16 + source * 0.08 + persistence * 0.06
    if behavioral < 42 and source < 50:
        confidence -= 7
    return round(max(5.0, min(98.0, confidence)), 1)


def _lesson(cluster: dict[str, Any], signal: dict[str, Any]) -> str:
    families = set(cluster.get("behavioral_families", []))
    if {"Demand", "Affordability"}.issubset(families):
        return "Demand plus affordability pressure suggests interest may be constrained by purchasing power."
    if {"Stress", "Affordability"}.issubset(families):
        return "Stress plus affordability pressure should be watched as a welfare and cost-of-living signal."
    if cluster.get("cross_source_confirmation_score", 0) >= 70:
        return "Cross-source confirmation makes this stronger than a one-off signal."
    if cluster.get("appearance_count", 0) <= 1:
        return "One-off aggregate signals remain weak until they persist or receive confirmation."
    return "Repeated aggregate behavior is strengthening the collective signal."


def _adaptation_note(cluster: dict[str, Any], signal: dict[str, Any]) -> str:
    parts = []
    if cluster.get("appearance_count", 0) > 1:
        parts.append("persistence increased")
    if len(cluster.get("source_types_seen", [])) > 1:
        parts.append("cross-source confirmation increased")
    if cluster.get("counties_seen"):
        parts.append("county spread evidence increased")
    if cluster.get("historical_recurrence_score", 0) >= 55:
        parts.append("historical recurrence increased attention")
    if not parts:
        parts.append("kept conservative because evidence is still one-off or source-limited")
    return "Behavioral scoring adapted: " + "; ".join(parts) + "."


def _source_types(signal: dict[str, Any], records: list[dict[str, Any]]) -> list[str]:
    values = [str(record.get("source_type")) for record in records if record.get("source_type")]
    if not values and signal.get("source_summary"):
        values = [part.strip() for part in str(signal.get("source_summary")).split("+") if part.strip()]
    return values or ["aggregate_public"]


def _cluster_key(signal: dict[str, Any]) -> str:
    return " ".join(str(signal.get("semantic_cluster") or signal.get("signal_topic") or "signal").lower().split())[:140]


def _merge_unique(existing: list[Any], incoming: list[Any]) -> list[str]:
    output = [str(item) for item in existing if item]
    for item in incoming:
        value = str(item)
        if value and value not in output:
            output.append(value)
    return output[-40:]


def _limited(existing: list[Any], value: Any, limit: int) -> list[Any]:
    output = list(existing or [])
    if value not in {None, ""}:
        output.append(value)
    return output[-limit:]


def _num(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default
