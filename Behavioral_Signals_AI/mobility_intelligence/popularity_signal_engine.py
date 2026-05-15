"""Generate revealed-demand signals from aggregated place activity indicators."""

from __future__ import annotations

from typing import Any

from .place_classifier import demand_category_to_signal_category


def generate_place_activity_signal(place_record: dict[str, Any]) -> dict[str, Any]:
    category = str(place_record.get("place_category", "general_place_activity"))
    prominence = float(place_record.get("place_prominence", 0) or 0)
    confidence = float(place_record.get("confidence", 50) or 50)
    review_count = float(place_record.get("review_count", 0) or 0)
    review_level = min(100.0, review_count / 10.0)
    trend = str(place_record.get("estimated_activity_trend", "stable"))
    trend_bonus = 14 if trend == "rising" else -8 if trend == "falling" else 0
    business_bonus = 8 if str(place_record.get("business_status", "")).upper() == "OPERATIONAL" else 0
    hours_bonus = 5 if str(place_record.get("opening_hours_status", "")) in {"open_now", "available"} else 0
    demand_relevance = min(100.0, prominence * 0.40 + review_level * 0.22 + confidence * 0.18 + trend_bonus + business_bonus + hours_bonus)
    opportunity_score = min(100.0, demand_relevance * 0.72 + _category_importance(category) * 0.28)
    infrastructure_pressure = min(100.0, demand_relevance * 0.55 + (20 if "pressure" in category or "transport" in category or "health" in category else 0))
    place_name = str(place_record.get("place_name", "place category"))
    signal_category = demand_category_to_signal_category(category)
    interpretation = (
        f"{place_record.get('popularity_level', 'moderate').title()} public place relevance around {place_name} "
        f"suggests {signal_category} activity and potential revealed demand pressure."
    )
    return {
        "signal_topic": f"{signal_category} place activity",
        "signal_category": signal_category,
        "mobility_place_category": category,
        "demand_category": place_record.get("demand_category") or signal_category,
        "geographic_scope": place_record.get("county") or place_record.get("region") or "Kenya-wide",
        "demand_relevance": round(demand_relevance, 2),
        "economic_activity_signal": round(prominence, 2),
        "review_count": int(place_record.get("review_count", 0) or 0),
        "rating": float(place_record.get("rating", 0) or 0),
        "revealed_preference_strength": round(min(100.0, demand_relevance * 0.8 + confidence * 0.2), 2),
        "opportunity_score": round(opportunity_score, 2),
        "infrastructure_pressure_score": round(infrastructure_pressure, 2),
        "confidence_score": round(confidence, 2),
        "momentum": "Rising" if trend == "rising" else "Declining" if trend == "falling" else "Stable",
        "source_summary": "Aggregated Google Maps ecosystem place intelligence",
        "privacy_level": "aggregated_place_intelligence_only",
        "interpretation": interpretation,
        "place_activity_reinforcement": True,
    }


def _level_score(level: str) -> float:
    return {"very_high": 95.0, "high": 78.0, "moderate": 55.0, "low": 25.0}.get(level, 50.0)


def _category_importance(category: str) -> float:
    if category in {"food_household_demand", "health_demand", "transport_demand", "water_access_pressure"}:
        return 85.0
    if category in {"financial_services_demand", "education_demand", "retail_trade_demand"}:
        return 70.0
    return 55.0