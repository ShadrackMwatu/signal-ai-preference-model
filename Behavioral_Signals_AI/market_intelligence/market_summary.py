"""Market intelligence summaries for decision-oriented Behavioral Signals AI outputs."""

from __future__ import annotations

from typing import Any


def summarize_market_intelligence(signals: list[dict[str, Any]]) -> dict[str, Any]:
    if not signals:
        return {"headline": "No aggregate demand signals available.", "top_opportunities": [], "recommended_actions": []}
    ranked = sorted(signals, key=lambda item: float(item.get("demand_signal_strength", 0.0)), reverse=True)
    top = ranked[:3]
    return {
        "headline": f"Signal identified {len(signals)} Kenya-wide aggregate demand signal(s).",
        "top_opportunities": [item.get("trend_name", "Trend") for item in top],
        "recommended_actions": [item.get("recommendation", "Monitor aggregate indicators.") for item in top],
    }