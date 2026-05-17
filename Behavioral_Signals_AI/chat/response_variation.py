"""Small response-variation helpers for Open Signals conversation."""

from __future__ import annotations

import re
from typing import Any


VARIATIONS: dict[str, list[str]] = {
    "greeting": [
        "Good morning. I’m here and ready to help.",
        "Hello. What would you like to talk through?",
        "Hi. I’m here with you.",
    ],
    "wellbeing": [
        "I’m doing well and ready to help.",
        "I’m good. Ready when you are.",
        "I’m doing fine, steady and listening.",
    ],
    "gratitude": [
        "You’re welcome.",
        "Anytime.",
        "Glad to help.",
    ],
    "affirmation": [
        "Okay.",
        "Got it.",
        "Understood.",
    ],
    "farewell": [
        "Goodbye. I’ll be here when you need me.",
        "Talk soon.",
        "Take care.",
    ],
    "transition": [
        "I can also help interpret current signals whenever you want.",
        "When useful, we can move from conversation into county or market signals.",
        "If you want, we can look at emerging risks or opportunities next.",
    ],
}


def varied_response(kind: str, session_context: dict[str, Any] | None = None, *, avoid_transition: bool = False) -> str:
    """Return a deterministic variation that avoids the previous opening phrase."""
    session = session_context or {}
    options = VARIATIONS.get(kind, ["I’m here."])
    previous = _opening(str(session.get("last_response_opening") or ""))
    seed = len(kind) + len(previous) + len(str(session.get("last_tone") or ""))
    choice = options[seed % len(options)]
    if previous and _opening(choice) == previous and len(options) > 1:
        choice = options[(seed + 1) % len(options)]
    if not avoid_transition and should_add_soft_transition(kind, session):
        choice = f"{choice} {VARIATIONS['transition'][seed % len(VARIATIONS['transition'])]}"
    return choice


def should_add_soft_transition(kind: str, session_context: dict[str, Any] | None = None) -> bool:
    """Occasionally bridge casual conversation toward Open Signals, without forcing it."""
    if kind not in {"greeting", "wellbeing"}:
        return False
    session = session_context or {}
    if session.get("last_response_mode") in {"analytical", "policy_answer", "business_opportunity_answer"}:
        return False
    recent = str(session.get("recent_phrases") or "")
    return len(recent) % 3 == 0


def _opening(text: str) -> str:
    first = re.split(r"[.!?\n]", str(text or "").strip(), maxsplit=1)[0]
    return " ".join(first.lower().split())[:80]
