"""Aggregate-only conversation learning for Open Signals chat.

This module records broad interaction patterns so Open Signals can improve
clarification, response mode selection, proactive suggestions, and county or
category relevance without storing personal user data.
"""

from __future__ import annotations

import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.chat.intents import detect_open_signals_intent
from Behavioral_Signals_AI.data_ingestion.privacy_filter import assert_no_private_fields
from Behavioral_Signals_AI.geography.county_matcher import detect_county_from_text
from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS
from Behavioral_Signals_AI.signal_engine.category_learning import get_category_options
from Behavioral_Signals_AI.storage.storage_manager import read_json, write_json

DEFAULT_CONVERSATION_LEARNING_PATH = Path("Behavioral_Signals_AI/outputs/conversation_learning_summary.json")

PRIVATE_RESPONSE_MARKER = "cannot identify individuals or expose private behavior"
CLARIFICATION_MARKERS = [
    "do you want me to explain",
    "should i focus on",
    "tell me whether you want",
    "could you clarify",
    "specific county",
]
FALLBACK_MARKERS = [
    "fallback aggregate intelligence",
    "sample aggregate signal",
    "evidence is limited",
    "not enough current aggregate evidence",
    "limited current aggregate evidence",
]
LOW_QUALITY_MARKERS = [
    "evidence is limited",
    "i may not have enough context",
    "treat this as indicative",
]


def record_conversation_interaction(
    message: str,
    answer: str,
    history: list[Any] | None,
    location: str,
    category: str,
    urgency: str,
    *,
    path: str | Path | None = None,
) -> dict[str, Any]:
    """Update aggregate chat-learning memory from a single interaction."""
    prompt = str(message or "").strip()
    response = str(answer or "")
    summary_path = Path(path) if path else _conversation_learning_path()
    summary = read_json(summary_path, _empty_summary())
    if not isinstance(summary, dict):
        summary = _empty_summary()

    intent = detect_open_signals_intent(prompt)["intent"]
    mode = _response_mode(intent, prompt, response)
    county = _requested_county(prompt, location)
    selected_category = _requested_category(prompt, category)

    summary["schema_version"] = 1
    summary["updated_at"] = datetime.now(UTC).isoformat()
    summary["total_interactions"] = int(summary.get("total_interactions", 0)) + 1
    _increment(summary.setdefault("common_prompt_types", {}), intent)
    _increment(summary.setdefault("most_requested_response_modes", {}), mode)
    if county:
        _increment(summary.setdefault("most_requested_counties", {}), county)
    if selected_category and selected_category != "All":
        _increment(summary.setdefault("most_requested_categories", {}), selected_category)
    if _is_unclear_or_clarification(intent, response):
        summary["unclear_prompt_frequency"] = int(summary.get("unclear_prompt_frequency", 0)) + 1
        summary["clarification_count"] = int(summary.get("clarification_count", 0)) + 1
    if _is_privacy_refusal(prompt, response):
        summary["privacy_refusal_count"] = int(summary.get("privacy_refusal_count", 0)) + 1
    if _is_fallback_answer(response):
        summary["fallback_answer_count"] = int(summary.get("fallback_answer_count", 0)) + 1
    if _is_low_quality_answer(response):
        summary["low_quality_answer_count"] = int(summary.get("low_quality_answer_count", 0)) + 1

    summary["learning_hints"] = _learning_hints(summary)
    if _debug_enabled():
        _append_debug_prompt(summary, prompt)
    else:
        summary.pop("debug_raw_prompts", None)

    write_json(summary_path, summary)
    return summary


def get_conversation_learning_summary(path: str | Path | None = None) -> dict[str, Any]:
    """Read aggregate conversation-learning memory, initializing it if needed."""
    summary_path = Path(path) if path else _conversation_learning_path()
    summary = read_json(summary_path, _empty_summary())
    return summary if isinstance(summary, dict) else _empty_summary()


def conversation_learning_hints(path: str | Path | None = None) -> dict[str, Any]:
    """Return compact hints that other chat modules can use without raw prompts."""
    summary = get_conversation_learning_summary(path)
    return dict(summary.get("learning_hints") or _learning_hints(summary))


def _empty_summary() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "updated_at": "",
        "total_interactions": 0,
        "common_prompt_types": {},
        "unclear_prompt_frequency": 0,
        "privacy_refusal_count": 0,
        "fallback_answer_count": 0,
        "low_quality_answer_count": 0,
        "clarification_count": 0,
        "most_requested_counties": {},
        "most_requested_categories": {},
        "most_requested_response_modes": {},
        "learning_hints": {
            "preferred_clarification_focus": "county_or_signal",
            "proactive_county_focus": "",
            "proactive_category_focus": "",
            "response_mode_bias": "balanced",
        },
    }


def _conversation_learning_path() -> Path:
    return Path(os.getenv("SIGNAL_CONVERSATION_LEARNING_PATH", str(DEFAULT_CONVERSATION_LEARNING_PATH)))


def _response_mode(intent: str, prompt: str, answer: str) -> str:
    text = _normalize(prompt)
    response = _normalize(answer)
    if _is_privacy_refusal(prompt, answer):
        return "privacy_refusal"
    if intent in {"greeting", "identity_query", "capability_query", "small_talk", "gratitude", "farewell", "help"}:
        return intent
    if "compare" in text or "county comparison" in response:
        return "comparison_answer"
    if "policy" in text or "policymaker" in text or "policy signal" in response:
        return "policy_answer"
    if "business" in text or "opportunity" in text or "market opportunity signal" in response:
        return "business_opportunity_answer"
    if _is_unclear_or_clarification(intent, answer):
        return "clarification"
    return "analytical_answer"


def _requested_county(prompt: str, selected_location: str) -> str:
    detected = detect_county_from_text(str(prompt or "")).get("county_name", "")
    if detected and detected != "Kenya-wide":
        return str(detected)
    location = str(selected_location or "")
    if location in LOCATION_OPTIONS and location not in {"Global", "Kenya"}:
        return location
    normalized_prompt = _normalize(prompt)
    for option in LOCATION_OPTIONS:
        if option in {"Global", "Kenya"}:
            continue
        if _normalize(option) in normalized_prompt:
            return option
    return ""


def _requested_category(prompt: str, selected_category: str) -> str:
    normalized_prompt = _normalize(prompt)
    for option in get_category_options():
        if option == "All":
            continue
        if _normalize(option) in normalized_prompt:
            return option
    category = str(selected_category or "All")
    return category if category != "All" else ""


def _is_unclear_or_clarification(intent: str, answer: str) -> bool:
    response = _normalize(answer)
    return intent in {"unclear_query", "short_followup"} or any(marker in response for marker in CLARIFICATION_MARKERS)


def _is_privacy_refusal(prompt: str, answer: str) -> bool:
    response = _normalize(answer)
    if PRIVATE_RESPONSE_MARKER in response:
        return True
    return not assert_no_private_fields({"prompt": str(prompt or "")})


def _is_fallback_answer(answer: str) -> bool:
    response = _normalize(answer)
    return any(marker in response for marker in FALLBACK_MARKERS)


def _is_low_quality_answer(answer: str) -> bool:
    response = _normalize(answer)
    return any(marker in response for marker in LOW_QUALITY_MARKERS)


def _learning_hints(summary: dict[str, Any]) -> dict[str, Any]:
    counties = summary.get("most_requested_counties") or {}
    categories = summary.get("most_requested_categories") or {}
    modes = summary.get("most_requested_response_modes") or {}
    total = max(int(summary.get("total_interactions", 0)), 1)
    clarification_rate = int(summary.get("clarification_count", 0)) / total
    fallback_rate = int(summary.get("fallback_answer_count", 0)) / total
    mode_bias = "clarify_first" if clarification_rate >= 0.35 else "evidence_cautious" if fallback_rate >= 0.35 else "balanced"
    return {
        "preferred_clarification_focus": "county_or_category" if clarification_rate >= 0.25 else "county_or_signal",
        "proactive_county_focus": _top_key(counties),
        "proactive_category_focus": _top_key(categories),
        "response_mode_bias": mode_bias,
        "top_response_mode": _top_key(modes),
    }


def _append_debug_prompt(summary: dict[str, Any], prompt: str) -> None:
    safe_prompt = _redact_prompt(prompt)
    prompts = list(summary.get("debug_raw_prompts") or [])[-19:]
    prompts.append({"timestamp": datetime.now(UTC).isoformat(), "prompt": safe_prompt})
    summary["debug_raw_prompts"] = prompts


def _redact_prompt(prompt: str) -> str:
    redacted = str(prompt or "")[:500]
    redacted = re.sub(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b", "[email removed]", redacted)
    redacted = re.sub(r"\b(?:\+?254|0)?7\d{8}\b", "[phone removed]", redacted)
    redacted = re.sub(
        r"\b(user_id|device_id|imei|private_message|personal_profile|exact location|gps|route|home address|work address)\b",
        "[private field removed]",
        redacted,
        flags=re.IGNORECASE,
    )
    return redacted


def _increment(counter: dict[str, int], key: str) -> None:
    clean_key = str(key or "").strip() or "unknown"
    counter[clean_key] = int(counter.get(clean_key, 0)) + 1


def _top_key(counter: dict[str, Any]) -> str:
    if not counter:
        return ""
    return str(max(counter.items(), key=lambda item: int(item[1]))[0])


def _debug_enabled() -> bool:
    return str(os.getenv("SIGNAL_DEBUG_CONVERSATION_LEARNING", "")).lower() in {"1", "true", "yes"}


def _normalize(text: Any) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())
