"""Open Signals AI-native intelligence orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.ai_platform.context_builder import build_open_signals_context
from Behavioral_Signals_AI.ai_platform.response_planner import choose_response_mode, deterministic_response
from Behavioral_Signals_AI.ai_platform.safety_layer import PRIVATE_DATA_RESPONSE, context_contains_private_fields, is_privacy_sensitive_prompt
from Behavioral_Signals_AI.chat.intents import detect_open_signals_intent
from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS
from Behavioral_Signals_AI.llm.open_signals_llm_orchestrator import generate_open_signals_llm_answer
from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

METRICS_PATH = Path("Behavioral_Signals_AI/outputs/evaluation_metrics.json")


@dataclass
class OpenSignalsOrchestrationResult:
    answer: str
    mode: str
    intent: str
    context: dict[str, Any]
    used_llm: bool = False


def orchestrate_open_signals_answer(
    message: str,
    history: list[Any] | None = None,
    location: str = "Kenya",
    category: str = "All",
    urgency: str = "All",
    session_context: dict[str, str] | None = None,
) -> OpenSignalsOrchestrationResult:
    if is_privacy_sensitive_prompt(message):
        _increment_metric("privacy_refusal_count")
        return OpenSignalsOrchestrationResult(PRIVATE_DATA_RESPONSE, "privacy_refusal", "privacy_refusal", {}, False)
    intent = detect_open_signals_intent(message)
    context = build_open_signals_context(message, intent, location, category, urgency, session_context, history)
    if context_contains_private_fields(context):
        _increment_metric("privacy_refusal_count")
        return OpenSignalsOrchestrationResult(PRIVATE_DATA_RESPONSE, "privacy_refusal", intent["intent"], {}, False)
    mode = choose_response_mode(intent["intent"], message)
    if mode == "comparison_answer":
        comparison_answer = _comparison_fallback(message, category, urgency)
        if comparison_answer:
            return OpenSignalsOrchestrationResult(comparison_answer, mode, intent["intent"], context, False)
    fallback = deterministic_response(mode, context)
    result = generate_open_signals_llm_answer(mode, context, fallback)
    answer = str(result.get("answer") or fallback)
    used_llm = result.get("llm_mode") == "api"
    if not used_llm:
        _increment_metric("chat_fallback_rate")
    return OpenSignalsOrchestrationResult(answer, mode, intent["intent"], context, used_llm)


def run_open_signals_learning_cycle() -> dict[str, Any]:
    """Update backend aggregate learning and evaluation metrics without storing personal data."""
    from Behavioral_Signals_AI.ai_platform.retrieval_engine import retrieve_platform_context

    context = retrieve_platform_context("Kenya", "All", "All")
    signals = context.get("signals", [])
    metrics = build_evaluation_metrics(signals, context.get("memory", {}))
    write_json(METRICS_PATH, metrics)
    return metrics


def build_evaluation_metrics(signals: list[dict[str, Any]], memory: dict[str, Any] | None = None) -> dict[str, Any]:
    memory = memory or {}
    active = len(signals)
    validated = sum(1 for signal in signals if str(signal.get("validation_status", "")).lower() in {"validated", "partially_validated"})
    county_specific = sum(1 for signal in signals if signal.get("county_name") and signal.get("county_name") != "Kenya-wide")
    confidences = [_number(signal.get("confidence_score")) for signal in signals if _number(signal.get("confidence_score")) > 0]
    source_coverage = sorted({str(signal.get("source_summary", "unknown"))[:80] for signal in signals if signal.get("source_summary")})
    outcomes = memory.get("outcomes", []) if isinstance(memory, dict) else []
    confirmed = sum(1 for item in outcomes if str(item.get("outcome_status", "")).lower() in {"confirmed", "partially_confirmed"})
    false_positive_candidates = sum(1 for item in outcomes if str(item.get("outcome_status", "")).lower() == "not_confirmed")
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "active_signals": active,
        "validated_signals": validated,
        "county_specific_signals": county_specific,
        "source_coverage": source_coverage,
        "fallback_usage": _current_metric("chat_fallback_rate"),
        "average_confidence": round(sum(confidences) / len(confidences), 2) if confidences else 0,
        "outcome_confirmation_rate": round(confirmed / len(outcomes), 3) if outcomes else 0,
        "false_positive_candidates": false_positive_candidates,
        "chat_fallback_rate": _current_metric("chat_fallback_rate"),
        "privacy_refusal_count": _current_metric("privacy_refusal_count"),
        "privacy_level": "aggregate_public",
    }


def _increment_metric(name: str) -> None:
    metrics = read_json(METRICS_PATH, {})
    if not isinstance(metrics, dict):
        metrics = {}
    metrics[name] = int(metrics.get(name, 0) or 0) + 1
    metrics["last_updated"] = datetime.now(UTC).isoformat()
    write_json(METRICS_PATH, metrics)


def _current_metric(name: str) -> int:
    metrics = read_json(METRICS_PATH, {})
    if isinstance(metrics, dict):
        try:
            return int(metrics.get(name, 0) or 0)
        except (TypeError, ValueError):
            return 0
    return 0


def _number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0



def _comparison_fallback(message: str, category: str = "All", urgency: str = "All") -> str:
    from Behavioral_Signals_AI.ai_platform.retrieval_engine import compare_counties

    counties = _counties_from_text(message)
    if len(counties) < 2:
        return ""
    comparison = compare_counties(counties[0], counties[1], category or "All", urgency or "All")
    first = comparison.get("county_a_signal") or {}
    second = comparison.get("county_b_signal") or {}
    stronger = comparison.get("stronger_county") or counties[0]
    return (
        f"**Short answer:** {stronger} currently shows the stronger aggregate signal in this comparison.\n\n"
        f"- **{counties[0]}:** {first.get('signal_topic', 'No strong signal available')} "
        f"with {first.get('confidence_score', 'unknown')}% confidence and {first.get('spread_risk', 'Moderate')} spread risk.\n"
        f"- **{counties[1]}:** {second.get('signal_topic', 'No strong signal available')} "
        f"with {second.get('confidence_score', 'unknown')}% confidence and {second.get('spread_risk', 'Moderate')} spread risk.\n"
        "- **Recommended action:** Compare persistence, urgency, and outcome confirmation before deciding where to prioritize response."
    )


def _counties_from_text(message: str) -> list[str]:
    normalized = " ".join(str(message or "").lower().replace("_", " ").replace("-", " ").split())
    matches = []
    for option in LOCATION_OPTIONS:
        if option in {"Global", "Kenya"}:
            continue
        option_norm = " ".join(option.lower().replace("_", " ").replace("-", " ").split())
        index = normalized.find(option_norm)
        if index >= 0:
            matches.append((index, option))
    return [county for _, county in sorted(matches)]
