"""Semantic query analysis for Open Signals chat.

The analyzer is deliberately lightweight and deterministic. It resolves
county/entity intent and analytical language before the chat stack decides
whether to clarify or answer.
"""

from __future__ import annotations

import difflib
import re
import unicodedata
from typing import Any

from Behavioral_Signals_AI.geography.county_matcher import detect_county_from_text
from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS
from Behavioral_Signals_AI.signal_engine.category_learning import get_category_options

ANALYTICAL_TERMS = {
    "happening", "rising", "emerging", "trending", "trend", "trends", "opportunities",
    "opportunity", "risks", "risk", "pressure", "demand", "shortages", "shortage",
    "affordability", "jobs", "inflation", "housing", "transport", "health", "food",
    "water", "energy", "market", "business", "stress", "signals", "signal",
}

TIME_TERMS = {
    "right now": "current",
    "currently": "current",
    "now": "current",
    "today": "today",
    "recently": "recent",
    "lately": "recent",
    "this week": "recent",
    "emerging": "emerging",
}

BUSINESS_TERMS = {"opportunity", "opportunities", "business", "market", "investment", "investor", "sme"}
POLICY_TERMS = {"policy", "policymaker", "policymakers", "government", "public", "monitor"}
CONVERSATIONAL_TERMS = {"hi", "hello", "hey", "thanks", "thank you", "who are you", "what is your name"}


def analyze_open_signals_query(prompt: str) -> dict[str, Any]:
    """Return a structured semantic read of a user prompt."""
    text = str(prompt or "").strip()
    normalized = _normalize(text)
    county = resolve_county_entity(text)
    category = resolve_category_entity(text)
    analytical = _has_analytical_language(normalized) or bool(county and _looks_like_county_question(normalized))
    time_focus = _time_focus(normalized)
    intent = _semantic_intent(normalized, analytical)
    confidence = _confidence(county, category, analytical, time_focus, normalized)
    return {
        "intent": intent,
        "county": county,
        "category": category,
        "time_focus": time_focus,
        "analytical": analytical,
        "confidence": confidence,
    }


def resolve_county_entity(prompt: str) -> str:
    """Resolve explicit or fuzzy Kenyan county mentions from prompt text."""
    text = str(prompt or "")
    detected = detect_county_from_text(text)
    county = str(detected.get("county_name") or "")
    if county and county != "Kenya-wide":
        return county
    normalized = _normalize(text)
    for option in LOCATION_OPTIONS:
        if option in {"Global", "Kenya"}:
            continue
        option_norm = _normalize(option)
        if re.search(rf"\b{re.escape(option_norm)}(?:\s+county)?\b", normalized):
            return option
    words = re.findall(r"[a-zA-Z']{4,}", normalized)
    counties = [option for option in LOCATION_OPTIONS if option not in {"Global", "Kenya"}]
    normalized_counties = {_normalize(county): county for county in counties}
    for word in words:
        matches = difflib.get_close_matches(word, normalized_counties.keys(), n=1, cutoff=0.86)
        if matches:
            return normalized_counties[matches[0]]
    return ""


def resolve_category_entity(prompt: str) -> str:
    normalized = _normalize(prompt)
    for category in get_category_options():
        if category == "All":
            continue
        if _normalize(category) in normalized:
            return category
    keyword_map = {
        "food and agriculture": ["food", "maize", "unga", "agriculture", "fertilizer"],
        "jobs and labour market": ["jobs", "employment", "labour", "unemployment", "youth"],
        "housing": ["housing", "rent", "construction"],
        "health": ["health", "hospital", "clinic", "medicine"],
        "transport": ["transport", "fuel", "traffic", "logistics", "matatu"],
        "energy": ["energy", "electricity", "tokens", "power"],
        "water and sanitation": ["water", "sanitation", "borehole"],
        "cost of living": ["affordability", "inflation", "prices", "cost of living", "expensive"],
        "trade and business": ["business", "market", "opportunity", "retail", "trade"],
    }
    for category, terms in keyword_map.items():
        if any(term in normalized for term in terms):
            return category
    return ""


def _semantic_intent(normalized: str, analytical: bool) -> str:
    tokens = set(re.findall(r"[a-zA-Z]+", normalized))
    if any(term in normalized for term in CONVERSATIONAL_TERMS) and not analytical:
        return "conversational"
    if tokens.intersection(POLICY_TERMS):
        return "policy"
    if tokens.intersection(BUSINESS_TERMS):
        return "business"
    if analytical:
        return "analytical"
    return "exploratory"


def _has_analytical_language(normalized: str) -> bool:
    tokens = set(re.findall(r"[a-zA-Z]+", normalized))
    return bool(tokens.intersection(ANALYTICAL_TERMS)) or any(
        phrase in normalized for phrase in ["what is happening", "what's happening", "show me", "tell me about"]
    )


def _looks_like_county_question(normalized: str) -> bool:
    return normalized.startswith(("what ", "show ", "explain ", "tell ")) or " in " in f" {normalized} "


def _time_focus(normalized: str) -> str:
    for phrase, label in TIME_TERMS.items():
        if phrase in normalized:
            return label
    return ""


def _confidence(county: str, category: str, analytical: bool, time_focus: str, normalized: str) -> float:
    score = 0.35
    if county:
        score += 0.25
    if category:
        score += 0.15
    if analytical:
        score += 0.2
    if time_focus:
        score += 0.05
    if len(normalized.split()) <= 2 and not county:
        score -= 0.2
    return round(max(0.0, min(1.0, score)), 2)


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    return " ".join(normalized.lower().replace("_", " ").replace("-", " ").replace("'", "").split())
