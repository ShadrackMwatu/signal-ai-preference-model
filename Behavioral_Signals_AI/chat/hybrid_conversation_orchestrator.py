"""Hybrid conversational orchestration for Open Signals chat."""

from __future__ import annotations

import re
from typing import Any, Callable

from Behavioral_Signals_AI.chat.intents import detect_open_signals_intent
from Behavioral_Signals_AI.chat.persona import choose_tone, persona_context
from Behavioral_Signals_AI.chat.reference_resolver import resolve_short_followup
from Behavioral_Signals_AI.chat.response_synthesizer import PRIVATE_DATA_RESPONSE, synthesize_response
from Behavioral_Signals_AI.data_ingestion.privacy_filter import assert_no_private_fields
from Behavioral_Signals_AI.data_ingestion.retrieval_index import retrieve_relevant_context

FallbackHandler = Callable[[str, list[Any] | None, str, str, str], str]


def answer_with_hybrid_orchestrator(
    message: str,
    history: list[Any] | None,
    location: str,
    category: str,
    urgency: str,
    fallback_handler: FallbackHandler,
) -> str:
    """Plan and synthesize an Open Signals answer, delegating analytical work to fallback."""
    plan = build_response_plan(message, history, location, category, urgency)
    if plan["privacy_risk"]:
        return PRIVATE_DATA_RESPONSE
    if plan["response_mode"] in {"greeting", "identity", "capability", "small_talk", "gratitude", "farewell", "clarification"}:
        return synthesize_response(plan)
    fallback = fallback_handler(message, history, location, category, urgency)
    plan["fallback_answer_summary"] = _compact_text(fallback)
    return synthesize_response(plan, fallback)


def build_response_plan(
    message: str,
    history: list[Any] | None,
    location: str,
    category: str,
    urgency: str,
) -> dict[str, Any]:
    """Create an internal, non-user-visible response plan. No chain-of-thought is exposed."""
    prompt = str(message or "").strip()
    session_context = infer_session_context(history)
    detected = detect_open_signals_intent(prompt)
    resolved = resolve_short_followup(prompt, history, session_context)
    if resolved.get("resolved"):
        detected = {"intent": str(resolved.get("intent")), "confidence": float(resolved.get("confidence", 0.8))}
    privacy_risk = _privacy_risk(prompt)
    tone = choose_tone(prompt, detected["intent"], session_context)
    mode = _response_mode(prompt, detected["intent"], tone, session_context)
    needs_clarification = mode == "clarification"
    retrieved = [] if privacy_risk else retrieve_relevant_context(prompt, location or "Kenya", category or "All", limit=5)
    return {
        "intent": detected["intent"],
        "intent_confidence": detected.get("confidence", 0.0),
        "context_used": _context_used(session_context),
        "evidence_used": _evidence_summary(retrieved),
        "response_mode": mode,
        "tone": tone,
        "needs_clarification": needs_clarification,
        "privacy_risk": privacy_risk,
        "session_context": session_context,
        "retrieved_evidence": retrieved,
        "filters": {"location": location, "category": category, "urgency": urgency},
        "persona": persona_context(),
        "user_prompt": prompt,
    }


def infer_session_context(history: list[Any] | None) -> dict[str, str]:
    """Extract temporary session memory from visible chat history only."""
    context = {
        "last_response_opening": "",
        "last_response_mode": "",
        "last_signal_mentioned": "",
        "last_signal": "",
        "last_tone": "",
        "recent_phrases": "",
        "introduced_identity": "",
        "last_category": "",
        "last_county": "",
    }
    texts = _history_text_items(history)
    for text in texts[-8:]:
        safe = _strip_private_terms(text)
        opening = _opening(safe)
        if opening:
            context["last_response_opening"] = opening
        signal_match = re.search(r"Strongest relevant signal:\*\*\s*([^\n(]+)", safe, re.IGNORECASE)
        if signal_match:
            context["last_signal"] = signal_match.group(1).strip(" :.-")[:120]
            context["last_signal_mentioned"] = context["last_signal"]
            context["last_response_mode"] = "analytical"
        if "I'm Open Signals" in safe or "You are speaking with Open Signals" in safe:
            context["introduced_identity"] = "true"
            context["last_response_mode"] = "identity"
        county = _county_from_text(safe)
        if county:
            context["last_county"] = county
        category = _category_from_text(safe)
        if category:
            context["last_category"] = category
    context["recent_phrases"] = " | ".join(_opening(text) for text in texts[-3:] if text)
    return context


def _response_mode(prompt: str, intent: str, tone: str, session_context: dict[str, str]) -> str:
    text = _normalize(prompt)
    if intent == "greeting":
        return "greeting"
    if intent == "identity_query":
        return "identity"
    if intent == "capability_query" or intent == "help":
        return "capability"
    if intent in {"small_talk", "gratitude", "farewell"}:
        return intent
    if _is_vague(text) and not _has_context(session_context):
        return "clarification"
    if intent == "comparison_query":
        return "comparison_answer"
    if tone == "policy":
        return "policy_answer"
    if tone == "business":
        return "business_opportunity_answer"
    return "analytical_answer"


def _privacy_risk(prompt: str) -> bool:
    return not assert_no_private_fields({"prompt": prompt}) or bool(re.search(
        r"\b(user_id|device_id|phone|email|private message|exact location|gps|route|raw searches|raw likes|individual)\b",
        prompt or "",
        re.IGNORECASE,
    ))


def _has_context(session_context: dict[str, str]) -> bool:
    return bool(session_context.get("last_signal") or session_context.get("last_county") or session_context.get("last_category"))


def _is_vague(text: str) -> bool:
    return text in {"tell me more", "what about this", "explain", "show me", "what is happening", "more", "continue", "this", "that"}


def _context_used(session_context: dict[str, str]) -> str:
    used = []
    if session_context.get("last_signal"):
        used.append(f"last signal: {session_context['last_signal']}")
    if session_context.get("last_county"):
        used.append(f"county: {session_context['last_county']}")
    if session_context.get("last_category"):
        used.append(f"category: {session_context['last_category']}")
    return "; ".join(used) or "no prior signal context"


def _evidence_summary(records: list[dict[str, Any]]) -> str:
    if not records:
        return "no retrieved aggregate evidence"
    labels = []
    for record in records[:3]:
        labels.append(str(record.get("source_name") or record.get("source_type") or record.get("topic") or "aggregate evidence")[:80])
    return ", ".join(labels)


def _history_text_items(history: list[Any] | None) -> list[str]:
    items: list[str] = []
    for item in list(history or []):
        if isinstance(item, dict):
            items.append(str(item.get("content") or ""))
        elif isinstance(item, (tuple, list)):
            items.extend(str(part or "") for part in item[:2])
        else:
            items.append(str(item or ""))
    return items


def _county_from_text(text: str) -> str:
    for county in ["Nairobi", "Nakuru", "Makueni", "Mombasa", "Kisumu", "Kiambu", "Machakos"]:
        if county.lower() in str(text or "").lower():
            return county
    return ""


def _category_from_text(text: str) -> str:
    normalized = _normalize(text)
    mapping = {
        "food and agriculture": ["food", "agriculture", "maize", "fertilizer", "unga"],
        "jobs and labour market": ["jobs", "employment", "labour", "youth"],
        "transport": ["transport", "fuel", "logistics"],
        "housing": ["housing", "rent", "construction"],
        "water and sanitation": ["water", "sanitation"],
    }
    for category, terms in mapping.items():
        if any(term in normalized for term in terms):
            return category
    return ""


def _strip_private_terms(text: str) -> str:
    return re.sub(r"\b(user_id|device_id|phone|email|private_message|gps|route|exact location)\b", "[private field removed]", str(text or ""), flags=re.IGNORECASE)


def _opening(text: str) -> str:
    first = re.split(r"[.!?\n]", str(text or "").strip(), maxsplit=1)[0]
    return _normalize(first)[:100]


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())


def _compact_text(text: str) -> str:
    return " ".join(str(text or "").split())[:500]
