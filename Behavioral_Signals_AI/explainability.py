"""Simple explainability helpers for Signal demand predictions."""

from __future__ import annotations

from typing import Any


def generate_prediction_explanation(features: dict[str, float], prediction: dict[str, Any]) -> dict[str, Any]:
    """Generate human-readable drivers without using any individual-level data."""

    drivers: list[str] = []

    if features.get("likes", 0) >= 140:
        drivers.append("high likes")
    if features.get("comments", 0) >= 40:
        drivers.append("high comments")
    if features.get("shares", 0) >= 24:
        drivers.append("high shares")
    if features.get("searches", 0) >= 160:
        drivers.append("high searches")
    if features.get("engagement_intensity", 0) >= 0.68:
        drivers.append("strong engagement intensity")
    if features.get("purchase_intent_score", 0) >= 0.65:
        drivers.append("strong purchase intent")
    if features.get("trend_growth", 0) >= 0.45:
        drivers.append("fast trend growth")
    elif features.get("trend_growth", 0) <= 0.1:
        drivers.append("weak trend growth")
    if features.get("noise_score", 0) >= 0.72:
        drivers.append("possible noise")
    if features.get("unmet_need_signal", 0) >= 0.6 or prediction.get("unmet_demand_flag"):
        drivers.append("possible unmet demand")

    if not drivers:
        drivers.append("balanced signal profile with no extreme drivers")

    summary = (
        f"Signal classified this topic as {prediction.get('demand_classification', 'Unknown')} "
        f"with {prediction.get('confidence_score', 0):.0%} confidence. "
        f"The main aggregate drivers were {', '.join(drivers[:4])}."
    )

    return {
        "key_drivers": drivers,
        "driver_summary": summary,
        "policy_note": _policy_note(prediction),
    }


def format_key_drivers_markdown(explanation: dict[str, Any]) -> str:
    drivers = explanation.get("key_drivers", [])
    if not drivers:
        return "- No strong drivers identified."
    return "\n".join(f"- {driver}" for driver in drivers)


def _policy_note(prediction: dict[str, Any]) -> str:
    interpretation = str(prediction.get("investment_opportunity_interpretation", ""))
    if "Strong Investment Opportunity" in interpretation:
        return "This signal supports near-term commercial scaling and targeted policy facilitation."
    if "Emerging Opportunity" in interpretation:
        return "This signal suggests a growing market that merits monitoring, pilot investments, and light-touch support."
    if "Potential Unmet Demand Opportunity" in interpretation or "Possible Unmet Demand" in interpretation or prediction.get("unmet_demand_flag"):
        return "This signal points to a gap between expressed interest and available supply, delivery, or affordability."
    if "Emerging Signal" in interpretation:
        return "This signal is worth monitoring further because momentum exists, but the evidence is not yet strong enough for major commitments."
    if "Limited Market Momentum" in interpretation:
        return "This signal suggests demand remains soft or fragmented, so follow-on validation is recommended before scaling."
    return "This signal should be monitored further before major investment or policy commitments."
