"""Response planning for Open Signals conversational intelligence."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.ai_platform.safety_layer import PRIVATE_DATA_RESPONSE

CLARIFICATION = "Do you want me to explain the strongest current signal, a specific county, or a market opportunity?"


def choose_response_mode(intent: str, message: str = "") -> str:
    lowered = str(message or "").lower()
    if intent == "greeting":
        return "greeting"
    if intent == "identity_query":
        return "identity"
    if intent in {"capability_query", "help", "small_talk"}:
        return "capability"
    if intent == "comparison_query" or "compare" in lowered:
        return "comparison_answer"
    if "policy" in lowered or "policymaker" in lowered or "government" in lowered:
        return "policy_answer"
    if "business" in lowered or "opportunity" in lowered or "market" in lowered:
        return "business_opportunity_answer"
    if intent in {"unclear_query", "follow_up_query"}:
        return "clarification"
    return "analytical_answer"


def deterministic_response(mode: str, context: dict[str, Any]) -> str:
    if mode == "greeting":
        return "Hello. I'm Open Signals - I monitor emerging aggregate behavioral signals, market pressure, risks, and opportunities across Kenya."
    if mode == "identity":
        return "I'm Open Signals - a privacy-preserving behavioral economic intelligence analyst for aggregate demand, risks, opportunities, and county trends in Kenya."
    if mode == "capability":
        return "I can help analyze county-level signals, affordability pressure, market opportunities, economic stress, policy concerns, and evolving behavioral trends using aggregate intelligence."
    if mode == "privacy_refusal":
        return PRIVATE_DATA_RESPONSE
    if mode == "clarification":
        return CLARIFICATION
    signals = context.get("aggregate_live_signals") or []
    evidence = context.get("retrieved_evidence") or []
    top = signals[0] if signals else _signal_from_evidence(evidence[0]) if evidence else {}
    if not top:
        return "I do not have enough current aggregate evidence for that yet."
    return _format_signal_answer(top, mode)


def _format_signal_answer(signal: dict[str, Any], mode: str) -> str:
    topic = signal.get("signal_topic", "current aggregate signal")
    scope = signal.get("county_name") or signal.get("geographic_scope") or "Kenya-wide"
    confidence = signal.get("confidence_score", "unknown")
    action = signal.get("recommended_action") or "Monitor persistence, validate with aggregate sources, and watch whether related signals strengthen."
    meaning = signal.get("interpretation") or signal.get("geospatial_insight") or f"{topic} may reflect an emerging aggregate demand, risk, or opportunity pattern."
    if mode == "policy_answer":
        focus = "Policy focus: monitor urgency, spread risk, service pressure, affordability effects, and whether outcome evidence confirms the signal."
    elif mode == "business_opportunity_answer":
        focus = "Opportunity focus: look for unmet demand, supply gaps, affordability constraints, and county-level market response options."
    else:
        focus = f"Opportunity or risk: {signal.get('opportunity_level', 'Moderate')} opportunity, {signal.get('unmet_demand_likelihood', 'Medium')} unmet demand, {signal.get('urgency', 'Medium')} urgency."
    return (
        f"**Short answer:** {topic} is the strongest relevant signal for {scope}.\n\n"
        f"- **What it means:** {meaning}\n"
        f"- **Confidence level:** {confidence}%\n"
        f"- **County/scope:** {scope}\n"
        f"- **{focus}**\n"
        f"- **Recommended action:** {action}"
    )


def _signal_from_evidence(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_topic": record.get("topic"),
        "signal_category": record.get("category"),
        "county_name": record.get("county_name") or record.get("location"),
        "geographic_scope": record.get("location"),
        "confidence_score": record.get("confidence"),
        "interpretation": record.get("summary"),
        "recommended_action": "Validate this retrieved aggregate evidence against live signals, history, and outcome learning.",
        "opportunity_level": "Moderate",
        "unmet_demand_likelihood": "Medium",
        "urgency": "Medium",
    }
