"""Adaptive demand forecasting from aggregate behavioral signals."""

from __future__ import annotations

from typing import Any


def forecast_demand(signal: dict[str, Any]) -> dict[str, Any]:
    strength = float(signal.get("demand_signal_strength") or signal.get("signal_strength") or 0.0)
    persistence = float(signal.get("signal_persistence") or signal.get("persistence") or 50.0)
    confidence = float(signal.get("adaptive_confidence") or signal.get("confidence_score") or signal.get("confidence") or 50.0)
    forecast = (strength * 0.48) + (persistence * 0.28) + (confidence * 0.24)
    return {
        "predicted_demand_strength": round(min(max(forecast, 0), 100), 2),
        "predicted_demand_level": "High" if forecast >= 75 else "Moderate" if forecast >= 50 else "Emerging" if forecast >= 35 else "Low",
    }