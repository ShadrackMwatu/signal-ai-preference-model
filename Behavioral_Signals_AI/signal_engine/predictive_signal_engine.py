"""Predictive signal evolution for Kenya aggregate behavioral intelligence."""

from __future__ import annotations

from typing import Any


def predict_signal_evolution(signal: dict[str, Any], memory: dict[str, Any] | None = None, related_signals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Estimate future direction, duration, and spread risk from lightweight evidence."""
    related = related_signals or []
    cluster = _find_cluster(signal, memory or {})
    appearances = int(cluster.get("number_of_appearances", 0) or 0)
    momentum = str(signal.get("momentum", "Stable"))
    urgency_score = _num(signal.get("urgency_score"), _urgency_base(signal.get("urgency")))
    confidence = _num(signal.get("confidence_score"), 50)
    source_agreement = _num(signal.get("multi_source_confirmation_score"), 45)
    category = str(signal.get("signal_category", "other")).lower()

    if momentum in {"Breakout", "Rising"} or urgency_score >= 72:
        direction = "rising"
    elif momentum == "Declining" or confidence < 42:
        direction = "declining"
    else:
        direction = "stable"

    forecast_confidence = min(96.0, max(25.0, confidence * 0.45 + source_agreement * 0.25 + min(100, appearances * 14 + 35) * 0.20 + len(related) * 4))
    expected_duration = _expected_duration(direction, appearances, category)
    spread_risk = estimate_county_spread_risk(signal, cluster, related)
    return {
        "predicted_direction": direction,
        "forecast_confidence": round(forecast_confidence, 1),
        "expected_duration": expected_duration,
        "spread_risk": spread_risk,
    }


def estimate_county_spread_risk(signal: dict[str, Any], cluster: dict[str, Any] | None = None, related_signals: list[dict[str, Any]] | None = None) -> str:
    cluster = cluster or {}
    related = related_signals or []
    category = str(signal.get("signal_category", "other")).lower()
    county_history = {str(item) for item in cluster.get("county_history", []) if item}
    related_counties = {str(item.get("geographic_scope")) for item in related if item.get("geographic_scope")}
    scope = str(signal.get("geographic_scope", "Kenya-wide"))
    county_count = len({scope, *county_history, *related_counties} - {"", "Kenya-wide"})
    pressure_category = category in {"food and agriculture", "cost of living", "energy", "water and sanitation", "transport", "health"}
    if scope == "Kenya-wide" and pressure_category:
        return "High"
    if county_count >= 3:
        return "High"
    if county_count >= 1 or pressure_category:
        return "Moderate"
    return "Low"


def _find_cluster(signal: dict[str, Any], memory: dict[str, Any]) -> dict[str, Any]:
    topic = str(signal.get("signal_topic", "")).lower().strip()
    clusters = memory.get("clusters", {}) if isinstance(memory, dict) else {}
    for key, cluster in clusters.items():
        existing = str(cluster.get("topic", key)).lower().strip()
        if topic == existing or topic in existing or existing in topic:
            return cluster
    return {}


def _expected_duration(direction: str, appearances: int, category: str) -> str:
    if appearances >= 5:
        return "several weeks if aggregate evidence persists"
    if direction == "rising" and category in {"food and agriculture", "cost of living", "energy", "water and sanitation"}:
        return "1-3 weeks, with risk of longer persistence"
    if direction == "declining":
        return "short-lived unless confirmed by new sources"
    return "1-2 weeks under current evidence"


def _urgency_base(urgency: Any) -> float:
    return {"High": 85.0, "Medium": 58.0, "Low": 30.0}.get(str(urgency), 55.0)


def _num(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default
