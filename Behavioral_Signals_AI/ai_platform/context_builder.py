"""Build privacy-safe, retrieval-grounded context for Open Signals chat."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.ai_platform.retrieval_engine import retrieve_platform_context
from Behavioral_Signals_AI.data_ingestion.retrieval_index import retrieve_relevant_context
from Behavioral_Signals_AI.ai_platform.safety_layer import sanitize_context

SAFE_SIGNAL_FIELDS = [
    "signal_topic",
    "signal_category",
    "demand_level",
    "opportunity_level",
    "unmet_demand_likelihood",
    "urgency",
    "geographic_scope",
    "county_name",
    "source_summary",
    "confidence_score",
    "priority_score",
    "behavioral_intelligence_score",
    "momentum",
    "forecast_direction",
    "spread_risk",
    "interpretation",
    "recommended_action",
    "historical_pattern_match",
    "outcome_learning_note",
    "validation_status",
    "geospatial_insight",
    "confidence_reasoning",
]


def build_open_signals_context(
    message: str,
    intent: dict[str, Any],
    location: str = "Kenya",
    category: str = "All",
    urgency: str = "All",
    session_context: dict[str, str] | None = None,
    history: list[Any] | None = None,
) -> dict[str, Any]:
    retrieved = retrieve_platform_context(location, category, urgency)
    signals = [_safe_signal(signal) for signal in retrieved.get("signals", [])[:8]]
    retrieved_evidence = retrieve_relevant_context(message, location, category, limit=5)
    context = {
        "question": str(message or "")[:500],
        "intent": dict(intent or {}),
        "filters": retrieved.get("filters", {}),
        "session_context": dict(session_context or {}),
        "recent_history_summary": _history_summary(history),
        "aggregate_live_signals": signals,
        "memory_context": retrieved.get("memory", {}),
        "retrieved_evidence": retrieved_evidence,
        "grounding_notes": [
            "latest live signal cache",
            "historical signal memory",
            "outcome learning memory",
            "geospatial signal memory",
            "behavioral intelligence memory",
            "category learning memory",
            "evaluation metrics when available",
            "ingested public aggregate records retrieval index",
        ],
        "privacy_boundary": "aggregate_anonymized_public_or_user_authorized_only",
    }
    return sanitize_context(context)


def _safe_signal(signal: dict[str, Any]) -> dict[str, Any]:
    return {field: signal.get(field) for field in SAFE_SIGNAL_FIELDS if field in signal}


def _history_summary(history: list[Any] | None) -> list[str]:
    summary = []
    for item in list(history or [])[-4:]:
        if isinstance(item, dict):
            summary.append(str(item.get("content") or "")[:240])
        elif isinstance(item, (tuple, list)):
            summary.extend(str(part or "")[:240] for part in item[:2])
        else:
            summary.append(str(item or "")[:240])
    return summary
