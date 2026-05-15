"""Score aggregated place activity signals."""

from __future__ import annotations

from typing import Any


def score_place_activity_signal(record: dict[str, Any]) -> dict[str, Any]:
    popularity = _level_score(str(record.get("popularity_level", "moderate")))
    trend = {"rising": 80.0, "stable": 55.0, "falling": 30.0}.get(str(record.get("estimated_activity_trend", "stable")), 50.0)
    confidence = float(record.get("confidence", 50) or 50)
    review = _level_score(str(record.get("review_activity_level", "moderate")))
    prominence = float(record.get("place_prominence", 0) or 0)
    category = _category_score(str(record.get("place_category", "")))
    strength = popularity * 0.20 + trend * 0.15 + category * 0.15 + confidence * 0.15 + review * 0.15 + prominence * 0.20
    urgency = min(100.0, strength + (10 if str(record.get("activity_indicator")) == "increasing" else 0))
    return {
        "mobility_signal_strength": round(strength, 2),
        "demand_relevance": round(min(100.0, strength * 0.92 + category * 0.08), 2),
        "urgency_score": round(urgency, 2),
        "interpretation": f"Aggregated place intelligence indicates {str(record.get('place_category', 'place'))} relevance at {round(strength, 1)}/100.",
    }


def _level_score(level: str) -> float:
    return {"very_high": 95.0, "high": 78.0, "moderate": 55.0, "low": 25.0}.get(level, 50.0)


def _category_score(category: str) -> float:
    return 85.0 if category in {"food_household_demand", "health_demand", "transport_demand", "water_access_pressure"} else 65.0