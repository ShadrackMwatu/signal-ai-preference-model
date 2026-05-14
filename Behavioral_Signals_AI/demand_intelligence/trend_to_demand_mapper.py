"""Map public aggregate trend records into behavioral demand signals."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.recommendation_engine.trend_recommendations import generate_trend_recommendation

CATEGORY_TO_DEMAND = {
    "prices": "household affordability and price pressure",
    "jobs": "employment and skills demand",
    "health": "healthcare access and service demand",
    "food_agriculture": "food and agricultural market demand",
    "mobility_logistics": "transport and logistics demand",
    "finance": "credit, tax, and household liquidity demand",
    "technology": "digital service and productivity demand",
    "trade": "trade, import, export, and competitiveness demand",
    "public_services": "public service delivery demand",
    "general_public_interest": "general market or public concern",
}

COUNTY_HINTS = {
    "nairobi": "Nairobi County",
    "mombasa": "Mombasa County",
    "kisumu": "Kisumu County",
    "nakuru": "Nakuru County",
    "eldoret": "Uasin Gishu County",
    "kiambu": "Kiambu County",
    "machakos": "Machakos County",
}


def map_trend_to_demand_signal(trend: dict[str, Any]) -> dict[str, Any]:
    """Convert one aggregate trend into an interpretable behavioral demand signal."""

    trend_name = str(trend.get("trend_name") or trend.get("name") or "Trend")
    category = str(trend.get("category") or _category_from_name(trend_name))
    inferred_category = CATEGORY_TO_DEMAND.get(category, CATEGORY_TO_DEMAND["general_public_interest"])
    confidence = _confidence_score(trend)
    demand_strength = _demand_strength(trend, confidence)
    unmet = _unmet_demand_likelihood(category, demand_strength, trend_name)
    urgency = _urgency_level(demand_strength, unmet, trend)
    scope = _scope_from_trend(trend)

    signal = {
        "trend_name": trend_name,
        "inferred_product_service_category": inferred_category,
        "inferred_demand_category": inferred_category,
        "demand_signal_strength": round(demand_strength, 1),
        "possible_unmet_demand": round(unmet, 1),
        "unmet_demand_likelihood": round(unmet, 1),
        "urgency": urgency,
        "affected_county_or_scope": scope,
        "business_implication": _business_implication(trend_name, inferred_category, urgency),
        "policy_implication": _policy_implication(trend_name, inferred_category, urgency),
        "confidence_score": round(confidence, 1),
    }
    signal["recommendation"] = generate_trend_recommendation(signal)
    return signal


def map_trends_to_demand_signals(trends: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Map multiple aggregate trends without storing or inferring individual behavior."""

    return [map_trend_to_demand_signal(trend) for trend in trends]


def _confidence_score(trend: dict[str, Any]) -> float:
    value = _numeric(trend.get("confidence_score"), None)
    if value is None:
        value = _numeric(trend.get("confidence"), 0.55)
    if value <= 1:
        value *= 100
    return min(max(value, 10.0), 98.0)


def _demand_strength(trend: dict[str, Any], confidence: float) -> float:
    relevance = _numeric(trend.get("relevance_to_demand"), 0.0)
    if relevance <= 1:
        relevance *= 100
    aggregate = _numeric(trend.get("aggregate_demand_score"), 0.0)
    volume_score = _volume_score(trend.get("volume") or trend.get("tweet_volume"))
    weighted = (max(relevance, aggregate) * 0.48) + (volume_score * 0.22) + (confidence * 0.30)
    return min(max(weighted, 5.0), 99.0)


def _unmet_demand_likelihood(category: str, strength: float, trend_name: str) -> float:
    pressure_bonus = 0.0
    lowered = trend_name.lower()
    if category in {"prices", "health", "food_agriculture", "public_services", "finance"}:
        pressure_bonus += 12.0
    if any(word in lowered for word in ("shortage", "access", "prices", "cost", "fees", "water", "health")):
        pressure_bonus += 10.0
    return min(max((strength * 0.68) + pressure_bonus, 5.0), 96.0)


def _urgency_level(strength: float, unmet: float, trend: dict[str, Any]) -> str:
    growth = str(trend.get("growth_indicator", "")).lower()
    if strength >= 75 or unmet >= 75 or "breakout" in growth or "rising" in growth:
        return "High"
    if strength >= 50 or unmet >= 50:
        return "Medium"
    return "Low"


def _scope_from_trend(trend: dict[str, Any]) -> str:
    location = str(trend.get("location") or "Kenya").strip().lower()
    if location == "global":
        return "Global benchmark"
    return "Kenya-wide"


def _business_implication(trend_name: str, category: str, urgency: str) -> str:
    prefix = "Act quickly" if urgency == "High" else "Monitor" if urgency == "Medium" else "Track"
    return f"{prefix}: {trend_name} may signal demand for {category}; validate with aggregate search, sales, price, and supply indicators."


def _policy_implication(trend_name: str, category: str, urgency: str) -> str:
    prefix = "Prioritize response" if urgency == "High" else "Review policy options" if urgency == "Medium" else "Watch for persistence"
    return f"{prefix}: {trend_name} may indicate {category}; compare with county, price, welfare, and service-delivery data."


def _category_from_name(name: str) -> str:
    lowered = name.lower()
    if any(word in lowered for word in ("price", "fuel", "inflation", "cost", "fees")):
        return "prices"
    if any(word in lowered for word in ("job", "employment", "hiring", "youth")):
        return "jobs"
    if any(word in lowered for word in ("health", "hospital", "clinic", "medicine")):
        return "health"
    if any(word in lowered for word in ("food", "maize", "agri", "farm")):
        return "food_agriculture"
    if any(word in lowered for word in ("transport", "traffic", "delivery", "logistics")):
        return "mobility_logistics"
    if any(word in lowered for word in ("credit", "loan", "tax", "bank", "lending")):
        return "finance"
    if any(word in lowered for word in ("digital", "tech", "ai", "online")):
        return "technology"
    return "general_public_interest"


def _volume_score(value: Any) -> float:
    volume = _numeric(value, None)
    if volume is None:
        return 45.0
    return min(max((volume / 250000.0) * 100.0, 10.0), 100.0)


def _numeric(value: Any, default: float | None) -> float | None:
    if value in {None, "", "not available"}:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).replace(",", "").replace("+", "").strip()
    multiplier = 1.0
    if cleaned.lower().endswith("k"):
        multiplier = 1000.0
        cleaned = cleaned[:-1]
    elif cleaned.lower().endswith("m"):
        multiplier = 1000000.0
        cleaned = cleaned[:-1]
    try:
        return float(cleaned) * multiplier
    except ValueError:
        return default