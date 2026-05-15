"""Strategic summary generation for aggregate Behavioral Signals AI outputs."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.llm.llm_client import complete_json
from Behavioral_Signals_AI.llm.prompt_templates import STRATEGIC_SUMMARY_TEMPLATE
from Behavioral_Signals_AI.llm.safety_guardrails import sanitize_llm_signals


def generate_strategic_signal_summary(signals: list[dict[str, Any]]) -> str:
    safe_signals = sanitize_llm_signals(signals or [])
    fallback = {"summary": _fallback_summary(safe_signals)}
    result = complete_json(STRATEGIC_SUMMARY_TEMPLATE, {"signals": safe_signals}, fallback=fallback)
    return str(result.get("summary") or fallback["summary"])


def _fallback_summary(signals: list[dict[str, Any]]) -> str:
    if not signals:
        return "Aggregate signal monitoring is active. Strategic insight will strengthen as more signals persist and validate."
    top = signals[0]
    topic = top.get("signal_topic") or top.get("topic") or "Kenya aggregate demand"
    categories = sorted({str(signal.get("signal_category") or signal.get("category") or "other") for signal in signals})
    scopes = sorted({str(signal.get("geographic_scope") or signal.get("county_or_scope") or "Kenya-wide") for signal in signals})
    return (
        f"Main issue emerging: {topic}. Strongest opportunity: monitor and respond to persistent demand in {', '.join(categories[:4])}. "
        f"Highest policy concern: validate affordability, service, or supply pressure where urgency is rising. "
        f"Counties or scope affected: {', '.join(scopes[:4])}. Monitor next: persistence, source agreement, outcome validation, and county spread."
    )