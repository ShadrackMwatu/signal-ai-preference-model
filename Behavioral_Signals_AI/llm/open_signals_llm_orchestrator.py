"""LLM orchestration for retrieval-grounded Open Signals answers."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.ai_platform.safety_layer import sanitize_context
from Behavioral_Signals_AI.llm.llm_client import complete_json
from Behavioral_Signals_AI.llm.open_signals_system_prompt import OPEN_SIGNALS_SYSTEM_PROMPT


def generate_open_signals_llm_answer(mode: str, context: dict[str, Any], fallback_answer: str) -> dict[str, Any]:
    """Call the optional LLM with summarized aggregate context, otherwise return fallback."""
    payload = {
        "response_mode": mode,
        "context": summarize_context_for_llm(context),
        "instructions": [
            "Answer conversationally and concisely.",
            "Ground the answer in aggregate Open Signals context only.",
            "Mention uncertainty when context is limited.",
            "Never expose private data, raw individual behavior, device IDs, routes, or identities.",
        ],
        "required_output": {"answer": "string"},
    }
    return complete_json(OPEN_SIGNALS_SYSTEM_PROMPT, sanitize_context(payload), fallback={"answer": fallback_answer})


def generate_hybrid_open_signals_answer(plan: dict[str, Any], fallback_answer: str) -> dict[str, Any]:
    """Generate a concise hybrid chat answer from a privacy-safe response plan."""
    payload = {
        "persona": plan.get("persona", {}),
        "user_prompt": plan.get("user_prompt", ""),
        "response_plan": {
            "intent": plan.get("intent"),
            "response_mode": plan.get("response_mode"),
            "tone": plan.get("tone"),
            "context_used": plan.get("context_used"),
            "evidence_used": plan.get("evidence_used"),
        },
        "session_context": plan.get("session_context", {}),
        "retrieved_aggregate_evidence": list(plan.get("retrieved_evidence", []) or [])[:5],
        "privacy_rules": [
            "Use aggregate, anonymized, public, or user-authorized signal intelligence only.",
            "Do not reveal raw searches, likes, comments, individual mobility, device IDs, exact personal locations, or private data.",
            "Do not invent unsupported signals.",
            "Keep the answer concise, natural, and grounded.",
        ],
        "fallback_answer": fallback_answer,
        "required_output": {"answer": "string"},
    }
    return complete_json(OPEN_SIGNALS_SYSTEM_PROMPT, sanitize_context(payload), fallback={"answer": fallback_answer})


def summarize_context_for_llm(context: dict[str, Any]) -> dict[str, Any]:
    signals = list(context.get("aggregate_live_signals", []) or [])[:5]
    memory = context.get("memory_context", {}) if isinstance(context.get("memory_context"), dict) else {}
    return sanitize_context({
        "question": context.get("question", ""),
        "intent": context.get("intent", {}),
        "filters": context.get("filters", {}),
        "session_context": context.get("session_context", {}),
        "top_signals": signals,
        "memory_summary": {
            "historical_count": len(memory.get("historical", []) or []),
            "outcome_count": len(memory.get("outcomes", []) or []),
            "geospatial_count": len(memory.get("geospatial", []) or []),
            "behavioral_count": len(memory.get("behavioral", []) or []),
            "evaluation_metrics": memory.get("evaluation_metrics", {}),
        },
        "retrieved_evidence": list(context.get("retrieved_evidence", []) or [])[:5],
        "privacy_boundary": context.get("privacy_boundary"),
    })
