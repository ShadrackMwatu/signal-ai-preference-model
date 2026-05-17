"""Hybrid conversational orchestration for Open Signals chat."""

from __future__ import annotations

import re
from typing import Any, Callable

from Behavioral_Signals_AI.chat.intents import detect_open_signals_intent
from Behavioral_Signals_AI.chat.conversation_learning import conversation_learning_hints
from Behavioral_Signals_AI.chat.general_conversation import analyze_general_conversation, is_general_conversation
from Behavioral_Signals_AI.chat.persona import choose_tone, persona_context
from Behavioral_Signals_AI.chat.reference_resolver import resolve_short_followup
from Behavioral_Signals_AI.chat.retrieval_grounding import retrieve_relevant_signals
from Behavioral_Signals_AI.chat.response_synthesizer import PRIVATE_DATA_RESPONSE, synthesize_response
from Behavioral_Signals_AI.chat.semantic_query_analyzer import analyze_open_signals_query, resolve_county_entity
from Behavioral_Signals_AI.data_ingestion.privacy_filter import assert_no_private_fields
from Behavioral_Signals_AI.data_ingestion.retrieval_index import retrieve_relevant_context
from Behavioral_Signals_AI.tools.tool_executor import execute_tool_plan
from Behavioral_Signals_AI.tools.tool_registry import list_tools
from Behavioral_Signals_AI.tools.tool_router import route_tools_for_prompt

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
    if plan["response_mode"] in {"greeting", "identity", "capability", "small_talk", "gratitude", "farewell", "affirmation", "wellbeing", "time_date", "creator_origin", "humor", "confusion", "general_conversation", "clarification"}:
        return synthesize_response(plan)
    effective_filters = plan.get("filters", {})
    fallback = fallback_handler(
        message,
        history,
        str(effective_filters.get("location") or location),
        str(effective_filters.get("category") or category),
        urgency,
    )
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
    learning_hints = conversation_learning_hints()
    general = analyze_general_conversation(prompt, history)
    semantic = analyze_open_signals_query(prompt)
    detected = detect_open_signals_intent(prompt)
    resolved = resolve_short_followup(prompt, history, session_context)
    if resolved.get("resolved"):
        detected = {"intent": str(resolved.get("intent")), "confidence": float(resolved.get("confidence", 0.8))}
    elif semantic["analytical"] and semantic["county"]:
        detected = {"intent": "signal_query", "confidence": max(float(detected.get("confidence", 0.0)), float(semantic["confidence"]))}
    privacy_risk = _privacy_risk(prompt)
    if is_general_conversation(general) and not semantic.get("analytical"):
        detected = {"intent": str(general["intent"]), "confidence": float(general["confidence"])}
    tone = _semantic_tone(prompt, detected["intent"], session_context, semantic, general)
    mode = _response_mode(prompt, detected["intent"], tone, session_context, semantic, general)
    needs_clarification = mode == "clarification"
    effective_location = str(semantic.get("county") or location or "Kenya")
    effective_category = str(semantic.get("category") or category or "All")
    retrieved = [] if privacy_risk else retrieve_relevant_context(prompt, effective_location, effective_category, limit=5)
    grounded_signals = [] if privacy_risk else retrieve_relevant_signals(
        str(semantic.get("county") or ""),
        effective_category,
        str(semantic.get("time_focus") or ""),
        session_context,
        limit=5,
    )
    tool_calls = [] if privacy_risk else route_tools_for_prompt(
        prompt,
        semantic,
        {"location": effective_location, "category": effective_category, "urgency": urgency},
        session_context,
    )
    tool_results = [] if privacy_risk else execute_tool_plan(tool_calls)
    if _tool_privacy_blocked(tool_results):
        privacy_risk = True
    return {
        "intent": detected["intent"],
        "intent_confidence": detected.get("confidence", 0.0),
        "context_used": _context_used(session_context),
        "evidence_used": _evidence_summary(retrieved, grounded_signals, tool_results),
        "response_mode": mode,
        "tone": tone,
        "needs_clarification": needs_clarification,
        "privacy_risk": privacy_risk,
        "session_context": session_context,
        "retrieved_evidence": retrieved,
        "grounded_signals": grounded_signals,
        "tool_calls": tool_calls,
        "tool_results": tool_results,
        "available_tools": list_tools(),
        "semantic_query": semantic,
        "general_conversation": general,
        "filters": {"location": effective_location, "category": effective_category, "urgency": urgency},
        "persona": persona_context(),
        "conversation_learning_hints": learning_hints,
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


def _response_mode(prompt: str, intent: str, tone: str, session_context: dict[str, str], semantic: dict[str, Any] | None = None, general: dict[str, Any] | None = None) -> str:
    text = _normalize(prompt)
    semantic = semantic or {}
    general = general or {}
    if is_general_conversation(general) and not semantic.get("analytical"):
        return _general_response_mode(str(general.get("intent") or intent))
    if semantic.get("analytical") and semantic.get("county"):
        if semantic.get("intent") == "policy":
            return "policy_answer"
        if semantic.get("intent") == "business":
            return "business_opportunity_answer"
        return "analytical_answer"
    if intent == "greeting":
        return "greeting"
    if intent in {"identity_query", "identity"}:
        return "identity"
    if intent in {"capability_query", "capability"} or intent == "help":
        return "capability"
    if intent in {"small_talk", "gratitude", "farewell", "affirmation", "wellbeing", "time_date", "creator_origin", "humor", "confusion"}:
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


def _semantic_tone(prompt: str, intent: str, session_context: dict[str, str], semantic: dict[str, Any], general: dict[str, Any] | None = None) -> str:
    if general and is_general_conversation(general) and not semantic.get("analytical"):
        return str(general.get("tone") or "casual")
    if semantic.get("intent") == "policy":
        return "policy"
    if semantic.get("intent") == "business":
        return "business"
    return choose_tone(prompt, intent, session_context)


def _general_response_mode(intent: str) -> str:
    mapping = {
        "casual_smalltalk": "general_conversation",
        "identity": "identity",
        "capability": "capability",
    }
    return mapping.get(intent, intent)


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


def _tool_privacy_blocked(tool_results: list[dict[str, Any]]) -> bool:
    for result in tool_results or []:
        if result.get("tool") == "privacy_check" and result.get("ok") and not result.get("data", {}).get("allowed", True):
            return True
    return False


def _evidence_summary(
    records: list[dict[str, Any]],
    grounded_signals: list[dict[str, Any]] | None = None,
    tool_results: list[dict[str, Any]] | None = None,
) -> str:
    labels = []
    for signal in list(grounded_signals or [])[:2]:
        labels.append(str(signal.get("signal_topic") or signal.get("source_summary") or "live signal cache")[:80])
    for result in list(tool_results or [])[:4]:
        if result.get("ok") and result.get("tool") != "privacy_check":
            labels.append(f"tool:{result.get('tool')}")
    if not records and not labels:
        return "no retrieved aggregate evidence"
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
    return resolve_county_entity(text)


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
