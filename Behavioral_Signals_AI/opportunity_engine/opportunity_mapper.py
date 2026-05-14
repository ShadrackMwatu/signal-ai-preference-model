"""Opportunity intelligence from revealed aggregate demand."""

from __future__ import annotations

from typing import Any


def infer_opportunity(trend: dict[str, Any], metrics: dict[str, float], preference: dict[str, Any]) -> dict[str, Any]:
    category = str(trend.get("category", "general_public_interest"))
    strength = float(metrics.get("signal_strength", 0.0))
    pressure = float(metrics.get("economic_pressure", 0.0))

    if category in {"prices", "food_agriculture", "health", "public_services"} and pressure >= 60:
        opportunity_type = "supply gap or affordability opportunity"
    elif category in {"mobility_logistics"}:
        opportunity_type = "logistics and delivery opportunity"
    elif category in {"technology", "finance"}:
        opportunity_type = "digital-service opportunity"
    elif strength >= 65:
        opportunity_type = "market expansion opportunity"
    else:
        opportunity_type = "monitoring opportunity"

    return {
        "opportunity_type": opportunity_type,
        "market_gap": "Likely" if pressure >= 65 else "Possible" if pressure >= 45 else "Unclear",
        "opportunity_score": round((strength * 0.55) + (pressure * 0.45), 1),
    }