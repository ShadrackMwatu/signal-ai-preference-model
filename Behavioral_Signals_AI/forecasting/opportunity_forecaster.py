"""Opportunity forecasting from aggregate demand and persistence signals."""

from __future__ import annotations

from typing import Any


def forecast_opportunity(signal: dict[str, Any]) -> dict[str, Any]:
    demand = float(signal.get("predicted_demand_strength") or signal.get("demand_signal_strength") or 0.0)
    unmet = float(signal.get("possible_unmet_demand") or signal.get("unmet_demand_likelihood") or 0.0)
    confidence = float(signal.get("adaptive_confidence") or signal.get("confidence_score") or 50.0)
    score = (demand * 0.45) + (unmet * 0.35) + (confidence * 0.20)
    return {
        "predicted_opportunity_score": round(min(max(score, 0), 100), 2),
        "predicted_opportunity_level": "High" if score >= 75 else "Moderate" if score >= 50 else "Watch",
    }