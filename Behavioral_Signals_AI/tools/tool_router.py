"""Deterministic tool router for Open Signals chat."""

from __future__ import annotations

import re
from typing import Any

from Behavioral_Signals_AI.chat.semantic_query_analyzer import analyze_open_signals_query, resolve_county_entity
from Behavioral_Signals_AI.geography.location_options import LOCATION_OPTIONS
from Behavioral_Signals_AI.tools.tool_registry import registered_tool_names


def route_tools_for_prompt(
    prompt: str,
    semantic_query: dict[str, Any] | None = None,
    filters: dict[str, str] | None = None,
    session_context: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Map a user prompt to registered internal tools."""
    text = str(prompt or "")
    normalized = _normalize(text)
    semantic = semantic_query or analyze_open_signals_query(text)
    active_filters = filters or {}
    session = session_context or {}
    county = str(semantic.get("county") or resolve_county_entity(text) or active_filters.get("location") or session.get("last_county") or "")
    category = str(semantic.get("category") or active_filters.get("category") or session.get("last_category") or "All")
    time_focus = str(semantic.get("time_focus") or "")
    calls: list[dict[str, Any]] = [{"name": "privacy_check", "arguments": {"text": text}}]

    if _is_comparison(normalized):
        counties = _counties_from_prompt(text)
        if len(counties) >= 2:
            calls.append({"name": "compare_counties", "arguments": {"county_a": counties[0], "county_b": counties[1], "category": category}})
            return _dedupe_registered(calls)

    if "strongest" in normalized or "top signal" in normalized or "strongest signal" in normalized:
        calls.append({"name": "get_top_signal", "arguments": {"location": county or active_filters.get("location", "Kenya"), "category": category}})
    elif county:
        calls.append({"name": "get_county_signals", "arguments": {"county": county, "category": category, "time_focus": time_focus}})
        calls.append({"name": "get_geospatial_context", "arguments": {"county": county, "category": category}})
    else:
        calls.append({"name": "get_live_signals", "arguments": {"location": active_filters.get("location", "Kenya"), "category": category}})

    if category and category != "All":
        calls.append({"name": "get_category_signals", "arguments": {"category": category, "location": county or active_filters.get("location", "Kenya")}})
    if any(term in normalized for term in ["opportunity", "opportunities", "business", "market"]):
        calls.append({"name": "summarize_opportunities", "arguments": {"location": county or active_filters.get("location", "Kenya"), "category": category}})
    if any(term in normalized for term in ["risk", "risks", "stress", "pressure", "shortage", "shortages", "affordability"]):
        calls.append({"name": "summarize_risks", "arguments": {"location": county or active_filters.get("location", "Kenya"), "category": category}})
    if any(term in normalized for term in ["forecast", "rising", "emerging", "future", "next"]):
        calls.append({"name": "get_forecast_context", "arguments": {"county": county, "category": category}})
    if any(term in normalized for term in ["history", "historical", "persist", "persistent", "pattern"]):
        calls.append({"name": "get_historical_pattern", "arguments": {"county": county, "category": category}})
    if any(term in normalized for term in ["outcome", "validated", "confirmed", "accuracy"]):
        calls.append({"name": "get_outcome_learning", "arguments": {"county": county, "category": category}})
    if any(term in normalized for term in ["sure", "fresh", "current", "updated", "confidence"]):
        calls.append({"name": "get_source_freshness", "arguments": {}})
        calls.append({"name": "get_evaluation_metrics", "arguments": {}})
    return _dedupe_registered(calls)


def _counties_from_prompt(prompt: str) -> list[str]:
    normalized = _normalize(prompt)
    counties = []
    for option in LOCATION_OPTIONS:
        if option in {"Global", "Kenya"}:
            continue
        if _normalize(option) in normalized:
            counties.append(option)
    return counties


def _is_comparison(normalized: str) -> bool:
    return bool(re.search(r"\b(compare|versus|vs|different|stronger)\b", normalized))


def _dedupe_registered(calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    names = registered_tool_names()
    seen: set[tuple[str, str]] = set()
    routed = []
    for call in calls:
        name = str(call.get("name") or "")
        args = call.get("arguments") if isinstance(call.get("arguments"), dict) else {}
        key = (name, str(sorted(args.items())))
        if name in names and key not in seen:
            routed.append({"name": name, "arguments": args})
            seen.add(key)
    return routed


def _normalize(text: str) -> str:
    return " ".join(str(text or "").lower().replace("_", " ").replace("-", " ").split())
