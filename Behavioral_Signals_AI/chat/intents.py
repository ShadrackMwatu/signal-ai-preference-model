"""Lightweight intent detection for Open Signals chat."""

from __future__ import annotations

import re
from typing import TypedDict

from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS


class OpenSignalsIntent(TypedDict):
    intent: str
    confidence: float


ANALYSIS_KEYWORDS = {
    "risk", "risks", "opportunity", "opportunities", "signal", "signals", "county", "counties",
    "trend", "trends", "pressure", "affordability", "forecast", "demand", "unemployment",
    "fuel", "prices", "food", "water", "health", "transport", "jobs", "policy", "policymakers",
    "market", "business", "rising", "stronger", "changed", "persisted", "sector", "sectors",
    "stress", "inflation", "shortage", "shortages", "cost", "living", "urgency", "urgent",
    "monitor", "monitoring", "emerging", "persistent", "declining", "comparison",
}

ANALYSIS_PHRASES = [
    "food prices",
    "fuel prices",
    "cost of living",
    "market opportunity",
    "business opportunity",
    "policy concern",
    "county trend",
    "county signals",
    "demand signal",
    "affordability pressure",
    "economic pressure",
    "water access",
    "public services",
    "what is happening in",
    "show signals",
    "show risks",
    "show opportunities",
    "what should policymakers",
]

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
IDENTITY_PATTERNS = [
    r"\bwhat(?:'s| is) your name\b",
    r"\byour name\b",
    r"\bwho are you\b",
    r"\bare you (?:an? )?ai\b",
    r"\bare you artificial intelligence\b",
    r"\bexplain yourself\b",
    r"\bintroduce yourself\b",
]
CAPABILITY_PATTERNS = [
    r"\bwhat can you do\b",
    r"\bwhat do you do\b",
    r"\bwhat are you doing\b",
    r"\bcan you help(?: me)?\b",
    r"\bhow do you work\b",
    r"\bwhat can you analyze\b",
    r"\bwhat are signals\b",
    r"\bexplain signals\b",
    r"\bhow should i use\b",
    r"\bhow do i use\b",
]
SMALL_TALK_PATTERNS = [r"how are you", r"how are things", r"how is it going"]
AFFIRMATION_PATTERNS = [r"^ok$", r"^okay$", r"^alright$", r"^got it$", r"^sure$"]
HUMOR_PATTERNS = [r"\bjoke\b", r"\bmake me laugh\b", r"\bfunny\b"]
HELP_PATTERNS = [r"^help$", r"^help me$", r"\bhelp with open signals\b"]
FOLLOW_UP_PATTERNS = [
    r"what about", r"how about", r"why is that", r"why this", r"what does it show",
    r"what should .*do", r"what opportunity", r"why is .*rising",
]
COMPARISON_PATTERNS = [r"compare", r"different", r"stronger", r"versus", r"\bvs\b", r"which county"]
POLICY_PATTERNS = [r"policy", r"policymaker", r"government", r"county officials", r"monitor"]

LOW_CONFIDENCE_THRESHOLD = 0.65


def detect_open_signals_intent(message: str) -> OpenSignalsIntent:
    """Classify a prompt without using personal data or external services."""
    text = " ".join(str(message or "").strip().split())
    lowered = text.lower()
    if not lowered:
        return {"intent": "unclear_query", "confidence": 0.95}
    learned = _learned_override(text)
    if learned:
        return learned
    if lowered in {"who", "why", "meaning", "mean", "means", "how", "where"} or lowered.startswith("what about"):
        return {"intent": "short_followup", "confidence": 0.78}
    if _matches(lowered, GREETING_PATTERNS):
        return {"intent": "greeting", "confidence": 0.98}
    if _matches(lowered, FAREWELL_PATTERNS):
        return {"intent": "farewell", "confidence": 0.95}
    if _matches(lowered, GRATITUDE_PATTERNS):
        return {"intent": "gratitude", "confidence": 0.95}
    if _matches(lowered, AFFIRMATION_PATTERNS):
        return {"intent": "affirmation", "confidence": 0.94}
    if _matches(lowered, HUMOR_PATTERNS):
        return {"intent": "humor", "confidence": 0.9}
    if _matches(lowered, IDENTITY_PATTERNS):
        return {"intent": "identity_query", "confidence": 0.96}
    if _matches(lowered, CAPABILITY_PATTERNS):
        return {"intent": "capability_query", "confidence": 0.94}
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
    return {"intent": "unclear_query", "confidence": 0.55}


def _matches(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _mentions_county(text: str) -> bool:
    normalized = _normalize(text)
    return any(_normalize(option) in normalized for option in LOCATION_OPTIONS if option not in {"Global", "Kenya"})


def _contains_signal_keyword(text: str) -> bool:
    normalized = _normalize(text)
    if any(phrase in normalized for phrase in ANALYSIS_PHRASES):
        return True
    tokens = set(re.findall(r"[a-zA-Z]+", normalized))
    return bool(tokens.intersection({word.lower() for word in ANALYSIS_KEYWORDS | CATEGORY_TERMS}))


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())


def _learned_override(text: str) -> OpenSignalsIntent | None:
    try:
        from Behavioral_Signals_AI.chat.conversation_learning import get_learned_intent_override

        learned = get_learned_intent_override(text)
        if learned:
            return {"intent": str(learned["intent"]), "confidence": float(learned.get("confidence", 0.75))}
    except Exception:
        return None
    return None
