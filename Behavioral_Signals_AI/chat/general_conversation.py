"""General conversational intelligence for Open Signals chat."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from Behavioral_Signals_AI.chat.response_variation import varied_response

GENERAL_CONVERSATION_INTENTS = {
    "greeting",
    "farewell",
    "gratitude",
    "identity",
    "capability",
    "wellbeing",
    "casual_smalltalk",
    "time_date",
    "creator_origin",
    "affirmation",
    "confusion",
    "humor",
    "analytical",
    "policy",
    "opportunity",
    "risk",
    "comparison",
    "forecast",
}


def analyze_general_conversation(message: str, history: list[Any] | None = None) -> dict[str, Any]:
    """Classify a prompt as general conversation or domain analysis."""
    text = str(message or "").strip()
    normalized = _normalize(text)
    if not normalized:
        return _result("confusion", False, 0.9, "casual")
    if _is_analytical(normalized):
        return _result(_analytical_intent(normalized), True, 0.88, _tone_for_analytical(normalized))
    if re.search(r"^(hi+|hello|hey|good morning|good afternoon|good evening|habari|sasa)\b", normalized):
        return _result("greeting", False, 0.98, "casual")
    if re.search(r"\b(thanks|thank you|asante)\b", normalized):
        return _result("gratitude", False, 0.96, "casual")
    if normalized in {"ok", "okay", "alright", "sure", "yes", "yeah", "fine", "got it"}:
        return _result("affirmation", False, 0.95, "casual")
    if re.search(r"\b(bye|goodbye|see you|later)\b", normalized):
        return _result("farewell", False, 0.95, "casual")
    if re.search(r"\b(how are you|how are things|how is it going|uko aje)\b", normalized):
        return _result("wellbeing", False, 0.96, "casual")
    if re.search(r"\b(today|date|which day|what day|weekday|day is it|time)\b", normalized):
        return _result("time_date", False, 0.9, "casual")
    if re.search(r"\b(who made you|who created you|creator|where did you come from|origin)\b", normalized):
        return _result("creator_origin", False, 0.92, "casual")
    if re.search(r"\b(who are you|what are you|what is your name|your name|are you ai)\b", normalized):
        return _result("identity", False, 0.95, "casual")
    if re.search(r"\b(what can you do|what do you do|how do you work|can you help|what are you doing)\b", normalized):
        return _result("capability", False, 0.9, "casual")
    if re.search(r"\b(joke|make me laugh|funny)\b", normalized):
        return _result("humor", False, 0.9, "casual")
    if normalized in {"hmm", "uh", "what", "i dont understand", "confused"}:
        return _result("confusion", False, 0.78, "clarification")
    return _result("casual_smalltalk", False, 0.58, "casual")


def is_general_conversation(analysis: dict[str, Any]) -> bool:
    """Return true when the prompt should not be forced into signal analysis."""
    return not bool(analysis.get("analytical")) and str(analysis.get("intent")) in GENERAL_CONVERSATION_INTENTS


def generate_general_conversation_response(
    message: str,
    analysis: dict[str, Any],
    session_context: dict[str, str] | None = None,
) -> str:
    """Generate a direct, lightweight response for general conversation."""
    intent = str(analysis.get("intent") or "casual_smalltalk")
    session = session_context or {}
    if intent == "greeting":
        return varied_response("greeting", session)
    if intent == "wellbeing":
        return varied_response("wellbeing", session)
    if intent == "gratitude":
        return varied_response("gratitude", session, avoid_transition=True)
    if intent == "affirmation":
        return varied_response("affirmation", session, avoid_transition=True)
    if intent == "farewell":
        return varied_response("farewell", session, avoid_transition=True)
    if intent == "time_date":
        return _date_response(message)
    if intent == "creator_origin":
        return "I’m part of the Open Signals behavioral intelligence platform, built to help interpret aggregate public and authorized signal patterns."
    if intent == "identity":
        return "I’m Open Signals, a privacy-preserving behavioral intelligence assistant for understanding aggregate risks, demand patterns, opportunities, and county trends."
    if intent == "capability":
        if "what are you doing" in _normalize(message):
            return "I’m here analyzing and interpreting emerging behavioral signals and trends, and I’m also ready to chat naturally."
        return "I can chat normally, explain Open Signals, compare counties, summarize risks or opportunities, and interpret aggregate behavioral intelligence."
    if intent == "humor":
        return "Here’s a small one: I asked the data for a joke, but it said the punchline was still pending validation."
    if intent == "confusion":
        return "No problem. Tell me what you want to talk about, and I’ll keep it simple."
    return "I’m here. We can talk casually, or I can help analyze signals when you want."


def _date_response(message: str) -> str:
    now = datetime.now(ZoneInfo("Africa/Nairobi"))
    normalized = _normalize(message)
    if "time" in normalized and not any(term in normalized for term in ["day", "date", "today"]):
        return f"It is {now.strftime('%H:%M')} in Nairobi."
    return f"Today is {now.strftime('%A')}."


def _result(intent: str, analytical: bool, confidence: float, tone: str) -> dict[str, Any]:
    return {"intent": intent, "analytical": analytical, "confidence": confidence, "tone": tone}


def _is_analytical(normalized: str) -> bool:
    analytical_terms = [
        "signal", "signals", "risk", "risks", "opportunity", "opportunities", "county", "counties",
        "demand", "pressure", "affordability", "forecast", "rising", "emerging", "compare",
        "nairobi", "makueni", "nakuru", "kisumu", "turkana", "kwale", "transport", "food prices",
        "fuel", "policy", "policymakers", "market", "business",
    ]
    return any(term in normalized for term in analytical_terms)


def _analytical_intent(normalized: str) -> str:
    if "compare" in normalized:
        return "comparison"
    if "policy" in normalized or "policymaker" in normalized:
        return "policy"
    if "opportunity" in normalized or "business" in normalized or "market" in normalized:
        return "opportunity"
    if "risk" in normalized or "pressure" in normalized or "stress" in normalized:
        return "risk"
    if "forecast" in normalized or "rising" in normalized or "emerging" in normalized:
        return "forecast"
    return "analytical"


def _tone_for_analytical(normalized: str) -> str:
    if "urgent" in normalized or "right now" in normalized:
        return "urgent"
    if "policy" in normalized:
        return "policy"
    if "business" in normalized or "opportunity" in normalized:
        return "business"
    return "analytical"


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").replace("?", "").split())
