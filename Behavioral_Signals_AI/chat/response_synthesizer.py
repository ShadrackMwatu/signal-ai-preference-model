"""Response synthesis for hybrid Open Signals conversation."""

from __future__ import annotations

import re
from typing import Any

from Behavioral_Signals_AI.chat.answer_quality import evaluate_answer_quality, improve_answer_with_quality
from Behavioral_Signals_AI.chat.general_conversation import generate_general_conversation_response

PRIVATE_DATA_RESPONSE = (
    "Open Signals only uses aggregate, anonymized, public, or user-authorized intelligence. "
    "It cannot identify individuals or expose private behavior."
)


def synthesize_response(plan: dict[str, Any], fallback_answer: str = "") -> str:
    """Generate a privacy-safe response from a plan, using LLM if available and fallback otherwise."""
    if plan.get("privacy_risk"):
        return PRIVATE_DATA_RESPONSE
    if plan.get("needs_clarification"):
        return _clarification(plan)
    fallback = fallback_answer or _deterministic_response(plan)
    if plan.get("response_mode") in {"greeting", "identity", "capability", "small_talk", "gratitude", "farewell", "affirmation", "wellbeing", "time_date", "creator_origin", "humor", "confusion", "general_conversation", "clarification"}:
        return fallback
    from Behavioral_Signals_AI.llm.open_signals_llm_orchestrator import generate_hybrid_open_signals_answer

    result = generate_hybrid_open_signals_answer(plan, fallback)
    answer = str(result.get("answer") or fallback).strip() or fallback
    quality = evaluate_answer_quality(answer, plan)
    return improve_answer_with_quality(answer, plan, quality)


def _deterministic_response(plan: dict[str, Any]) -> str:
    mode = str(plan.get("response_mode") or "")
    tone = str(plan.get("tone") or "casual")
    session = plan.get("session_context", {}) if isinstance(plan.get("session_context"), dict) else {}
    hints = plan.get("conversation_learning_hints", {}) if isinstance(plan.get("conversation_learning_hints"), dict) else {}
    preferred_styles = hints.get("preferred_styles", {}) if isinstance(hints.get("preferred_styles"), dict) else {}
    preferred = str(preferred_styles.get(str(plan.get("intent") or "")) or "")
    if mode == "greeting":
        return generate_general_conversation_response(str(plan.get("user_prompt") or ""), {"intent": "greeting"}, session)
    if mode in {"small_talk", "general_conversation"}:
        if preferred == "capability_query":
            return "I can help when you are ready - ask me about a county, signal, risk, or opportunity."
        return generate_general_conversation_response(str(plan.get("user_prompt") or ""), plan.get("general_conversation", {"intent": "casual_smalltalk"}), session)
    if mode in {"wellbeing", "time_date", "creator_origin", "affirmation", "humor", "confusion"}:
        return generate_general_conversation_response(str(plan.get("user_prompt") or ""), {"intent": mode}, session)
    if mode == "identity":
        return generate_general_conversation_response(str(plan.get("user_prompt") or ""), {"intent": "identity"}, session)
    if mode == "capability":
        return generate_general_conversation_response(str(plan.get("user_prompt") or ""), {"intent": "capability"}, session)
    if mode == "gratitude":
        return generate_general_conversation_response(str(plan.get("user_prompt") or ""), {"intent": "gratitude"}, session)
    if mode == "farewell":
        return generate_general_conversation_response(str(plan.get("user_prompt") or ""), {"intent": "farewell"}, session)
    if mode == "clarification":
        return _clarification(plan)
    if tone == "policy":
        return "I can answer that from the current aggregate signals, with policy relevance, uncertainty, and recommended monitoring."
    if tone == "business":
        return "I can frame that as a market opportunity using the current aggregate signal evidence."
    return "Here is what the current aggregate signal evidence suggests."


def _clarification(plan: dict[str, Any]) -> str:
    session = plan.get("session_context", {}) if isinstance(plan.get("session_context"), dict) else {}
    hints = plan.get("conversation_learning_hints", {}) if isinstance(plan.get("conversation_learning_hints"), dict) else {}
    if session.get("last_signal"):
        return "Do you want me to explain why that signal matters, its likely meaning, or what action to take next?"
    if hints.get("preferred_clarification_focus") == "county_or_category":
        return "Should I focus on a specific county, category, or the strongest current signal?"
    return _pick([
        "Do you want the strongest current signal, a specific county, or a market opportunity?",
        "Should I focus on a county, a sector, a risk, or an opportunity?",
        "Tell me whether you want a county view, a market opportunity, or the main signal right now.",
    ], session, "clarification")


def _pick(options: list[str], session: dict[str, Any], key: str) -> str:
    previous = _opening(str(session.get("last_response_opening") or session.get("previous_opening_phrase") or ""))
    seed = len(key) + len(previous) + len(str(session.get("last_signal") or ""))
    choice = options[seed % len(options)]
    if previous and _opening(choice) == previous and len(options) > 1:
        choice = options[(seed + 1) % len(options)]
    return choice


def _opening(text: str) -> str:
    first = re.split(r"[.!?\n]", str(text or "").strip(), maxsplit=1)[0]
    return " ".join(first.lower().split())[:80]
