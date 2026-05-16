"""Resolve short Open Signals chat follow-ups using temporary session context."""

from __future__ import annotations

import re
from typing import Any


def resolve_short_followup(message: str, history: list[Any] | None, session_context: dict[str, str]) -> dict[str, Any]:
    """Map terse follow-ups to useful intents without storing personal data."""
    text = _normalize(message)
    if not text:
        return {"resolved": False, "intent": "", "confidence": 0.0}
    has_signal = bool(session_context.get("last_signal") or session_context.get("last_signal_topic"))
    has_place = bool(session_context.get("last_county"))
    last_intent = session_context.get("last_intent", "")
    recent = _recent_history_text(history)

    if text in {"who", "who?"}:
        if last_intent in {"greeting", "identity_query"} or _recent_is_conversational(recent):
            return _resolved("identity_query", 0.92)
        return _resolved("identity_query", 0.72)
    if text in {"why", "why?"}:
        return _resolved("explain_reason", 0.9) if has_signal else _unresolved("why_without_signal")
    if text in {"meaning", "meaning?", "mean", "means", "what meaning"}:
        return _resolved("explain_meaning", 0.9) if has_signal else _unresolved("meaning_without_signal")
    if text in {"how", "how?"}:
        return _resolved("explain_mechanism", 0.86) if has_signal else _unresolved("how_without_signal")
    if text in {"where", "where?"}:
        return _resolved("explain_geography", 0.86) if has_signal or has_place else _unresolved("where_without_signal")
    if text.startswith("what about"):
        entity = text.replace("what about", "", 1).strip(" ?")
        if entity:
            return {"resolved": True, "intent": "short_followup", "confidence": 0.82, "entity": entity}
        return _resolved("short_followup", 0.72) if has_signal or has_place else _unresolved("what_about_without_context")
    return {"resolved": False, "intent": "", "confidence": 0.0}


def _resolved(intent: str, confidence: float) -> dict[str, Any]:
    return {"resolved": True, "intent": intent, "confidence": confidence}


def _unresolved(reason: str) -> dict[str, Any]:
    return {"resolved": False, "intent": "short_followup", "confidence": 0.35, "reason": reason}


def _recent_history_text(history: list[Any] | None) -> str:
    parts: list[str] = []
    for item in list(history or [])[-4:]:
        if isinstance(item, dict):
            parts.append(str(item.get("content") or ""))
        elif isinstance(item, (tuple, list)):
            parts.extend(str(part or "") for part in item[:2])
        else:
            parts.append(str(item or ""))
    return _normalize(" ".join(parts))


def _recent_is_conversational(text: str) -> bool:
    return bool(re.search(r"\b(hello|i'm open signals|privacy-preserving|what would you like to explore)\b", text))


def _normalize(text: Any) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())
