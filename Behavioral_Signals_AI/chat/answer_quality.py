"""Answer-quality evaluation for Open Signals chat responses."""

from __future__ import annotations

import os
import re
from typing import Any

QUALITY_DIMENSIONS = [
    "evidence_grounding",
    "relevance_to_prompt",
    "privacy_safety",
    "clarity",
    "actionability",
    "confidence_alignment",
]


def evaluate_answer_quality(answer: str, plan: dict[str, Any]) -> dict[str, Any]:
    """Score an answer before returning it; scores are internal unless debug is enabled."""
    prompt = str(plan.get("user_prompt") or "")
    answer_text = str(answer or "")
    scores = {
        "evidence_grounding": _score_evidence(answer_text, plan),
        "relevance_to_prompt": _score_relevance(prompt, answer_text, plan),
        "privacy_safety": _score_privacy(answer_text),
        "clarity": _score_clarity(answer_text),
        "actionability": _score_actionability(answer_text, plan),
        "confidence_alignment": _score_confidence_alignment(answer_text, plan),
    }
    overall = round(sum(scores.values()) / len(scores), 2)
    return {
        "scores": scores,
        "overall": overall,
        "is_low_quality": overall < 70 or min(scores.values()) < 50,
        "needs_clarification": scores["relevance_to_prompt"] < 45,
        "weak_evidence": scores["evidence_grounding"] < 55 or "no retrieved aggregate evidence" in str(plan.get("evidence_used", "")).lower(),
    }


def improve_answer_with_quality(answer: str, plan: dict[str, Any], quality: dict[str, Any]) -> str:
    """Soften or clarify low-quality analytical answers without exposing internal scores."""
    if plan.get("privacy_risk"):
        return (
            "Open Signals only uses aggregate, anonymized, public, or user-authorized intelligence. "
            "It cannot identify individuals or expose private behavior."
        )
    if not quality.get("is_low_quality"):
        return _debug_suffix(answer, quality)
    cautious = str(answer or "").strip()
    if quality.get("weak_evidence") and "evidence is limited" not in cautious.lower():
        cautious = (
            "Evidence is limited, so treat this as indicative rather than confirmed. "
            + cautious
        )
    elif quality.get("needs_clarification"):
        return _debug_suffix(
            "I may not have enough context to answer that well. Do you want a specific county, sector, signal, or opportunity view?",
            quality,
        )
    if "monitor" not in cautious.lower():
        cautious += "\n\nRecommended next step: monitor for fresher aggregate evidence before making a strong conclusion."
    return _debug_suffix(cautious, quality)


def _score_evidence(answer: str, plan: dict[str, Any]) -> float:
    text = answer.lower()
    evidence = str(plan.get("evidence_used") or "").lower()
    if "evidence basis" in text or "validation" in text:
        return 92
    if evidence and "no retrieved aggregate evidence" not in evidence:
        return 75
    if plan.get("response_mode") in {"greeting", "identity", "capability", "small_talk", "gratitude", "farewell"}:
        return 80
    return 40


def _score_relevance(prompt: str, answer: str, plan: dict[str, Any]) -> float:
    if plan.get("needs_clarification"):
        return 70
    prompt_terms = _terms(prompt)
    answer_terms = _terms(answer)
    if not prompt_terms:
        return 80
    overlap = len(prompt_terms.intersection(answer_terms))
    if overlap:
        return min(95, 55 + overlap * 12)
    if plan.get("response_mode") in str(answer).lower():
        return 65
    return 35


def _score_privacy(answer: str) -> float:
    forbidden = re.compile(r"\b(user_id|device_id|phone|email|private message|exact location|gps|route|raw searches|raw likes|individual profile)\b", re.IGNORECASE)
    return 25 if forbidden.search(answer or "") else 100


def _score_clarity(answer: str) -> float:
    words = str(answer or "").split()
    if not words:
        return 0
    if len(words) <= 180:
        return 90
    if len(words) <= 260:
        return 75
    return 55


def _score_actionability(answer: str, plan: dict[str, Any]) -> float:
    if plan.get("response_mode") in {"greeting", "identity", "capability", "small_talk", "gratitude", "farewell"}:
        return 80
    text = answer.lower()
    return 90 if any(term in text for term in ["recommended", "monitor", "should", "next step", "action"]) else 55


def _score_confidence_alignment(answer: str, plan: dict[str, Any]) -> float:
    text = answer.lower()
    weak_evidence = "no retrieved aggregate evidence" in str(plan.get("evidence_used", "")).lower()
    if weak_evidence and any(term in text for term in ["confirmed", "certain", "definitely"]):
        return 35
    if weak_evidence and any(term in text for term in ["limited", "indicative", "monitor", "uncertain"]):
        return 85
    return 80


def _terms(text: str) -> set[str]:
    stop = {"what", "which", "should", "about", "show", "tell", "explain", "signal", "signals"}
    return {term for term in re.findall(r"[a-zA-Z]{4,}", str(text or "").lower()) if term not in stop}


def _debug_suffix(answer: str, quality: dict[str, Any]) -> str:
    if os.getenv("SIGNAL_DEBUG_CHAT_QUALITY", "").lower() not in {"1", "true", "yes"}:
        return answer
    return f"{answer}\n\n[debug answer quality: {quality}]"
