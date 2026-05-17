"""Interactive aggregate-signal Q&A for Open Signals."""

from __future__ import annotations

import re
from typing import Any

from Behavioral_Signals_AI.ai_platform.context_builder import build_open_signals_context
from Behavioral_Signals_AI.chat.intents import detect_open_signals_intent
from Behavioral_Signals_AI.chat.reference_resolver import resolve_short_followup
from Behavioral_Signals_AI.data_ingestion.retrieval_index import retrieve_relevant_context
from Behavioral_Signals_AI.geography.county_matcher import detect_county_from_text, signal_matches_location
from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS
from Behavioral_Signals_AI.llm.llm_client import complete_json
from Behavioral_Signals_AI.llm.open_signals_system_prompt import OPEN_SIGNALS_SYSTEM_PROMPT
from Behavioral_Signals_AI.llm.safety_guardrails import contains_private_fields, sanitize_llm_signals
from Behavioral_Signals_AI.signal_engine.category_learning import category_matches_signal, get_category_options
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals
from Behavioral_Signals_AI.signal_engine.signal_trajectory import detect_emerging_signals, detect_weakening_signals
from Behavioral_Signals_AI.ui.feed_diff_engine import rank_signals_for_display

PRIVATE_DATA_RESPONSE = (
    "Open Signals only uses aggregate, anonymized, public, or user-authorized intelligence. "
    "It cannot identify individuals or expose private behavior."
)

FORBIDDEN_PROMPT_PATTERNS = [
    re.compile(r"\b(user_id|device_id|phone|email|private_message|personal_profile|exact location|gps|route|home address|work address|raw likes|raw comments|raw shares|raw searches|individual profile)\b", re.IGNORECASE),
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    re.compile(r"\b(?:\+?254|0)?7\d{8}\b"),
]

CHAT_SYSTEM_PROMPT = OPEN_SIGNALS_SYSTEM_PROMPT

SAFE_FIELDS = [
    "signal_topic",
    "signal_category",
    "demand_level",
    "opportunity_level",
    "unmet_demand_likelihood",
    "urgency",
    "geographic_scope",
    "county_name",
    "source_summary",
    "confidence_score",
    "momentum",
    "forecast_direction",
    "spread_risk",
    "interpretation",
    "recommended_action",
    "historical_pattern_match",
    "outcome_learning_note",
    "validation_status",
    "geospatial_insight",
    "confidence_reasoning",
]


def answer_open_signals_prompt(message: str, history: list[Any] | None, location: str, category: str, urgency: str) -> str:
    """Answer a user question using only current interpreted aggregate signals."""
    cleaned = str(message or "").strip()
    if not cleaned:
        return "Ask a question about live aggregate signals, counties, demand, risks, or opportunities."
    if _has_private_request(cleaned):
        return PRIVATE_DATA_RESPONSE

    detected_intent = detect_open_signals_intent(cleaned)
    session_context = _conversation_context(history)
    resolved_followup = resolve_short_followup(cleaned, history, session_context)
    if resolved_followup.get("resolved"):
        detected_intent = {"intent": str(resolved_followup["intent"]), "confidence": float(resolved_followup.get("confidence", 0.8))}
    elif detected_intent["intent"] == "short_followup":
        return _short_followup_clarification(cleaned)
    if detected_intent["intent"] != "unclear_query":
        conversational = _conversational_response(detected_intent["intent"], cleaned)
        if conversational:
            return conversational

    question_location = _location_from_question(cleaned)
    question_category = _category_from_question(cleaned)
    if _needs_clarification(cleaned, detected_intent["intent"], session_context, question_location, question_category):
        return _clarification_prompt()
    effective_location = question_location or _context_location_for_followup(cleaned, session_context) or location or "Kenya"
    effective_category = question_category or _context_category_for_followup(cleaned, session_context) or category or "All"
    effective_urgency = urgency or "All"

    if detected_intent["intent"] == "unclear_query" and not _has_session_context(session_context):
        return _clarification_prompt()
    if detected_intent["intent"] == "comparison_query" or _is_comparison_question(cleaned):
        return _comparison_answer(cleaned, effective_category, effective_urgency, session_context)
    if _is_time_question(cleaned):
        return _time_aware_answer(cleaned, effective_location, effective_category, effective_urgency)

    signals = _filtered_ranked_signals(effective_location, effective_category, effective_urgency)
    if not signals:
        return _no_signal_answer(effective_location, effective_category, effective_urgency)

    answer_profile = _answer_profile(cleaned, detected_intent["intent"])
    reasoning_question = _resolved_reasoning_question(cleaned, detected_intent["intent"])
    fallback_answer = _grounded_rule_based_answer(
        reasoning_question,
        signals,
        effective_location,
        effective_category,
        effective_urgency,
        session_context,
        question_location,
        question_category,
        answer_profile,
    )
    payload = build_open_signals_llm_payload(
        reasoning_question,
        signals,
        {"location": effective_location, "category": effective_category, "urgency": effective_urgency},
        session_context,
        history,
        detected_intent["intent"],
        answer_profile,
    )
    result = complete_json(CHAT_SYSTEM_PROMPT, payload, fallback={"answer": fallback_answer})
    answer = str(result.get("answer") or fallback_answer).strip()
    return _ensure_grounded_answer(_strip_private_terms(answer), signals[0], effective_location, answer_profile) or fallback_answer



def build_open_signals_llm_payload(
    question: str,
    signals: list[dict[str, Any]],
    filters: dict[str, str],
    session_context: dict[str, str] | None,
    history: list[Any] | None,
    intent: str,
    answer_profile: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build a privacy-safe, aggregate-only context package for optional LLM reasoning."""
    ranked = rank_signals_for_display([signal for signal in signals if isinstance(signal, dict)])[:6]
    safe_signals = sanitize_llm_signals([_safe_signal(signal) for signal in ranked], limit=6)
    payload = {
        "question": str(question or "")[:500],
        "intent": intent,
        "filters": dict(filters or {}),
        "session_context": dict(session_context or {}),
        "history_turns": _safe_history(history),
        "aggregate_live_signals": safe_signals,
        "ml_adaptive_context": _ml_adaptive_context(ranked),
        "retrieval_context": _retrieval_context(ranked),
        "platform_grounding_context": build_open_signals_context(
            question,
            {"intent": intent, "confidence": 1.0},
            filters.get("location", "Kenya"),
            filters.get("category", "All"),
            filters.get("urgency", "All"),
            session_context,
            history,
        ),
        "answer_profile": dict(answer_profile or _answer_profile(question, intent)),
        "required_answer_style": _required_answer_style(answer_profile or _answer_profile(question, intent)),
        "privacy_boundary": "aggregate_anonymized_public_or_user_authorized_only",
    }
    if contains_private_fields(payload):
        raise ValueError("LLM payload contains private fields")
    return payload


def _ml_adaptive_context(signals: list[dict[str, Any]]) -> dict[str, Any]:
    if not signals:
        return {"ranking_basis": "no current signals"}
    top = signals[0]
    return {
        "ranking_basis": "adaptive ranking from priority, confidence, momentum, spread risk, persistence, source validation, and outcome learning when available",
        "top_signal": _topic(top),
        "top_signal_score": _signal_score(top),
        "top_trajectory": _trajectory_label(top),
        "top_confidence": top.get("confidence_score"),
        "top_spread_risk": top.get("spread_risk"),
    }


def _retrieval_context(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    context = []
    for signal in signals[:6]:
        context.append({
            "signal_topic": signal.get("signal_topic"),
            "county_or_scope": signal.get("county_name") or signal.get("geographic_scope"),
            "historical_learning_note": signal.get("historical_pattern_match"),
            "outcome_learning_note": signal.get("outcome_learning_note"),
            "geospatial_insight": signal.get("geospatial_insight"),
            "source_validation": signal.get("validation_status") or signal.get("source_summary"),
            "confidence_reasoning": signal.get("confidence_reasoning"),
        })
    return context


def respond_open_signals_chat(message: str, history: list[Any] | None, location: str, category: str, urgency: str) -> tuple[list[Any], str]:
    """Gradio adapter that appends an Open Signals answer to chat history."""
    answer = answer_open_signals_prompt(message, history or [], location, category, urgency)
    updated_history = list(history or [])
    if updated_history and isinstance(updated_history[0], tuple):
        updated_history.append((str(message or "").strip(), answer))
    else:
        updated_history.append({"role": "user", "content": str(message or "").strip()})
        updated_history.append({"role": "assistant", "content": answer})
    return _trim_chat_history(updated_history), ""






def _conversational_response(intent: str, message: str) -> str:
    """Return a natural non-analytical response for conversational prompts."""
    if intent == "greeting":
        return (
            "Hello. I'm Open Signals - I monitor emerging aggregate behavioral signals, market pressure, risks, "
            "and opportunities across Kenya. What would you like to explore?"
        )
    if intent == "identity_query":
        return (
            "I'm Open Signals - a privacy-preserving behavioral intelligence assistant focused on emerging "
            "aggregate signals, risks, opportunities, and demand patterns across Kenya."
        )
    if intent == "capability_query":
        lowered = _normalize(message)
        if "signal" in lowered:
            return (
                "Signals are interpreted aggregate patterns that may point to demand, affordability pressure, "
                "economic stress, market opportunity, or policy concern. I can help explain those patterns by "
                "county, category, urgency, and confidence using privacy-preserving aggregate intelligence."
            )
        return (
            "I can help analyze emerging county-level signals, affordability pressure, market opportunities, "
            "economic stress indicators, and evolving behavioral trends using aggregate intelligence."
        )
    if intent == "farewell":
        return "Goodbye. I will be here when you want to explore Kenya signals, risks, opportunities, or county trends."
    if intent == "gratitude":
        return "You're welcome. Ask me about a county, sector, risk, opportunity, or emerging demand signal whenever you're ready."
    if intent == "help":
        return (
            "I help interpret aggregate signals related to demand, affordability pressure, economic stress, "
            "opportunities, policy concerns, and county-level trends. You can ask things like 'show signals in Nairobi', "
            "'compare Nakuru and Makueni', or 'what should policymakers monitor?'"
        )
    if intent == "small_talk":
        return "I'm ready to help. I can interpret emerging aggregate signals, county trends, market opportunities, and policy risks."
    return ""



def _needs_clarification(
    question: str,
    intent: str,
    session_context: dict[str, str],
    question_location: str,
    question_category: str,
) -> bool:
    """Ask a clarifying question for vague prompts unless context makes the reference clear."""
    if question_location or question_category:
        return False
    has_context = _has_session_context(session_context)
    if _is_vague_prompt(question):
        return not has_context
    if intent == "follow_up_query":
        return not has_context
    if intent == "unclear_query":
        return True
    return False


def _has_session_context(session_context: dict[str, str]) -> bool:
    return bool(
        session_context.get("last_county")
        or session_context.get("last_category")
        or session_context.get("last_signal")
        or session_context.get("last_signal_topic")
    )


def _is_vague_prompt(question: str) -> bool:
    q = _normalize(question).strip(" ?.!\t\n\r")
    vague_exact = {
        "tell me more",
        "what about this",
        "explain",
        "show me",
        "what is happening",
        "what's happening",
        "what happens",
        "more",
        "continue",
        "go on",
        "this",
        "that",
    }
    if q in vague_exact:
        return True
    return bool(re.search(r"\b(tell me more|what about this|explain this|show me more|what is happening\??)\b", q))


def _clarification_prompt() -> str:
    return "Do you want me to explain the strongest current signal, a specific county, or a market opportunity?"


def _short_followup_clarification(message: str) -> str:
    lowered = _normalize(message)
    if lowered in {"who", "why", "meaning", "mean", "means", "how", "where"}:
        return "Do you mean who I am, why a signal matters, or the meaning of a specific signal?"
    return _clarification_prompt()

def _conversation_context(history: list[Any] | None) -> dict[str, str]:
    """Extract temporary session context from visible chat history only."""
    context = {
        "last_county": "",
        "last_category": "",
        "last_signal": "",
        "last_signal_topic": "",
        "last_intent": "",
        "last_answer_type": "",
    }
    for content in _history_text_items(history):
        safe = _strip_private_terms(content)
        county = _location_from_question(safe)
        if county and county not in {"Global", "Kenya"}:
            context["last_county"] = county
        category = _category_from_question(safe)
        if category:
            context["last_category"] = category
        match = re.search(r"Strongest relevant signal:\*\*\s*([^\n(]+)", safe, re.IGNORECASE)
        if match:
            context["last_signal"] = match.group(1).strip(" :.-")[:120]
            context["last_signal_topic"] = context["last_signal"]
            context["last_answer_type"] = "signal_answer"
        if "Hello. I'm Open Signals" in safe or "privacy-preserving behavioral intelligence" in safe:
            context["last_intent"] = "greeting" if "Hello. I'm Open Signals" in safe else "identity_query"
            context["last_answer_type"] = "conversational"
    return context


def _history_text_items(history: list[Any] | None) -> list[str]:
    items: list[str] = []
    for item in list(history or [])[-8:]:
        if isinstance(item, dict):
            items.append(str(item.get("content") or ""))
        elif isinstance(item, (tuple, list)):
            items.extend(str(part or "") for part in item[:2])
        else:
            items.append(str(item or ""))
    return items


def _context_location_for_followup(question: str, context: dict[str, str]) -> str:
    if _is_followup_question(question):
        return context.get("last_county", "")
    return ""


def _context_category_for_followup(question: str, context: dict[str, str]) -> str:
    if _is_followup_question(question):
        return context.get("last_category", "")
    return ""


def _is_followup_question(question: str) -> bool:
    q = _normalize(question)
    return bool(re.search(r"\b(that|this|it|there|same|also|why|what about|how about|opportunity|policy|policymakers|rising)\b", q))


def _filtered_ranked_signals(location: str, category: str, urgency: str) -> list[dict[str, Any]]:
    payload = get_cached_or_fallback_signals()
    cache_status = str(payload.get("status") or "unknown")
    signals = [signal for signal in payload.get("signals", []) if isinstance(signal, dict)]
    filtered: list[dict[str, Any]] = []
    for signal in signals:
        if not category_matches_signal(signal, category):
            continue
        if urgency != "All" and str(signal.get("urgency", "")).lower() != urgency.lower():
            continue
        if location not in {"", "All", "Kenya", "Global"} and not signal_matches_location(signal, location):
            continue
        filtered.append(dict(signal, _cache_status=cache_status))
    if filtered:
        return rank_signals_for_display(filtered)
    return rank_signals_for_display([dict(signal, _cache_status=cache_status) for signal in signals])



def _is_comparison_question(question: str) -> bool:
    q = _normalize(question)
    return any(term in q for term in ["compare", "different from", "difference", "stronger", "which county", "versus", " vs "])


def _is_time_question(question: str) -> bool:
    q = _normalize(question)
    return any(term in q for term in [
        "changed recently", "what changed", "rising fastest", "persisted", "persistent", "longest",
        "recent", "fastest", "trajectory", "accelerating", "weakened", "weakening", "spreading fastest",
        "spread fastest", "newly emerged", "new emerged", "emerged", "fading",
    ])


def _comparison_answer(question: str, category: str, urgency: str, session_context: dict[str, str]) -> str:
    counties = _locations_from_question(question)
    if len(counties) == 1 and session_context.get("last_county") and session_context["last_county"] != counties[0]:
        counties.insert(0, session_context["last_county"])
    base_signals = _filtered_ranked_signals("Kenya", category or "All", urgency or "All")
    if len(counties) < 2:
        ranked = _top_county_signals(base_signals)
    else:
        ranked = []
        for county in counties[:3]:
            county_signals = [signal for signal in base_signals if signal_matches_location(signal, county)]
            if county_signals:
                ranked.append((county, rank_signals_for_display(county_signals)[0]))
    if not ranked:
        return _no_signal_answer("Kenya", category or "All", urgency or "All")
    strongest_county, strongest = max(ranked, key=lambda item: _signal_score(item[1]))
    summary = f"**Short answer:** {strongest_county} currently shows the stronger signal in this comparison: {_topic(strongest)}."
    lines = [summary, "", "**County comparison:**"]
    for county, signal in ranked[:4]:
        lines.append(
            f"- **{county}:** {_topic(signal)}; confidence {_confidence(signal)}%; spread risk {signal.get('spread_risk', 'Moderate')}; trajectory {_trajectory_label(signal)}. {_risk_or_opportunity(signal)}"
        )
    lines.extend([
        "",
        f"**Interpretation:** The comparison is based on aggregate signal strength, urgency, confidence, momentum, spread risk, and persistence indicators. {strongest_county} should be watched first if this pattern continues.",
    ])
    return "\n".join(lines)


def _time_aware_answer(question: str, location: str, category: str, urgency: str) -> str:
    signals = _filtered_ranked_signals(location or "Kenya", category or "All", urgency or "All")
    if not signals:
        return _no_signal_answer(location or "Kenya", category or "All", urgency or "All")
    q = _normalize(question)
    if "weaken" in q or "fading" in q:
        selected = detect_weakening_signals(signals) or sorted(signals, key=lambda signal: _trajectory_score(signal))[:3]
        mode = "weakening"
    elif "newly" in q or "emerged" in q or "emerging" in q:
        selected = [signal for signal in detect_emerging_signals(signals) if signal.get("is_new_signal")] or detect_emerging_signals(signals) or signals[:3]
        mode = "newly emerged"
    elif "spread" in q:
        selected = sorted(signals, key=lambda signal: _safe_number(signal.get("geographic_spread_score") or signal.get("spread_score") or signal.get("confidence_score")), reverse=True)[:3]
        mode = "spreading fastest"
    elif "accelerat" in q or "fastest" in q or "rising" in q or "changed" in q:
        selected = sorted(signals, key=lambda signal: (_trajectory_score(signal), _signal_score(signal)), reverse=True)[:3]
        mode = "accelerating"
    elif "persist" in q or "longest" in q:
        selected = sorted(signals, key=lambda signal: _safe_number(signal.get("persistence_score") or signal.get("appearance_count") or signal.get("confidence_score")), reverse=True)[:3]
        mode = "persistent"
    else:
        selected = signals[:3]
        mode = "most active"
    top = selected[0]
    lines = [
        f"**Short answer:** The {mode} signal is {_topic(top)} in {_scope(top)}; it appears {top.get('trajectory_label') or _trajectory_label(top)} with {_confidence(top)}% confidence.",
        "",
        "**What changed:**",
    ]
    for signal in selected:
        lines.append(
            f"- **{_topic(signal)}:** {signal.get('trajectory_label') or _trajectory_label(signal)}; momentum {signal.get('momentum', 'Stable')}; forecast {signal.get('forecast_direction', 'Stable')}; validation {signal.get('validation_status', 'unvalidated')}.")
    lines.extend([
        "",
        "**Why it matters:** Time-aware ranking uses persistence, ranking movement, outcome learning notes, historical pattern matches, and current adaptive scores when available.",
    ])
    return "\n".join(lines)


def _top_county_signals(signals: list[dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
    by_county: dict[str, list[dict[str, Any]]] = {}
    for signal in signals:
        county = str(signal.get("county_name") or signal.get("geographic_scope") or "Kenya-wide")
        if county in {"", "Kenya-wide", "Global"}:
            continue
        by_county.setdefault(county, []).append(signal)
    ranked: list[tuple[str, dict[str, Any]]] = []
    for county, county_signals in by_county.items():
        ranked.append((county, rank_signals_for_display(county_signals)[0]))
    return sorted(ranked, key=lambda item: _signal_score(item[1]), reverse=True)[:4]


def _locations_from_question(question: str) -> list[str]:
    normalized_question = _normalize(question)
    counties = []
    for option in LOCATION_OPTIONS:
        if option in {"Global", "Kenya"}:
            continue
        if _normalize(option) in normalized_question:
            counties.append(option)
    detected = _location_from_question(question)
    if detected and detected not in {"Global", "Kenya"} and detected not in counties:
        counties.append(detected)
    return counties



def _resolved_reasoning_question(question: str, intent: str) -> str:
    if intent == "explain_reason":
        return "explain_reason why is this signal important"
    if intent == "explain_meaning":
        return "explain_meaning economic meaning"
    if intent == "explain_mechanism":
        return "explain_mechanism how does this signal work"
    if intent == "explain_geography":
        return "explain_geography where is this signal relevant"
    return question

def _answer_profile(question: str, intent: str = "") -> dict[str, str]:
    q = _normalize(question)
    if re.search(r"\b(briefly|brief|short|summary|summarize|quickly|concise)\b", q):
        depth = "short"
    elif re.search(r"\b(explain|why|in detail|details|detailed|deep dive)\b", q) or intent in {"explain_reason", "explain_meaning", "explain_mechanism", "explain_geography"}:
        depth = "structured"
    else:
        depth = "default"

    if re.search(r"\b(policy|policymaker|policymakers|government|public sector|monitor)\b", q):
        focus = "policy"
    elif re.search(r"\b(business|opportunity|market|investment|investor|enterprise|sme|retail)\b", q):
        focus = "opportunity"
    else:
        focus = "general"
    return {"depth": depth, "focus": focus}


def _required_answer_style(answer_profile: dict[str, str]) -> list[str]:
    depth = answer_profile.get("depth", "default")
    focus = answer_profile.get("focus", "general")
    if focus == "policy":
        return ["brief direct answer", "policy relevance", "risk to monitor", "recommended public action"]
    if focus == "opportunity":
        return ["brief direct answer", "market opportunity", "affected sector", "recommended business action"]
    if depth == "short":
        return ["short conversational answer", "strongest signal", "meaning", "recommended action"]
    if depth == "structured":
        return ["short summary", "why it matters", "evidence basis", "opportunity or risk", "recommended action"]
    return ["brief direct answer", "key signal", "what it means", "opportunity or risk", "recommended action"]


def _grounded_rule_based_answer(question: str, signals: list[dict[str, Any]], location: str, category: str, urgency: str, session_context: dict[str, str] | None = None, question_location: str = "", question_category: str = "", answer_profile: dict[str, str] | None = None) -> str:
    top = _select_relevant_signal(question, signals)
    q = question.lower()
    profile = answer_profile or _answer_profile(question)
    if profile.get("focus") == "policy":
        emphasis = _policy_sentence(top)
    elif profile.get("focus") == "opportunity":
        emphasis = _opportunity_sentence(top)
    elif "why" in q or "important" in q or "confidence" in q or "affected" in q or "explain_reason" in q:
        emphasis = _explainability_sentence(top)
    elif "opportun" in q or "market" in q or "business" in q or "sector" in q:
        emphasis = _opportunity_sentence(top)
    elif "policy" in q or "policymaker" in q or "monitor" in q:
        emphasis = _policy_sentence(top)
    elif "risk" in q or "stress" in q:
        emphasis = _risk_sentence(top)
    elif "meaning" in q or "explain_meaning" in q:
        emphasis = _economic_meaning_sentence(top)
    elif "explain_mechanism" in q or q.strip() == "how":
        emphasis = _mechanism_sentence(top)
    elif "explain_geography" in q or q.strip() == "where":
        emphasis = _geography_sentence(top)
    else:
        emphasis = _meaning_sentence(top)
    evidence_note = _retrieved_evidence_note(question, location, category)
    if evidence_note:
        emphasis = f"{emphasis} {evidence_note}"
    if question_location and session_context and session_context.get("last_county") and session_context.get("last_county") != question_location:
        emphasis = f"Compared with the previous county context ({session_context['last_county']}), {question_location} is now the active county context. {emphasis}"
    elif _is_followup_question(question) and session_context and session_context.get("last_signal"):
        emphasis = f"This follows the earlier signal context ({session_context['last_signal']}). {emphasis}"
    return _format_grounded_answer(top, emphasis, location, category, urgency, profile)



def _retrieved_evidence_note(question: str, location: str, category: str) -> str:
    evidence = retrieve_relevant_context(question, location, category, limit=2)
    if not evidence:
        return ""
    top = evidence[0]
    source = top.get("source_name") or top.get("source_type") or "retrieved aggregate evidence"
    summary = str(top.get("summary") or top.get("topic") or "")[:180]
    return f"Retrieved aggregate evidence from {source} adds context: {summary}."

def _select_relevant_signal(question: str, signals: list[dict[str, Any]]) -> dict[str, Any]:
    words = {word for word in re.findall(r"[a-zA-Z]{4,}", question.lower()) if word not in {"what", "show", "signals", "signal", "about", "which", "should"}}
    if not words:
        return signals[0]
    best = signals[0]
    best_score = -1
    for signal in signals:
        blob = _signal_blob(signal)
        score = sum(1 for word in words if word in blob)
        if score > best_score:
            best = signal
            best_score = score
    return best


def _format_grounded_answer(signal: dict[str, Any], emphasis: str, location: str, category: str, urgency: str, answer_profile: dict[str, str] | None = None) -> str:
    topic = str(signal.get("signal_topic") or "current aggregate signal")
    signal_category = str(signal.get("signal_category") or category or "other")
    confidence = str(signal.get("confidence_score", "unknown"))
    scope = str(signal.get("county_name") or signal.get("geographic_scope") or location or "Kenya-wide")
    opportunity = str(signal.get("opportunity_level", "Moderate"))
    urgency_value = str(signal.get("urgency", urgency or "Medium"))
    risk = _risk_label(signal)
    action = str(signal.get("recommended_action") or signal.get("monitoring_recommendation") or "Monitor persistence, source confirmation, county spread, and outcome validation.")
    evidence = _evidence_basis_sentence(signal)
    profile = answer_profile or {"depth": "default", "focus": "general"}
    focus = profile.get("focus", "general")
    if focus == "policy":
        return (
            f"**Policy signal:** {topic} ({signal_category}).\n\n"
            f"**Policy meaning:** {emphasis}\n\n"
            f"**Evidence basis:** {evidence}\n\n"
            f"**Confidence and scope:** {confidence}% confidence; scope is {scope}.\n\n"
            f"**What to monitor:** urgency is {urgency_value}, spread risk is {risk}, and related signals should be checked for persistence and outcome validation.\n\n"
            f"**Recommended public action:** {action}"
        )
    if focus == "opportunity":
        return (
            f"**Market opportunity signal:** {topic} ({signal_category}).\n\n"
            f"**Opportunity meaning:** {emphasis}\n\n"
            f"**Evidence basis:** {evidence}\n\n"
            f"**Confidence and scope:** {confidence}% confidence; scope is {scope}.\n\n"
            f"**Market read:** opportunity is {opportunity}, urgency is {urgency_value}, and risk signal is {risk}.\n\n"
            f"**Recommended business action:** {action}"
        )
    if profile.get("depth") == "short":
        return (
            f"**Summary:** {topic} is the strongest relevant signal for {scope}. "
            f"{emphasis} Evidence basis: {evidence} Confidence is {confidence}%. Recommended action: {action}"
        )
    return (
        f"**Strongest relevant signal:** {topic} ({signal_category}).\n\n"
        f"**What it means:** {emphasis}\n\n"
        f"**Evidence basis:** {evidence}\n\n"
        f"**Confidence level:** {confidence}% based on aggregate interpreted signal evidence, source validation, historical learning, and current ranking.\n\n"
        f"**County/scope:** {scope}.\n\n"
        f"**Opportunity or risk:** Opportunity is {opportunity}; urgency is {urgency_value}; risk signal is {risk}.\n\n"
        f"**Recommended action:** {action}"
    )


def _meaning_sentence(signal: dict[str, Any]) -> str:
    interpretation = signal.get("interpretation") or signal.get("plain_language_meaning")
    if interpretation:
        return str(interpretation)
    return (
        f"This appears to be a {signal.get('demand_level', 'Moderate').lower()} demand signal with "
        f"{signal.get('momentum', 'Stable').lower()} momentum and {signal.get('forecast_direction', 'Stable').lower()} forecast direction."
    )



def _economic_meaning_sentence(signal: dict[str, Any]) -> str:
    return (
        f"Economically, {signal.get('signal_topic', 'this signal')} suggests a possible shift in aggregate demand, "
        f"affordability pressure, service stress, or market opportunity in {signal.get('county_name') or signal.get('geographic_scope') or 'Kenya'}. "
        f"For policy, it is a cue to monitor whether the pattern persists, spreads, or becomes validated by public aggregate evidence."
    )


def _mechanism_sentence(signal: dict[str, Any]) -> str:
    return (
        f"This signal becomes important when aggregate evidence reinforces itself through persistence, source agreement, "
        f"momentum, county spread, historical recurrence, and outcome validation. Current trajectory is "
        f"{signal.get('trajectory_label') or _trajectory_label(signal)} with {signal.get('confidence_score', 'unknown')}% confidence."
    )


def _geography_sentence(signal: dict[str, Any]) -> str:
    return (
        f"The current geographic scope is {signal.get('county_name') or signal.get('geographic_scope') or 'Kenya-wide'}. "
        f"Spread risk is {signal.get('spread_risk', 'Low')}, and county relevance should be interpreted only from aggregate, "
        f"public, or user-authorized evidence."
    )


def _evidence_basis_sentence(signal: dict[str, Any]) -> str:
    source_summary = str(signal.get("source_summary") or "aggregate interpreted sources")
    evidence_types = _evidence_types(signal)
    validation = _validation_label(signal)
    limited_note = " Evidence is limited because the current cache is using fallback aggregate intelligence." if _is_limited_evidence(signal) else ""
    return (
        f"{source_summary}; based on {', '.join(evidence_types)}. "
        f"Validation: {validation}.{limited_note}"
    )


def _evidence_types(signal: dict[str, Any]) -> list[str]:
    types: list[str] = []
    cache_status = str(signal.get("_cache_status") or "").lower()
    source_summary = str(signal.get("source_summary") or "").lower()
    if cache_status in {"live_or_near_live", "using_cached_last_success"}:
        types.append("current live signal cache")
    elif cache_status in {"sample_aggregate_signal", "initialized_from_sample"} or "sample aggregate" in source_summary:
        types.append("fallback aggregate intelligence")
    else:
        types.append("current signal cache")
    if signal.get("historical_pattern_match"):
        types.append("historical recurrence")
    if signal.get("geospatial_insight") or signal.get("county_name"):
        types.append("county relevance")
    if signal.get("outcome_learning_note") or signal.get("accuracy_confidence"):
        types.append("outcome learning")
    if signal.get("validation_status"):
        types.append("source validation")
    return list(dict.fromkeys(types))


def _validation_label(signal: dict[str, Any]) -> str:
    value = str(signal.get("validation_status") or "").strip().lower().replace("_", " ")
    if value in {"validated", "partially validated", "partially", "unvalidated"}:
        return "partially validated" if value == "partially" else value
    if signal.get("outcome_learning_note") or signal.get("historical_pattern_match"):
        return "partially validated"
    return "unvalidated"


def _is_limited_evidence(signal: dict[str, Any]) -> bool:
    cache_status = str(signal.get("_cache_status") or "").lower()
    source_summary = str(signal.get("source_summary") or "").lower()
    return cache_status in {"sample_aggregate_signal", "initialized_from_sample", "missing", "unknown"} or "sample aggregate" in source_summary


def _opportunity_sentence(signal: dict[str, Any]) -> str:
    return (
        f"This signal may indicate a market or service opportunity where {signal.get('signal_category', 'the category')} demand is visible but still needs validation. "
        f"Opportunity level is {signal.get('opportunity_level', 'Moderate')} and unmet demand likelihood is {signal.get('unmet_demand_likelihood', 'Medium')}."
    )


def _policy_sentence(signal: dict[str, Any]) -> str:
    return (
        f"This is policy-relevant because it combines {signal.get('urgency', 'Medium')} urgency, "
        f"{signal.get('spread_risk', 'Low')} spread risk, and an outcome-learning note: "
        f"{signal.get('outcome_learning_note') or signal.get('historical_pattern_match') or 'evidence is still accumulating.'}"
    )


def _risk_sentence(signal: dict[str, Any]) -> str:
    return (
        f"The main risk is that {signal.get('signal_topic', 'this signal')} may reflect unresolved demand pressure, affordability pressure, or service stress. "
        f"Current urgency is {signal.get('urgency', 'Medium')} and spread risk is {signal.get('spread_risk', 'Low')}."
    )



def _explainability_sentence(signal: dict[str, Any]) -> str:
    reasons = [
        f"trajectory is {_trajectory_label(signal)}",
        f"spread risk is {signal.get('spread_risk', 'Moderate')}",
        f"momentum is {signal.get('momentum', 'Stable')}",
    ]
    if signal.get("confidence_reasoning"):
        reasons.append(str(signal.get("confidence_reasoning")))
    if signal.get("historical_pattern_match"):
        reasons.append(f"historical memory notes {signal.get('historical_pattern_match')}")
    if signal.get("outcome_learning_note"):
        reasons.append(f"outcome learning says {signal.get('outcome_learning_note')}")
    if signal.get("source_summary"):
        reasons.append(f"source agreement context: {signal.get('source_summary')}")
    return "This signal matters because " + "; ".join(reasons[:5]) + "."


def _topic(signal: dict[str, Any]) -> str:
    return str(signal.get("signal_topic") or "current aggregate signal")


def _scope(signal: dict[str, Any]) -> str:
    return str(signal.get("county_name") or signal.get("geographic_scope") or "Kenya-wide")


def _confidence(signal: dict[str, Any]) -> str:
    value = signal.get("confidence_score", "unknown")
    if isinstance(value, (int, float)):
        return str(round(float(value), 1)).rstrip("0").rstrip(".")
    return str(value)


def _risk_or_opportunity(signal: dict[str, Any]) -> str:
    return f"opportunity {signal.get('opportunity_level', 'Moderate')}, unmet demand {signal.get('unmet_demand_likelihood', 'Medium')}, urgency {signal.get('urgency', 'Medium')}"


def _trajectory_label(signal: dict[str, Any]) -> str:
    momentum = _normalize(signal.get("momentum", ""))
    forecast = _normalize(signal.get("forecast_direction", ""))
    urgency = _normalize(signal.get("urgency", ""))
    confidence = _safe_number(signal.get("confidence_score"))
    adaptive = _safe_number(signal.get("behavioral_intelligence_score") or signal.get("priority_score"))
    if "breakout" in momentum or "accelerat" in momentum:
        return "accelerating"
    if "rising" in momentum or "rising" in forecast:
        return "strengthening" if confidence >= 70 or adaptive >= 70 else "emerging"
    if "fall" in momentum or "declin" in forecast:
        return "weakening"
    if "high" in urgency and confidence >= 70:
        return "persistent"
    return "stabilizing"


def _trajectory_score(signal: dict[str, Any]) -> float:
    label = _trajectory_label(signal)
    weights = {"accelerating": 5, "strengthening": 4, "emerging": 3, "persistent": 3, "stabilizing": 2, "weakening": 1}
    return weights.get(label, 2) + _safe_number(signal.get("confidence_score")) / 100


def _signal_score(signal: dict[str, Any]) -> float:
    return max(
        _safe_number(signal.get("priority_score")),
        _safe_number(signal.get("behavioral_intelligence_score")),
        _safe_number(signal.get("confidence_score")),
    )


def _safe_number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0

def _risk_label(signal: dict[str, Any]) -> str:
    risk_parts = [
        f"{signal.get('unmet_demand_likelihood', 'Medium')} unmet demand",
        f"{signal.get('spread_risk', 'Low')} spread risk",
        f"{signal.get('forecast_direction', 'Stable')} forecast",
    ]
    return ", ".join(risk_parts)


def _location_from_question(question: str) -> str:
    detected = detect_county_from_text(question)
    county = detected.get("county_name", "")
    if county and county != "Kenya-wide":
        return county
    normalized_question = _normalize(question)
    for option in LOCATION_OPTIONS:
        if option in {"Global", "Kenya"}:
            continue
        if _normalize(option) in normalized_question:
            return option
    if "global" in normalized_question:
        return "Global"
    if "kenya" in normalized_question or "national" in normalized_question:
        return "Kenya"
    return ""


def _category_from_question(question: str) -> str:
    normalized = _normalize(question)
    for option in get_category_options():
        if option == "All":
            continue
        if _normalize(option) in normalized:
            return option
    keyword_map = {
        "water and sanitation": ["water", "sanitation", "borehole"],
        "food and agriculture": ["food", "maize", "unga", "farm", "agriculture"],
        "jobs and labour market": ["jobs", "employment", "labour", "youth"],
        "trade and business": ["business", "market", "retail", "opportunity"],
        "health": ["health", "hospital", "clinic", "medicine"],
        "transport": ["transport", "traffic", "matatu", "fare"],
        "cost of living": ["cost", "prices", "affordability", "expensive"],
        "finance": ["finance", "credit", "loan", "sacco", "m-pesa", "mpesa"],
    }
    for category, terms in keyword_map.items():
        if any(term in normalized for term in terms):
            return category
    return ""


def _ensure_grounded_answer(answer: str, signal: dict[str, Any], location: str, answer_profile: dict[str, str] | None = None) -> str:
    profile = answer_profile or {"depth": "default", "focus": "general"}
    if profile.get("depth") == "short" and "summary" in answer.lower() and "evidence basis" in answer.lower():
        return answer
    if profile.get("focus") == "policy" and "policy" in answer.lower() and "recommended" in answer.lower() and "evidence basis" in answer.lower():
        return answer
    if profile.get("focus") == "opportunity" and ("opportunity" in answer.lower() or "market" in answer.lower()) and "recommended" in answer.lower() and "evidence basis" in answer.lower():
        return answer
    required_markers = ["Strongest relevant signal", "What it means", "Evidence basis", "Confidence level", "County/scope", "Opportunity or risk", "Recommended action"]
    if all(marker.lower() in answer.lower() for marker in required_markers):
        return answer
    return _format_grounded_answer(signal, answer or _meaning_sentence(signal), location, str(signal.get("signal_category", "All")), str(signal.get("urgency", "All")), profile)


def _no_signal_answer(location: str, category: str, urgency: str) -> str:
    return (
        f"No matching aggregate signals are currently available for {location}, {category}, {urgency}.\n\n"
        "Evidence basis: limited current aggregate evidence for that filter combination; validation is unvalidated.\n\n"
        "Try asking about Kenya-wide signals, opportunities, policy monitoring, or county relevance."
    )


def _safe_signal(signal: dict[str, Any]) -> dict[str, Any]:
    return {field: signal.get(field) for field in SAFE_FIELDS if field in signal}


def _safe_history(history: list[Any] | None) -> list[str]:
    safe: list[str] = []
    for item in list(history or [])[-3:]:
        safe.append(_strip_private_terms(str(item))[:240])
    return safe


def _signal_blob(signal: dict[str, Any]) -> str:
    return " ".join(str(value).lower() for value in _safe_signal(signal).values() if value)


def _has_private_request(text: str) -> bool:
    return any(pattern.search(text or "") for pattern in FORBIDDEN_PROMPT_PATTERNS)


def _strip_private_terms(text: str) -> str:
    cleaned = str(text or "")
    for pattern in FORBIDDEN_PROMPT_PATTERNS:
        cleaned = pattern.sub("[private field removed]", cleaned)
    return cleaned


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())


def _trim_chat_history(history: list[Any], max_messages: int = 8) -> list[Any]:
    """Keep the public chat compact while preserving recent context."""
    return list(history or [])[-max_messages:]

