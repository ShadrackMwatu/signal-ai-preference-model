"""Interactive aggregate-signal Q&A for Open Signals."""

from __future__ import annotations

import re
from typing import Any

from Behavioral_Signals_AI.geography.county_matcher import detect_county_from_text, signal_matches_location
from Behavioral_Signals_AI.llm.llm_client import complete_json
from Behavioral_Signals_AI.signal_engine.category_learning import category_matches_signal, get_category_options
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals
from Behavioral_Signals_AI.ui.feed_diff_engine import rank_signals_for_display

PRIVATE_DATA_RESPONSE = (
    "Open Signals only uses aggregate, anonymized, public, or user-authorized intelligence. "
    "It cannot identify individuals or expose private behavior."
)

FORBIDDEN_PROMPT_PATTERNS = [
    re.compile(r"\b(user_id|device_id|phone|email|private_message|personal_profile|exact location|gps|route|home address|work address|raw likes|raw comments|raw shares|raw searches|individual profile)\b", re.IGNORECASE),
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"\b(?:\+?254|0)?7\d{8}\b"),
]

CHAT_SYSTEM_PROMPT = (
    "You are Open Signals. Answer only from aggregate, anonymized, public, or user-authorized signal intelligence. "
    "Do not reveal raw searches, raw likes, raw comments, raw shares, personal identities, device IDs, exact personal locations, "
    "private movement traces, or individual profiles. Be concise and focus on demand, risks, opportunities, counties, and policy implications. "
    "Every answer must include strongest relevant signal, what it means, confidence level, county or scope, opportunity or risk, recommended action, "
    "and suggested follow-up prompts. Return JSON with one field: answer."
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
        return PRIVATE_DATA_RESPONSE

    effective_location = _location_from_question(cleaned) or location or "Kenya"
    effective_category = _category_from_question(cleaned) or category or "All"
    effective_urgency = urgency or "All"

    signals = _filtered_ranked_signals(effective_location, effective_category, effective_urgency)
    if not signals:
        return _no_signal_answer(effective_location, effective_category, effective_urgency)

    fallback_answer = _grounded_rule_based_answer(cleaned, signals, effective_location, effective_category, effective_urgency)
    payload = {
        "question": cleaned,
        "filters": {"location": effective_location, "category": effective_category, "urgency": effective_urgency},
        "required_answer_fields": [
            "strongest relevant signal",
            "what it means",
            "confidence level",
            "county or scope",
            "opportunity or risk",
            "recommended action",
            "suggested follow-up prompts",
        ],
        "signals": [_safe_signal(signal) for signal in signals[:6]],
        "history_turns": _safe_history(history),
        "privacy_boundary": "aggregate_interpreted_signals_only",
    }
    result = complete_json(CHAT_SYSTEM_PROMPT, payload, fallback={"answer": fallback_answer})
    answer = str(result.get("answer") or fallback_answer).strip()
    return _ensure_grounded_answer(_strip_private_terms(answer), signals[0], effective_location) or fallback_answer


def respond_open_signals_chat(message: str, history: list[Any] | None, location: str, category: str, urgency: str) -> tuple[list[Any], str]:
    """Gradio adapter that appends an Open Signals answer to chat history."""
    answer = answer_open_signals_prompt(message, history or [], location, category, urgency)
    updated_history = list(history or [])
    if updated_history and isinstance(updated_history[0], tuple):
        updated_history.append((str(message or "").strip(), answer))
    else:
        updated_history.append({"role": "user", "content": str(message or "").strip()})
        updated_history.append({"role": "assistant", "content": answer})
    return _trim_chat_history(updated_history), ""




def ask_strongest_signal_now(history: list[Any] | None, location: str, category: str, urgency: str) -> tuple[list[Any], str]:
    """Submit the strongest-signal prompt from the compact chip UI."""
    return respond_open_signals_chat("Strongest signal now", history, location, category, urgency)


def ask_county_risks(history: list[Any] | None, location: str, category: str, urgency: str) -> tuple[list[Any], str]:
    """Submit the county-risk prompt from the compact chip UI."""
    return respond_open_signals_chat("Show county risks", history, location, category, urgency)


def ask_opportunities(history: list[Any] | None, location: str, category: str, urgency: str) -> tuple[list[Any], str]:
    """Submit the opportunity prompt from the compact chip UI."""
    return respond_open_signals_chat("Show opportunities", history, location, category, urgency)


def ask_policy_monitoring(history: list[Any] | None, location: str, category: str, urgency: str) -> tuple[list[Any], str]:
    """Submit the policy-monitoring prompt from the compact chip UI."""
    return respond_open_signals_chat("What should policymakers monitor?", history, location, category, urgency)

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


def _grounded_rule_based_answer(question: str, signals: list[dict[str, Any]], location: str, category: str, urgency: str) -> str:
    top = _select_relevant_signal(question, signals)
    q = question.lower()
    if "opportun" in q or "market" in q or "business" in q:
        emphasis = _opportunity_sentence(top)
    elif "policy" in q or "policymaker" in q or "monitor" in q:
        emphasis = _policy_sentence(top)
    elif "risk" in q or "stress" in q:
        emphasis = _risk_sentence(top)
    else:
        emphasis = _meaning_sentence(top)
    return _format_grounded_answer(top, emphasis, location, category, urgency)


def _select_relevant_signal(question: str, signals: list[dict[str, Any]]) -> dict[str, Any]:
    words = {word for word in re.findall(r"[a-zA-Z]{4,}", question.lower()) if word not in {"what", "show", "signals", "signal", "about", "which", "should"}}
    if not words:
        return signals[0]
    best = signals[0]
    best_score = -1
    for signal in signals:
        blob = _signal_blob(signal)
        score = sum(1 for word in words if word in blob)
        if score > best_score:
            best = signal
            best_score = score
    return best


def _format_grounded_answer(signal: dict[str, Any], emphasis: str, location: str, category: str, urgency: str) -> str:
    topic = str(signal.get("signal_topic") or "current aggregate signal")
    signal_category = str(signal.get("signal_category") or category or "other")
    confidence = str(signal.get("confidence_score", "unknown"))
    scope = str(signal.get("county_name") or signal.get("geographic_scope") or location or "Kenya-wide")
    opportunity = str(signal.get("opportunity_level", "Moderate"))
    urgency_value = str(signal.get("urgency", urgency or "Medium"))
    risk = _risk_label(signal)
    action = str(signal.get("recommended_action") or signal.get("monitoring_recommendation") or "Monitor persistence, source confirmation, county spread, and outcome validation.")
    return (
        f"**Strongest relevant signal:** {topic} ({signal_category}).\n\n"
        f"**What it means:** {emphasis}\n\n"
        f"**Confidence level:** {confidence}% based on aggregate interpreted signal evidence, source validation, historical learning, and current ranking.\n\n"
        f"**County/scope:** {scope}.\n\n"
        f"**Opportunity or risk:** Opportunity is {opportunity}; urgency is {urgency_value}; risk signal is {risk}.\n\n"
        f"**Recommended action:** {action}\n\n"
        "**Suggested follow-up prompts:** Show risks | Show opportunities | Explain county relevance | What should policymakers do?"
    )


def _meaning_sentence(signal: dict[str, Any]) -> str:
    interpretation = signal.get("interpretation") or signal.get("plain_language_meaning")
    if interpretation:
        return str(interpretation)
    return (
        f"This appears to be a {signal.get('demand_level', 'Moderate').lower()} demand signal with "
        f"{signal.get('momentum', 'Stable').lower()} momentum and {signal.get('forecast_direction', 'Stable').lower()} forecast direction."
    )


def _opportunity_sentence(signal: dict[str, Any]) -> str:
    return (
        f"This signal may indicate a market or service opportunity where {signal.get('signal_category', 'the category')} demand is visible but still needs validation. "
        f"Opportunity level is {signal.get('opportunity_level', 'Moderate')} and unmet demand likelihood is {signal.get('unmet_demand_likelihood', 'Medium')}."
    )


def _policy_sentence(signal: dict[str, Any]) -> str:
    return (
        f"This is policy-relevant because it combines {signal.get('urgency', 'Medium')} urgency, "
        f"{signal.get('spread_risk', 'Low')} spread risk, and an outcome-learning note: "
        f"{signal.get('outcome_learning_note') or signal.get('historical_pattern_match') or 'evidence is still accumulating.'}"
    )


def _risk_sentence(signal: dict[str, Any]) -> str:
    return (
        f"The main risk is that {signal.get('signal_topic', 'this signal')} may reflect unresolved demand pressure, affordability pressure, or service stress. "
        f"Current urgency is {signal.get('urgency', 'Medium')} and spread risk is {signal.get('spread_risk', 'Low')}."
    )


def _risk_label(signal: dict[str, Any]) -> str:
    risk_parts = [
        f"{signal.get('unmet_demand_likelihood', 'Medium')} unmet demand",
        f"{signal.get('spread_risk', 'Low')} spread risk",
        f"{signal.get('forecast_direction', 'Stable')} forecast",
    ]
    return ", ".join(risk_parts)


def _location_from_question(question: str) -> str:
    detected = detect_county_from_text(question)
    county = detected.get("county_name", "")
    if county and county != "Kenya-wide":
        return county
    q = question.lower()
    if "global" in q:
        return "Global"
    if "kenya" in q or "national" in q:
        return "Kenya"
    return ""


def _category_from_question(question: str) -> str:
    normalized = _normalize(question)
    for option in get_category_options():
        if option == "All":
            continue
        if _normalize(option) in normalized:
            return option
    keyword_map = {
        "water and sanitation": ["water", "sanitation", "borehole"],
        "food and agriculture": ["food", "maize", "unga", "farm", "agriculture"],
        "jobs and labour market": ["jobs", "employment", "labour", "youth"],
        "trade and business": ["business", "market", "retail", "opportunity"],
        "health": ["health", "hospital", "clinic", "medicine"],
        "transport": ["transport", "traffic", "matatu", "fare"],
        "cost of living": ["cost", "prices", "affordability", "expensive"],
        "finance": ["finance", "credit", "loan", "sacco", "m-pesa", "mpesa"],
    }
    for category, terms in keyword_map.items():
        if any(term in normalized for term in terms):
            return category
    return ""


def _ensure_grounded_answer(answer: str, signal: dict[str, Any], location: str) -> str:
    required_markers = ["Strongest relevant signal", "What it means", "Confidence level", "County/scope", "Opportunity or risk", "Recommended action", "Suggested follow-up prompts"]
    if all(marker.lower() in answer.lower() for marker in required_markers):
        return answer
    return _format_grounded_answer(signal, answer or _meaning_sentence(signal), location, str(signal.get("signal_category", "All")), str(signal.get("urgency", "All")))


def _no_signal_answer(location: str, category: str, urgency: str) -> str:
    return (
        f"No matching aggregate signals are currently available for {location}, {category}, {urgency}.\n\n"
        "**Suggested follow-up prompts:** Show Kenya-wide signals | Show opportunities | What should policymakers do? | Explain county relevance"
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


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())


def _trim_chat_history(history: list[Any], max_messages: int = 8) -> list[Any]:
    """Keep the public chat compact while preserving recent context."""
    return list(history or [])[-max_messages:]
