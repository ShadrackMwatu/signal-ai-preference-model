"""LLM-assisted and fallback interpretation for aggregate behavioral signals."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.llm.llm_client import complete_json
from Behavioral_Signals_AI.llm.opportunity_reasoner import fallback_opportunity_reasoning, infer_opportunity_type
from Behavioral_Signals_AI.llm.prompt_templates import SIGNAL_INTERPRETATION_TEMPLATE
from Behavioral_Signals_AI.llm.safety_guardrails import sanitize_llm_signal_input

REQUIRED_INTERPRETATION_FIELDS = [
    "plain_language_meaning",
    "economic_interpretation",
    "opportunity_interpretation",
    "policy_implication",
    "recommended_action",
    "risk_note",
]


def interpret_signal_with_llm(signal: dict[str, Any]) -> dict[str, str]:
    """Interpret one aggregate signal with optional LLM support and safe fallback."""
    safe_signal = sanitize_llm_signal_input(signal)
    fallback = _fallback_interpretation(safe_signal)
    result = complete_json(SIGNAL_INTERPRETATION_TEMPLATE, safe_signal, fallback=fallback)
    output = _normalize_interpretation(result, fallback)
    output["llm_input_privacy"] = "aggregate_sanitized"
    return output


def _fallback_interpretation(signal: dict[str, Any]) -> dict[str, str]:
    topic = str(signal.get("signal_topic") or signal.get("topic") or "this aggregate signal")
    category = str(signal.get("signal_category") or signal.get("category") or "other")
    scope = str(signal.get("geographic_scope") or signal.get("county_or_scope") or "Kenya-wide")
    families = ", ".join(str(item) for item in signal.get("behavioral_families", []) or ["Demand"])
    momentum = str(signal.get("momentum") or signal.get("forecast_direction") or "Stable")
    outcome_note = str(signal.get("outcome_learning_note") or "Outcome evidence is still accumulating.")
    opportunity = fallback_opportunity_reasoning(signal)
    pressure = infer_opportunity_type(signal)
    return {
        "plain_language_meaning": f"{topic} is an aggregate {category} signal in {scope} with {momentum.lower()} momentum.",
        "economic_interpretation": f"The signal reflects {families.lower()} behavior and may indicate {pressure} affecting households, businesses, or public services.",
        "opportunity_interpretation": opportunity["opportunity_interpretation"],
        "policy_implication": f"Use the signal as an early aggregate indicator for monitoring, validation, and targeted policy response in {category}.",
        "recommended_action": opportunity["recommended_action"],
        "risk_note": f"Interpret cautiously because signals are aggregate indicators, not individual behavior. {outcome_note}",
        "llm_mode": "rule_based_fallback",
    }


def _normalize_interpretation(result: dict[str, Any], fallback: dict[str, str]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for field in REQUIRED_INTERPRETATION_FIELDS:
        value = result.get(field) or fallback.get(field) or "Aggregate interpretation is still developing."
        normalized[field] = str(value)
    normalized["llm_mode"] = str(result.get("llm_mode") or fallback.get("llm_mode") or "rule_based_fallback")
    if result.get("llm_warning"):
        normalized["llm_warning"] = str(result["llm_warning"])
    if result.get("llm_provider"):
        normalized["llm_provider"] = str(result["llm_provider"])
    return normalized