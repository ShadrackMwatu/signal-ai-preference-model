"""Privacy guardrails for LLM-assisted aggregate signal interpretation."""

from __future__ import annotations

from typing import Any

PRIVATE_FIELDS = {
    "user_id",
    "userid",
    "name",
    "full_name",
    "email",
    "phone",
    "private_message",
    "message_text",
    "exact_location",
    "gps",
    "latitude",
    "longitude",
    "individual_profile",
    "personal_profile",
    "profile_url",
    "ip_address",
    "device_id",
    "cookie_id",
}

ALLOWED_SIGNAL_FIELDS = {
    "signal_topic",
    "topic",
    "category",
    "signal_category",
    "county_or_scope",
    "geographic_scope",
    "behavioral_families",
    "momentum",
    "confidence_score",
    "source_summary",
    "historical_pattern_match",
    "outcome_learning_note",
    "validation_status",
    "demand_level",
    "opportunity_level",
    "unmet_demand_likelihood",
    "urgency",
    "forecast_direction",
    "predicted_direction",
    "privacy_level",
    "ml_adaptive_context",
    "historical_learning_note",
    "source_validation",
    "source_reliability",
    "accuracy_confidence",
    "persistence_score",
    "behavioral_intelligence_score",
    "priority_score",
    "confidence_reasoning",
    "geospatial_insight",
    "county_code",
    "county_name",
}


def sanitize_llm_signal_input(signal: dict[str, Any]) -> dict[str, Any]:
    """Return a compact aggregate-only payload safe for LLM processing."""
    safe: dict[str, Any] = {}
    for key in ALLOWED_SIGNAL_FIELDS:
        if key in signal and key.lower() not in PRIVATE_FIELDS:
            safe[key] = _sanitize_value(signal[key])
    safe["privacy_instruction"] = "aggregate_public_or_authorized_only_no_individual_profiling"
    return safe


def sanitize_llm_signals(signals: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    return [sanitize_llm_signal_input(signal) for signal in signals[:limit]]


def contains_private_fields(payload: Any) -> bool:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if str(key).lower() in PRIVATE_FIELDS:
                return True
            if contains_private_fields(value):
                return True
    elif isinstance(payload, list):
        return any(contains_private_fields(item) for item in payload)
    return False


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value if not isinstance(item, dict)]
    if isinstance(value, dict):
        return {str(k): _sanitize_value(v) for k, v in value.items() if str(k).lower() not in PRIVATE_FIELDS}
    return str(value)