"""Aggregate behavioral-economic inference layer."""

from __future__ import annotations

from typing import Any


def infer_aggregate_behavior(trend: dict[str, Any], metrics: dict[str, float]) -> dict[str, Any]:
    """Infer Kenya-wide aggregate behavioral meaning from a trend record."""

    pressure = float(metrics.get("economic_pressure", 0.0))
    strength = float(metrics.get("signal_strength", 0.0))
    name = str(trend.get("trend_name", "this trend"))

    if pressure >= 70:
        interpretation = f"{name} suggests visible aggregate economic pressure in Kenya."
    elif strength >= 55:
        interpretation = f"{name} suggests active revealed interest and possible market demand in Kenya."
    else:
        interpretation = f"{name} is an early aggregate signal that should be monitored before action."

    return {
        "scope": "Kenya-wide",
        "behavioral_signal": interpretation,
        "decision_question": "What does this aggregate behavior reveal?",
    }