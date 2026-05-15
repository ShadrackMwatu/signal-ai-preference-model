"""Normalize aggregate source records into the Behavioral Signals AI backend schema."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.privacy import sanitize_aggregate_record


def _score(value: Any, default: float = 50.0) -> float:
    try:
        if value is None:
            return default
        number = float(value)
        if 0 <= number <= 1:
            number *= 100
        return max(0.0, min(100.0, number))
    except Exception:
        return default


def normalize_source_record(record: dict[str, Any]) -> dict[str, Any]:
    safe = sanitize_aggregate_record(record)
    topic = safe.get("topic") or safe.get("signal_name") or safe.get("trend_name") or safe.get("query") or "Kenya demand signal"
    category = safe.get("category") or "other"
    return {
        "topic": str(topic),
        "source_type": str(safe.get("source_type") or safe.get("provider_type") or "aggregate_public"),
        "location": str(safe.get("location") or "Kenya"),
        "category": str(category).replace("_", " "),
        "relative_interest": _score(safe.get("relative_interest") or safe.get("volume") or safe.get("search_intensity")),
        "engagement_signal": _score(safe.get("engagement_signal") or safe.get("engagement_velocity") or safe.get("demand_relevance")),
        "growth_signal": _score(safe.get("growth_signal") or (75 if str(safe.get("growth", "")).lower() in {"rising", "breakout"} else 45)),
        "sentiment_signal": max(-1.0, min(1.0, float(safe.get("sentiment") or safe.get("sentiment_signal") or 0.0))),
        "timestamp": str(safe.get("timestamp") or safe.get("fetched_at") or datetime.now(UTC).isoformat()),
        "privacy_level": "aggregate_public",
    }