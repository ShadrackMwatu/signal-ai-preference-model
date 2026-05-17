"""Open Signals conversational persona and tone selection."""

from __future__ import annotations

import re
from typing import Any

OPEN_SIGNALS_PERSONA = {
    "name": "Open Signals",
    "traits": [
        "calm",
        "analytical",
        "helpful",
        "privacy-preserving",
        "policy-aware",
        "market-aware",
        "not alarmist",
        "conversational before analytical",
    ],
    "privacy_boundary": "aggregate_anonymized_public_or_user_authorized_only",
}

TONE_MODES = {"casual", "analytical", "policy", "business", "exploratory", "clarification"}


def choose_tone(message: str, intent: str, session_context: dict[str, Any] | None = None) -> str:
    """Choose a compact tone mode from user wording and intent."""
    text = " ".join(str(message or "").lower().replace("_", " ").split())
    if intent in {"greeting", "farewell", "gratitude", "small_talk", "identity_query", "capability_query"}:
        return "casual"
    if intent in {"unclear_query", "short_followup"}:
        return "clarification"
    if re.search(r"\b(policy|policymaker|government|public sector|monitor)\b", text):
        return "policy"
    if re.search(r"\b(business|opportunity|market|investment|enterprise|sme)\b", text):
        return "business"
    if re.search(r"\b(explore|what about|tell me more|show me)\b", text):
        return "exploratory"
    return "analytical"


def persona_context() -> dict[str, Any]:
    """Return privacy-safe persona context for optional LLM prompting."""
    return dict(OPEN_SIGNALS_PERSONA)
