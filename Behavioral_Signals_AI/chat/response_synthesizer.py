"""Response synthesis for hybrid Open Signals conversation."""

from __future__ import annotations

import re
from typing import Any

from Behavioral_Signals_AI.llm.open_signals_llm_orchestrator import generate_hybrid_open_signals_answer

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
    if plan.get("response_mode") in {"greeting", "identity", "capability", "small_talk", "gratitude", "farewell", "clarification"}:
        return fallback
    result = generate_hybrid_open_signals_answer(plan, fallback)
    return str(result.get("answer") or fallback).strip() or fallback


def _deterministic_response(plan: dict[str, Any]) -> str:
    mode = str(plan.get("response_mode") or "")
    tone = str(plan.get("tone") or "casual")
    session = plan.get("session_context", {}) if isinstance(plan.get("session_context"), dict) else {}
    if mode == "greeting":
        return _pick([
            "Hello - what would you like to explore today?",
            "Good morning. I can help you look at current signals, counties, risks, or opportunities.",
            "Hi. Tell me the county, sector, risk, or market opportunity you want to examine.",
        ], session, mode)
    if mode == "small_talk":
        return _pick([
            "I'm ready to help. I can look at current aggregate signals whenever you want.",
            "Doing well - ready to examine a county, sector, risk, or opportunity when you are.",
            "I'm here and ready to help interpret the signal picture.",
        ], session, mode)
    if mode == "identity":
        if session.get("introduced_identity"):
            return _pick([
                "I'm Open Signals. I help interpret aggregate Kenya signal intelligence without exposing private data.",
                "You are speaking with Open Signals, a privacy-preserving signal intelligence assistant for Kenya.",
            ], session, mode)
        return "I'm Open Signals - a privacy-preserving behavioral intelligence assistant for emerging risks, opportunities, demand patterns, and county trends in Kenya."
    if mode == "capability":
        return _pick([
            "I analyze emerging market pressure, affordability trends, and county-level behavioral signals.",
            "I can compare counties, explain why a signal matters, summarize opportunities, and outline policy monitoring priorities.",
            "I help interpret aggregate behavioral intelligence and evolving risks or opportunities.",
        ], session, mode)
    if mode == "gratitude":
        return "You're welcome. Ask about a county, sector, risk, or opportunity whenever you are ready."
    if mode == "farewell":
        return "Goodbye. I will be here when you want to explore Kenya signals again."
    if mode == "clarification":
        return _clarification(plan)
    if tone == "policy":
        return "I can answer that from the current aggregate signals, with policy relevance, uncertainty, and recommended monitoring."
    if tone == "business":
        return "I can frame that as a market opportunity using the current aggregate signal evidence."
    return "Here is what the current aggregate signal evidence suggests."


def _clarification(plan: dict[str, Any]) -> str:
    session = plan.get("session_context", {}) if isinstance(plan.get("session_context"), dict) else {}
    if session.get("last_signal"):
        return "Do you want me to explain why that signal matters, its likely meaning, or what action to take next?"
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
