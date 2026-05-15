"""Opportunity reasoning for aggregate Behavioral Signals AI signals."""

from __future__ import annotations

from typing import Any


def infer_opportunity_type(signal: dict[str, Any]) -> str:
    text = " ".join(str(signal.get(key, "")) for key in ["signal_topic", "signal_category", "semantic_cluster", "outcome_learning_note"]).lower()
    families = {str(item).lower() for item in signal.get("behavioral_families", [])}
    if any(word in text for word in ["price", "cheap", "affordable", "cost", "unga", "maize", "fuel", "rent"]):
        return "affordability pressure"
    if any(word in text for word in ["shortage", "water", "hospital", "clinic", "service", "public"]):
        return "service delivery gap"
    if any(word in text for word in ["supply", "available", "where to buy", "delivery"]):
        return "supply shortage"
    if any(word in text for word in ["jobs", "employment", "hiring", "work"]):
        return "employment pressure"
    if any(word in text for word in ["drought", "flood", "climate", "rain"]):
        return "climate stress"
    if "opportunity" in families or str(signal.get("opportunity_level", "")).lower() == "high":
        return "market opportunity"
    return "policy concern"


def fallback_opportunity_reasoning(signal: dict[str, Any]) -> dict[str, str]:
    opportunity_type = infer_opportunity_type(signal)
    topic = str(signal.get("signal_topic", "this signal"))
    category = str(signal.get("signal_category", signal.get("category", "other")))
    return {
        "opportunity_type": opportunity_type,
        "opportunity_interpretation": f"{topic} may represent a {opportunity_type} in {category} that should be validated with aggregate follow-up evidence.",
        "recommended_action": str(signal.get("recommended_action") or f"Monitor {topic}, compare related signals, and test a targeted response if persistence increases."),
    }