"""Infer demand and opportunity labels from normalized aggregate signals."""

from __future__ import annotations

from typing import Any


def _level(score: float) -> str:
    if score >= 75:
        return "High"
    if score >= 50:
        return "Moderate"
    return "Low"


def _urgency(growth: float, unmet: float) -> str:
    combined = growth * 0.55 + unmet * 0.45
    if combined >= 74:
        return "High"
    if combined >= 48:
        return "Medium"
    return "Low"


def infer_topical_signal(record: dict[str, Any], category: str, persistence_score: float = 50.0, source_confirmation: int = 1) -> dict[str, Any]:
    interest = float(record.get("relative_interest", 50.0))
    engagement = float(record.get("engagement_signal", 50.0))
    growth = float(record.get("growth_signal", 50.0))
    sentiment = float(record.get("sentiment_signal", 0.0))
    demand_score = min(100.0, max(0.0, interest * 0.48 + engagement * 0.22 + growth * 0.20 + persistence_score * 0.10))
    unmet_score = min(100.0, max(0.0, growth * 0.45 + interest * 0.30 + max(0.0, -sentiment * 100) * 0.25))
    opportunity_score = min(100.0, max(0.0, demand_score * 0.45 + unmet_score * 0.35 + min(source_confirmation, 3) * 6.0 + persistence_score * 0.08))
    confidence = min(96.0, max(35.0, 42.0 + source_confirmation * 8.0 + persistence_score * 0.18 + (100.0 - abs(sentiment) * 20.0) * 0.08))
    topic = str(record.get("topic", "Kenya demand signal"))
    return {
        "signal_topic": topic,
        "signal_category": category,
        "demand_level": _level(demand_score),
        "opportunity_level": _level(opportunity_score),
        "unmet_demand_likelihood": _level(unmet_score),
        "urgency": _urgency(growth, unmet_score),
        "geographic_scope": str(record.get("location") or "Kenya-wide"),
        "recommended_action": _recommended_action(category, demand_score, unmet_score),
        "confidence_score": round(confidence, 1),
        "last_updated": str(record.get("timestamp")),
        "demand_score": round(demand_score, 1),
        "opportunity_score": round(opportunity_score, 1),
        "persistence_score": round(persistence_score, 1),
        "source_confirmation": int(source_confirmation),
        "privacy_level": "aggregate_public",
    }


def _recommended_action(category: str, demand_score: float, unmet_score: float) -> str:
    if unmet_score >= 70:
        return f"Validate supply gaps in {category} and prepare targeted inventory, service, or policy response."
    if demand_score >= 70:
        return f"Monitor fast-moving {category} demand and test near-term business or public-service response."
    return f"Keep monitoring {category}; signal is developing but does not yet require a major response."