"""Lightweight forecasting foundation for aggregate behavioral signals."""

from __future__ import annotations

from typing import Any


def forecast_trend_persistence(trend: dict[str, Any], metrics: dict[str, float]) -> dict[str, Any]:
    persistence = float(metrics.get("persistence", 0.0))
    volatility = float(metrics.get("volatility", 0.0))
    if persistence >= 70 and volatility <= 45:
        outlook = "Likely to persist"
    elif persistence >= 50:
        outlook = "May continue"
    elif volatility >= 70:
        outlook = "Volatile signal"
    else:
        outlook = "Early/uncertain"
    return {
        "demand_persistence": round(persistence, 1),
        "volatility": round(volatility, 1),
        "forecast_outlook": outlook,
        "likely_demand_growth": "High" if persistence >= 70 else "Moderate" if persistence >= 50 else "Low",
    }