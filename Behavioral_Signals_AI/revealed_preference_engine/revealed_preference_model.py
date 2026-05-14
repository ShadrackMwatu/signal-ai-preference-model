"""Revealed-preference inference from aggregate digital behavioral traces."""

from __future__ import annotations

from typing import Any


def infer_revealed_preference(trend: dict[str, Any], metrics: dict[str, float]) -> dict[str, Any]:
    """Infer aggregate revealed interest, need, pressure, and substitution signals."""

    category = str(trend.get("category", "general_public_interest"))
    strength = float(metrics.get("signal_strength", 0.0))
    pressure = float(metrics.get("economic_pressure", 0.0))
    persistence = float(metrics.get("persistence", 0.0))

    return {
        "revealed_interest": _band(strength),
        "revealed_need": _band((pressure * 0.65) + (strength * 0.35)),
        "revealed_pressure": _band(pressure),
        "revealed_aggregate_demand": _demand_class(strength, pressure),
        "substitution_effect": _substitution_effect(category, str(trend.get("trend_name", ""))),
        "emerging_consumption_shift": "Likely" if persistence >= 65 and strength >= 55 else "Watch" if persistence >= 45 else "Weak",
    }


def _band(value: float) -> str:
    if value >= 75:
        return "High"
    if value >= 50:
        return "Moderate"
    return "Low"


def _demand_class(strength: float, pressure: float) -> str:
    if strength >= 75 and pressure >= 65:
        return "High revealed demand"
    if strength >= 55:
        return "Moderate revealed demand"
    if strength >= 40:
        return "Emerging revealed demand"
    return "Low revealed demand"


def _substitution_effect(category: str, name: str) -> str:
    lowered = name.lower()
    if category == "prices" or any(word in lowered for word in ("price", "cost", "fees", "fuel")):
        return "Consumers may search for cheaper substitutes or delay purchases."
    if category in {"technology", "finance"}:
        return "Users may shift toward digital or lower-friction alternatives."
    if category in {"mobility_logistics", "food_agriculture"}:
        return "Demand may shift toward more reliable, closer, or lower-cost suppliers."
    return "Substitution effect unclear from aggregate trend alone."