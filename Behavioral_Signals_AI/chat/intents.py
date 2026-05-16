"""Lightweight intent detection for Open Signals chat."""

from __future__ import annotations

import re
from typing import TypedDict

from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS


class OpenSignalsIntent(TypedDict):
    intent: str
    confidence: float


SIGNAL_KEYWORDS = {
    "what", "show", "explain", "compare", "risk", "risks", "opportunity", "opportunities",
    "signal", "signals", "county", "counties", "trend", "trends", "pressure", "affordability",
    "forecast", "demand", "unemployment", "fuel", "prices", "food", "water", "health",
    "transport", "jobs", "policy", "policymakers", "market", "business", "rising", "stronger",
    "changed", "persisted", "sector", "sectors", "stress", "Nairobi", "Nakuru", "Makueni",
}

CATEGORY_TERMS = {
    "food", "agriculture", "jobs", "labour", "housing", "health", "transport", "energy",
    "technology", "education", "finance", "water", "sanitation", "climate", "environment",
    "cost", "living", "trade", "business", "security", "governance", "ceramics",
}

GREETING_PATTERNS = [
    r"^hi+$", r"^hello+$", r"^hey+$", r"^good morning", r"^good afternoon", r"^good evening",
    r"^habari", r"^sasa$",
]
FAREWELL_PATTERNS = [r"^bye$", r"^goodbye$", r"^see you", r"^later$"]
GRATITUDE_PATTERNS = [r"^thanks?$", r"^thank you", r"^asante"]
SMALL_TALK_PATTERNS = [r"how are you", r"how are things", r"who are you"]
HELP_PATTERNS = [r"what can you do", r"help$", r"help me", r"how do i use", r"what do you do"]
FOLLOW_UP_PATTERNS = [r"what about", r"how about", r"why is that", r"why this", r"what does it show", r"what should .*do", r"what opportunity", r"why is .*rising"]
COMPARISON_PATTERNS = [r"compare", r"different", r"stronger", r"versus", r"\bvs\b", r"which county"]
POLICY_PATTERNS = [r"policy", r"policymaker", r"government", r"county officials", r"monitor"]


def detect_open_signals_intent(message: str) -> OpenSignalsIntent:
    """Classify a prompt without using personal data or external services."""
    text = " ".join(str(message or "").strip().split())
    lowered = text.lower()
    if not lowered:
        return {"intent": "unclear_query", "confidence": 0.95}
    if _matches(lowered, GREETING_PATTERNS):
        return {"intent": "greeting", "confidence": 0.98}
    if _matches(lowered, FAREWELL_PATTERNS):
        return {"intent": "farewell", "confidence": 0.95}
    if _matches(lowered, GRATITUDE_PATTERNS):
        return {"intent": "gratitude", "confidence": 0.95}
    if _matches(lowered, HELP_PATTERNS):
        return {"intent": "help", "confidence": 0.92}
    if _matches(lowered, SMALL_TALK_PATTERNS):
        return {"intent": "small_talk", "confidence": 0.9}
    if _matches(lowered, COMPARISON_PATTERNS):
        return {"intent": "comparison_query", "confidence": 0.9}
    if _matches(lowered, POLICY_PATTERNS):
        return {"intent": "policy_query", "confidence": 0.86}
    if _matches(lowered, FOLLOW_UP_PATTERNS):
        return {"intent": "follow_up_query", "confidence": 0.84}
    if _mentions_county(lowered) or _contains_signal_keyword(lowered):
        return {"intent": "signal_query", "confidence": 0.82}
    if len(lowered.split()) <= 3:
        return {"intent": "unclear_query", "confidence": 0.75}
    return {"intent": "small_talk", "confidence": 0.55}


def _matches(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _mentions_county(text: str) -> bool:
    normalized = _normalize(text)
    return any(_normalize(option) in normalized for option in LOCATION_OPTIONS if option not in {"Global", "Kenya"})


def _contains_signal_keyword(text: str) -> bool:
    tokens = set(re.findall(r"[a-zA-Z]+", text))
    return bool(tokens.intersection({word.lower() for word in SIGNAL_KEYWORDS | CATEGORY_TERMS}))


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())
