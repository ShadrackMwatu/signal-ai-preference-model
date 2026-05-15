"""Safe historical memory utilities for Behavioral Signals AI."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.storage.storage_manager import ensure_json, read_json, storage_health, write_json

HISTORICAL_MEMORY_PATH = Path(os.getenv("SIGNAL_HISTORICAL_MEMORY_PATH", "Behavioral_Signals_AI/outputs/historical_signal_memory.json"))
INSIGHT_INDEX_PATH = Path(os.getenv("SIGNAL_HISTORICAL_INSIGHT_INDEX_PATH", "Behavioral_Signals_AI/outputs/historical_insight_index.json"))
FORECAST_MEMORY_PATH = Path(os.getenv("SIGNAL_FORECAST_MEMORY_PATH", "Behavioral_Signals_AI/outputs/forecast_memory.json"))
HISTORY_ROOT = Path(os.getenv("SIGNAL_HISTORY_ROOT", "Behavioral_Signals_AI/history"))


def load_json(path: str | Path, default: Any) -> Any:
    return read_json(path, default)


def initialize_history_stores() -> None:
    for folder in [HISTORY_ROOT / "daily", HISTORY_ROOT / "monthly", HISTORY_ROOT / "yearly"]:
        folder.mkdir(parents=True, exist_ok=True)
    for path, default in [
        (HISTORICAL_MEMORY_PATH, {"records": [], "last_updated": None, "warnings": []}),
        (INSIGHT_INDEX_PATH, {"themes": {}, "counties": {}, "categories": {}, "lessons": [], "last_updated": None}),
        (FORECAST_MEMORY_PATH, {"forecasts": [], "last_updated": None}),
    ]:
        ensure_json(path, default)


def get_historical_storage_health() -> dict[str, Any]:
    return storage_health({"memory": HISTORICAL_MEMORY_PATH, "history": INSIGHT_INDEX_PATH, "forecast": FORECAST_MEMORY_PATH})


def update_historical_memory(signals: list[dict[str, Any]], period: str = "daily") -> dict[str, Any]:
    initialize_history_stores()
    payload = read_json(HISTORICAL_MEMORY_PATH, {"records": [], "last_updated": None, "warnings": []})
    records = list(payload.get("records", [])) if isinstance(payload, dict) else []
    now = datetime.now(UTC).isoformat()
    for signal in signals:
        records.append(to_historical_record(signal, period=period, date=now[:10]))
    payload = {"records": records[-3000:], "last_updated": now, "warnings": []}
    write_json(HISTORICAL_MEMORY_PATH, payload)
    update_insight_index(payload["records"])
    return payload


def update_insight_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    index = {"themes": {}, "counties": {}, "categories": {}, "lessons": [], "last_updated": datetime.now(UTC).isoformat()}
    for record in records:
        _bump(index["themes"], str(record.get("signal_cluster") or record.get("signal_topic") or "unknown"))
        _bump(index["counties"], str(record.get("county_or_scope") or "Kenya-wide"))
        _bump(index["categories"], str(record.get("category") or "other"))
        lesson = record.get("lessons_learned")
        if lesson:
            index["lessons"].append(str(lesson))
    index["lessons"] = index["lessons"][-50:]
    write_json(INSIGHT_INDEX_PATH, index)
    return index


def append_forecast_memory(signals: list[dict[str, Any]]) -> dict[str, Any]:
    initialize_history_stores()
    payload = read_json(FORECAST_MEMORY_PATH, {"forecasts": [], "last_updated": None})
    forecasts = list(payload.get("forecasts", [])) if isinstance(payload, dict) else []
    now = datetime.now(UTC).isoformat()
    for signal in signals:
        forecasts.append(
            {
                "timestamp": now,
                "signal_topic": signal.get("signal_topic"),
                "signal_cluster": signal.get("semantic_cluster"),
                "category": signal.get("signal_category"),
                "county_or_scope": signal.get("geographic_scope"),
                "forecast_direction": signal.get("forecast_direction") or signal.get("predicted_direction"),
                "forecast_confidence": signal.get("forecast_confidence"),
                "likely_next_development": signal.get("likely_next_development"),
                "historical_lesson_used": signal.get("historical_lesson_used"),
            }
        )
    payload = {"forecasts": forecasts[-1500:], "last_updated": now}
    write_json(FORECAST_MEMORY_PATH, payload)
    return payload


def to_historical_record(signal: dict[str, Any], period: str, date: str) -> dict[str, Any]:
    return {
        "period": period,
        "date": date,
        "signal_topic": signal.get("signal_topic"),
        "signal_cluster": signal.get("semantic_cluster") or signal.get("signal_topic"),
        "category": signal.get("signal_category"),
        "county_or_scope": signal.get("geographic_scope"),
        "demand_intelligence_score": _num(signal.get("demand_intelligence_score"), 0),
        "opportunity_intelligence_score": _num(signal.get("opportunity_intelligence_score"), 0),
        "urgency_score": _num(signal.get("urgency_score"), 0),
        "confidence_score": _num(signal.get("confidence_score"), 0),
        "momentum_label": signal.get("momentum"),
        "validation_status": signal.get("validation_status", "unvalidated"),
        "actual_outcome_if_known": signal.get("actual_outcome_if_known", "unknown"),
        "lessons_learned": signal.get("historical_lesson_used") or signal.get("confidence_reasoning") or "Historical evidence is accumulating.",
        "future_relevance": _future_relevance(signal),
    }


def _future_relevance(signal: dict[str, Any]) -> str:
    score = _num(signal.get("confidence_score"), 0) * 0.4 + _num(signal.get("urgency_score"), 0) * 0.35 + _num(signal.get("opportunity_intelligence_score"), 0) * 0.25
    if score >= 72:
        return "High"
    if score >= 48:
        return "Moderate"
    return "Low"


def _bump(bucket: dict[str, int], key: str) -> None:
    if not key:
        key = "unknown"
    bucket[key] = int(bucket.get(key, 0)) + 1


def _num(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default
