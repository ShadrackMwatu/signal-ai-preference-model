"""Interactive aggregate-signal Q&A for Open Signals."""

from __future__ import annotations

import re
from typing import Any

from Behavioral_Signals_AI.geography.county_matcher import signal_matches_location
from Behavioral_Signals_AI.llm.llm_client import complete_json
from Behavioral_Signals_AI.signal_engine.category_learning import category_matches_signal
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals
from Behavioral_Signals_AI.ui.feed_diff_engine import rank_signals_for_display

FORBIDDEN_PROMPT_PATTERNS = [
    re.compile(r"\b(user_id|device_id|phone|email|private_message|personal_profile|exact location|gps|route|home address|work address)\b", re.IGNORECASE),
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"\b(?:\+?254|0)?7\d{8}\b"),
]

CHAT_SYSTEM_PROMPT = (
    "You are Open Signals. Answer only from aggregate, anonymized, public, or user-authorized signal intelligence. "
    "Do not reveal raw searches, raw likes, raw comments, raw shares, personal identities, device IDs, exact personal locations, "
    "private movement traces, or individual profiles. Be concise and focus on demand, risks, opportunities, counties, and policy implications. "
    "Return JSON with one field: answer."
)

SAFE_FIELDS = [
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


def answer_open_signals_prompt(message: str, history: list[Any] | None, location: str, category: str, urgency: str) -> str:
    """Answer a user question using only current interpreted aggregate signals."""
    cleaned = str(message or "").strip()
    if not cleaned:
        return "Ask a question about live aggregate signals, counties, demand, risks, or opportunities."
    if _has_private_request(cleaned):
        return (
            "I cannot answer questions that request personal identities, device data, private messages, exact personal locations, "
            "routes, or individual profiles. Open Signals only discusses aggregate interpreted signal intelligence."
        )

    signals = _filtered_ranked_signals(location or "Kenya", category or "All", urgency or "All")
    if not signals:
        return "No matching aggregate signals are currently available for those filters. Try Kenya, All categories, or a broader urgency filter."

    fallback = {"answer": _rule_based_answer(cleaned, signals, location or "Kenya", category or "All", urgency or "All")}
    payload = {
        "question": cleaned,
        "filters": {"location": location or "Kenya", "category": category or "All", "urgency": urgency or "All"},
        "signals": [_safe_signal(signal) for signal in signals[:6]],
        "history_turns": _safe_history(history),
        "privacy_boundary": "aggregate_interpreted_signals_only",
    }
    result = complete_json(CHAT_SYSTEM_PROMPT, payload, fallback=fallback)
    answer = str(result.get("answer") or fallback["answer"]).strip()
    return _strip_private_terms(answer) or fallback["answer"]


def respond_open_signals_chat(message: str, history: list[Any] | None, location: str, category: str, urgency: str) -> tuple[list[Any], str]:
    """Gradio adapter that appends an Open Signals answer to chat history."""
    answer = answer_open_signals_prompt(message, history or [], location, category, urgency)
    updated_history = list(history or [])
    if updated_history and isinstance(updated_history[0], tuple):
        updated_history.append((str(message or "").strip(), answer))
    else:
        updated_history.append({"role": "user", "content": str(message or "").strip()})
        updated_history.append({"role": "assistant", "content": answer})
    return updated_history, ""


def _filtered_ranked_signals(location: str, category: str, urgency: str) -> list[dict[str, Any]]:
    payload = get_cached_or_fallback_signals()
    signals = [signal for signal in payload.get("signals", []) if isinstance(signal, dict)]
    filtered: list[dict[str, Any]] = []
    for signal in signals:
        if not category_matches_signal(signal, category):
            continue
        if urgency != "All" and str(signal.get("urgency", "")).lower() != urgency.lower():
            continue
        if location not in {"", "All", "Kenya", "Global"} and not signal_matches_location(signal, location):
            continue
        filtered.append(signal)
    return rank_signals_for_display(filtered or signals)


def _rule_based_answer(question: str, signals: list[dict[str, Any]], location: str, category: str, urgency: str) -> str:
    q = question.lower()
    top = signals[0]
    if "strongest" in q or "top" in q or "now" in q:
        return _strongest_signal_answer(top, location)
    if "opportun" in q or "market" in q or "business" in q:
        return _opportunity_answer(signals)
    if "policy" in q or "policymaker" in q or "monitor" in q:
        return _policy_answer(signals)
    if "water" in q:
        water = [signal for signal in signals if "water" in _signal_blob(signal)]
        return _theme_answer(water or signals, "water access stress")
    if location not in {"", "All", "Kenya", "Global"} or "county" in q or "happening" in q:
        return _location_answer(signals, location)
    return _summary_answer(signals, location, category, urgency)


def _strongest_signal_answer(signal: dict[str, Any], location: str) -> str:
    return (
        f"The strongest current aggregate signal for {location or signal.get('geographic_scope', 'Kenya')} is "
        f"{signal.get('signal_topic', 'an emerging aggregate signal')}. It is classified as "
        f"{signal.get('signal_category', 'other')}, with {signal.get('urgency', 'Medium')} urgency, "
        f"{signal.get('demand_level', 'Moderate')} demand, and {signal.get('opportunity_level', 'Moderate')} opportunity. "
        f"Recommended action: {signal.get('recommended_action', 'monitor persistence and validate with aggregate sources')}"
    )


def _opportunity_answer(signals: list[dict[str, Any]]) -> str:
    opportunities = [signal for signal in signals if str(signal.get("opportunity_level", "")).lower() == "high"] or signals[:3]
    bullets = "; ".join(f"{s.get('signal_topic')} ({s.get('signal_category')})" for s in opportunities[:3])
    return f"The clearest opportunity signals are: {bullets}. These should be monitored for persistence, county spread, and source confirmation before action."


def _policy_answer(signals: list[dict[str, Any]]) -> str:
    top = signals[0]
    return (
        f"Policymakers should monitor {top.get('signal_topic', 'the leading aggregate signal')} because it may indicate "
        f"{top.get('unmet_demand_likelihood', 'Medium')} unmet demand, {top.get('urgency', 'Medium')} urgency, and "
        f"{top.get('spread_risk', 'Low')} spread risk. Historical note: "
        f"{top.get('outcome_learning_note') or top.get('historical_pattern_match') or 'outcome evidence is still accumulating.'}"
    )


def _theme_answer(signals: list[dict[str, Any]], theme: str) -> str:
    top = signals[0]
    return (
        f"For {theme}, the closest aggregate signal is {top.get('signal_topic')}. "
        f"It suggests {top.get('demand_level', 'Moderate')} demand pressure and {top.get('urgency', 'Medium')} urgency. "
        f"Geospatial context: {top.get('geospatial_insight', top.get('geographic_scope', 'Kenya-wide'))}."
    )


def _location_answer(signals: list[dict[str, Any]], location: str) -> str:
    top = signals[0]
    scope = location if location not in {"", "All"} else top.get("geographic_scope", "Kenya")
    return (
        f"In {scope}, the leading interpreted signal is {top.get('signal_topic')}. "
        f"It points to {top.get('signal_category', 'aggregate demand')} with {top.get('momentum', 'Stable')} momentum, "
        f"{top.get('confidence_score', 0)}% confidence, and {top.get('forecast_direction', 'Stable')} forecast direction."
    )


def _summary_answer(signals: list[dict[str, Any]], location: str, category: str, urgency: str) -> str:
    top = signals[0]
    return (
        f"Using the current filters ({location}, {category}, {urgency}), Open Signals sees {len(signals)} interpreted aggregate signal(s). "
        f"The leading issue is {top.get('signal_topic')}, categorized as {top.get('signal_category')}. "
        f"It reflects {top.get('demand_level', 'Moderate')} demand, {top.get('opportunity_level', 'Moderate')} opportunity, "
        f"and {top.get('urgency', 'Medium')} urgency."
    )


def _safe_signal(signal: dict[str, Any]) -> dict[str, Any]:
    return {field: signal.get(field) for field in SAFE_FIELDS if field in signal}


def _safe_history(history: list[Any] | None) -> list[str]:
    safe: list[str] = []
    for item in list(history or [])[-3:]:
        safe.append(_strip_private_terms(str(item))[:240])
    return safe


def _signal_blob(signal: dict[str, Any]) -> str:
    return " ".join(str(value).lower() for value in _safe_signal(signal).values() if value)


def _has_private_request(text: str) -> bool:
    return any(pattern.search(text or "") for pattern in FORBIDDEN_PROMPT_PATTERNS)


def _strip_private_terms(text: str) -> str:
    cleaned = str(text or "")
    for pattern in FORBIDDEN_PROMPT_PATTERNS:
        cleaned = pattern.sub("[private field removed]", cleaned)
    return cleaned
