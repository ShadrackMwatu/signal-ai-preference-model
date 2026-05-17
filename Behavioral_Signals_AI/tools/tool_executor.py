"""Safe executor for registered Open Signals internal tools."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.chat.retrieval_grounding import retrieve_relevant_signals
from Behavioral_Signals_AI.data_ingestion.privacy_filter import assert_no_private_fields
from Behavioral_Signals_AI.geography.county_matcher import signal_matches_location
from Behavioral_Signals_AI.signal_engine.category_learning import category_matches_signal
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals
from Behavioral_Signals_AI.storage.storage_manager import read_json
from Behavioral_Signals_AI.tools.tool_registry import get_tool
from Behavioral_Signals_AI.ui.feed_diff_engine import rank_signals_for_display

OUTPUTS_DIR = Path("Behavioral_Signals_AI/outputs")
PRIVATE_REQUEST_RE = re.compile(
    r"\b(user_id|device_id|phone|email|private message|private_message|exact location|gps|route|raw searches|raw likes|individual|personal profile)\b",
    re.IGNORECASE,
)


def execute_tool(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute one registered tool and return a structured aggregate-only result."""
    schema = get_tool(name)
    if not schema:
        return _failure(name, "tool_not_registered")
    args = dict(arguments or {})
    try:
        result = _dispatch(name, args)
        if not assert_no_private_fields(result):
            return _failure(name, "privacy_filter_blocked_output")
        return {"tool": name, "ok": True, "privacy_level": schema.privacy_level, "data": result}
    except Exception:
        return _failure(name, "tool_execution_failed")


def execute_tool_plan(calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Execute a sequence of routed tool calls safely."""
    results = []
    for call in calls or []:
        results.append(execute_tool(str(call.get("name") or ""), call.get("arguments") if isinstance(call.get("arguments"), dict) else {}))
    blocked = any(result.get("tool") == "privacy_check" and result.get("ok") and not result.get("data", {}).get("allowed", True) for result in results)
    if blocked:
        return [result for result in results if result.get("tool") == "privacy_check"]
    return results


def _dispatch(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "privacy_check":
        return _privacy_check(str(args.get("text") or ""))
    if name == "get_live_signals":
        return _live_signals(args.get("location", "Kenya"), args.get("category", "All"), args.get("urgency", "All"), int(args.get("limit", 6) or 6))
    if name == "get_top_signal":
        signals = _filtered_signals(args.get("location", "Kenya"), args.get("category", "All"), args.get("urgency", "All"), 1)
        return {"signal": signals[0] if signals else None}
    if name == "get_county_signals":
        county = str(args.get("county") or "")
        return {"county": county, "signals": retrieve_relevant_signals(county, str(args.get("category") or "All"), str(args.get("time_focus") or ""), {}, int(args.get("limit", 6) or 6))}
    if name == "compare_counties":
        return _compare_counties(str(args.get("county_a") or ""), str(args.get("county_b") or ""), str(args.get("category") or "All"), str(args.get("urgency") or "All"))
    if name == "get_category_signals":
        return {"category": str(args.get("category") or "All"), "signals": _filtered_signals(args.get("location", "Kenya"), args.get("category", "All"), args.get("urgency", "All"), int(args.get("limit", 6) or 6))}
    if name == "get_historical_pattern":
        return {"patterns": _memory_matches("historical_signal_memory.json", args, "historical")}
    if name == "get_outcome_learning":
        return {"outcomes": _memory_matches("outcome_learning_memory.json", args, "outcome")}
    if name == "get_geospatial_context":
        return {"context": _geospatial_context(str(args.get("county") or ""), str(args.get("category") or "All"))}
    if name == "get_forecast_context":
        return {"forecast": _forecast_context(str(args.get("county") or ""), str(args.get("category") or "All"))}
    if name == "get_source_freshness":
        return _source_freshness()
    if name == "get_evaluation_metrics":
        return {"metrics": read_json(OUTPUTS_DIR / "evaluation_metrics.json", {})}
    if name == "summarize_opportunities":
        return {"opportunities": _summaries(_filtered_signals(args.get("location", "Kenya"), args.get("category", "All"), "All", int(args.get("limit", 5) or 5)), "opportunity")}
    if name == "summarize_risks":
        return {"risks": _summaries(_filtered_signals(args.get("location", "Kenya"), args.get("category", "All"), "All", int(args.get("limit", 5) or 5)), "risk")}
    return {}


def _privacy_check(text: str) -> dict[str, Any]:
    allowed = assert_no_private_fields({"prompt": text}) and not PRIVATE_REQUEST_RE.search(text or "")
    return {
        "allowed": bool(allowed),
        "reason": "aggregate_only_request" if allowed else "private_or_individual_level_request_blocked",
    }


def _live_signals(location: Any, category: Any, urgency: Any, limit: int) -> dict[str, Any]:
    payload = get_cached_or_fallback_signals()
    return {
        "source_status": str(payload.get("status") or "unknown"),
        "last_updated": str(payload.get("last_updated") or ""),
        "signals": _filtered_signals(str(location or "Kenya"), str(category or "All"), str(urgency or "All"), limit),
    }


def _filtered_signals(location: Any, category: Any, urgency: Any, limit: int) -> list[dict[str, Any]]:
    payload = get_cached_or_fallback_signals()
    signals = [dict(signal, _cache_status=payload.get("status"), _cache_last_updated=payload.get("last_updated")) for signal in payload.get("signals", []) if isinstance(signal, dict)]
    filtered = []
    for signal in signals:
        if category and category != "All" and not category_matches_signal(signal, str(category)):
            continue
        if urgency and urgency != "All" and str(signal.get("urgency", "")).lower() != str(urgency).lower():
            continue
        if location not in {"", "All", "Kenya", "Global"} and not signal_matches_location(signal, str(location)):
            continue
        filtered.append(_safe_signal(signal))
    if not filtered and location not in {"", "All", "Kenya", "Global"}:
        filtered = [_safe_signal(signal) for signal in signals if category in {"", "All"} or category_matches_signal(signal, str(category))]
    return rank_signals_for_display(filtered)[:limit]


def _compare_counties(county_a: str, county_b: str, category: str, urgency: str) -> dict[str, Any]:
    comparison = []
    for county in [county_a, county_b]:
        top = retrieve_relevant_signals(county, category, "", {}, 1)
        comparison.append({"county": county, "top_signal": _safe_signal(top[0]) if top else None})
    return {"comparison": comparison, "category": category, "urgency": urgency}


def _memory_matches(filename: str, args: dict[str, Any], memory_type: str) -> list[dict[str, Any]]:
    data = read_json(OUTPUTS_DIR / filename, {})
    records = _extract_records(data)
    query = " ".join(str(args.get(key) or "") for key in ["topic", "county", "category"]).lower()
    matches = []
    for record in records:
        safe = _safe_record(record)
        blob = " ".join(str(value).lower() for value in safe.values())
        if not query.strip() or any(term and term in blob for term in query.split()):
            matches.append(dict(safe, memory_type=memory_type))
    return matches[: int(args.get("limit", 5) or 5)]


def _geospatial_context(county: str, category: str) -> dict[str, Any]:
    signals = retrieve_relevant_signals(county, category, "", {}, 3)
    return {
        "county": county,
        "category": category,
        "signal_count": len(signals),
        "top_geospatial_insight": signals[0].get("geospatial_insight") if signals else "",
        "spread_risk": signals[0].get("spread_risk") if signals else "unknown",
    }


def _forecast_context(county: str, category: str) -> dict[str, Any]:
    signals = retrieve_relevant_signals(county, category, "emerging", {}, 3)
    top = signals[0] if signals else {}
    return {
        "county": county,
        "category": category,
        "forecast_direction": top.get("forecast_direction") or top.get("predicted_direction") or "Unknown",
        "confidence": top.get("confidence_score"),
        "topic": top.get("signal_topic"),
        "spread_risk": top.get("spread_risk"),
    }


def _source_freshness() -> dict[str, Any]:
    payload = get_cached_or_fallback_signals()
    timestamp = str(payload.get("last_updated") or "")
    status = str(payload.get("status") or "unknown")
    freshness = "fallback/sample-only" if "sample" in status.lower() or "fallback" in status.lower() else "insufficient evidence"
    if timestamp:
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=UTC)
            age_hours = (datetime.now(UTC) - parsed.astimezone(UTC)).total_seconds() / 3600
            freshness = "fresh" if age_hours <= 6 else "recently updated" if age_hours <= 48 else "stale"
        except ValueError:
            pass
    return {"freshness": freshness, "last_updated": timestamp, "status": status}


def _summaries(signals: list[dict[str, Any]], mode: str) -> list[dict[str, Any]]:
    key = "opportunity_level" if mode == "opportunity" else "urgency"
    ranked = sorted(signals, key=lambda signal: _level_score(signal.get(key)) + _safe_number(signal.get("confidence_score")) / 10, reverse=True)
    return [
        {
            "topic": signal.get("signal_topic"),
            "county_or_scope": signal.get("county_name") or signal.get("geographic_scope"),
            "category": signal.get("signal_category"),
            "confidence": signal.get("confidence_score"),
            "summary": signal.get("interpretation") or signal.get("recommended_action"),
        }
        for signal in ranked[:5]
    ]


def _extract_records(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ["records", "signals", "items", "memory", "clusters", "outcomes", "patterns"]:
            if isinstance(data.get(key), list):
                return [item for item in data[key] if isinstance(item, dict)]
        return [data] if data else []
    return []


def _safe_signal(signal: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "signal_topic", "signal_category", "demand_level", "opportunity_level", "unmet_demand_likelihood",
        "urgency", "geographic_scope", "county_name", "source_summary", "confidence_score", "priority_score",
        "behavioral_intelligence_score", "momentum", "forecast_direction", "spread_risk", "interpretation",
        "recommended_action", "historical_pattern_match", "outcome_learning_note", "validation_status",
        "geospatial_insight", "last_updated", "_cache_status", "_cache_last_updated", "_retrieval_grounding_score",
    }
    return {key: value for key, value in signal.items() if key in allowed}


def _safe_record(record: dict[str, Any]) -> dict[str, Any]:
    safe = {}
    for key, value in record.items():
        if str(key).lower() in {"name", "email", "phone", "user_id", "device_id", "exact_location", "route", "private_message"}:
            continue
        safe[str(key)] = value
    return safe if assert_no_private_fields(safe) else {}


def _level_score(value: Any) -> float:
    return {"very high": 100, "high": 80, "medium": 55, "moderate": 55, "low": 25}.get(str(value or "").lower(), 40)


def _safe_number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _failure(name: str, reason: str) -> dict[str, Any]:
    return {
        "tool": str(name or "unknown"),
        "ok": False,
        "privacy_level": "aggregate_public",
        "error": reason,
        "data": {"fallback": "Tool result unavailable; continue with existing aggregate context."},
    }
