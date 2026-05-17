"""County-aware retrieval grounding for Open Signals chat."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.geography.county_matcher import signal_matches_location
from Behavioral_Signals_AI.signal_engine.category_learning import category_matches_signal
from Behavioral_Signals_AI.signal_engine.signal_cache import get_cached_or_fallback_signals
from Behavioral_Signals_AI.ui.feed_diff_engine import rank_signals_for_display


def retrieve_relevant_signals(
    county: str = "",
    category: str = "",
    time_focus: str = "",
    session_context: dict[str, str] | None = None,
    limit: int = 6,
) -> list[dict[str, Any]]:
    """Retrieve and rank current interpreted signals for a county/category query."""
    payload = get_cached_or_fallback_signals()
    status = str(payload.get("status") or "unknown")
    cache_last_updated = str(payload.get("last_updated") or "")
    raw_signals = [signal for signal in payload.get("signals", []) if isinstance(signal, dict)]
    scored: list[tuple[float, dict[str, Any]]] = []
    effective_county = county or str((session_context or {}).get("last_county") or "")
    effective_category = category or str((session_context or {}).get("last_category") or "All")
    for signal in raw_signals:
        enriched = dict(signal, _cache_status=status, _cache_last_updated=cache_last_updated)
        score = _grounding_score(enriched, effective_county, effective_category, time_focus)
        if score > 0:
            enriched["_retrieval_grounding_score"] = round(score, 2)
            scored.append((score, enriched))
    scored.sort(key=lambda item: item[0], reverse=True)
    ranked = [signal for _, signal in scored[:limit]]
    if ranked:
        return ranked
    return rank_signals_for_display([
        dict(signal, _cache_status=status, _cache_last_updated=cache_last_updated, _retrieval_grounding_score=0)
        for signal in raw_signals
    ])[:limit]


def _grounding_score(signal: dict[str, Any], county: str, category: str, time_focus: str) -> float:
    score = 0.0
    if county:
        score += 45 if signal_matches_location(signal, county) else -30
    else:
        score += 10
    if category and category != "All":
        score += 25 if category_matches_signal(signal, category) else -10
    score += min(20.0, _safe_number(signal.get("confidence_score")) / 5)
    score += min(20.0, max(_safe_number(signal.get("priority_score")), _safe_number(signal.get("behavioral_intelligence_score"))) / 5)
    urgency = str(signal.get("urgency") or "").lower()
    if urgency == "high":
        score += 12
    elif urgency == "medium":
        score += 6
    momentum = str(signal.get("momentum") or signal.get("forecast_direction") or "").lower()
    if any(term in momentum for term in ["rising", "breakout", "accelerat"]):
        score += 12
    elif any(term in momentum for term in ["stable", "persistent"]):
        score += 5
    if str(signal.get("validation_status") or "").lower().replace("_", " ") in {"validated", "partially validated"}:
        score += 8
    if time_focus:
        score += _recency_score(signal)
        if time_focus == "emerging" and any(term in momentum for term in ["rising", "breakout", "accelerat"]):
            score += 8
    return score


def _recency_score(signal: dict[str, Any]) -> float:
    timestamp = str(signal.get("last_updated") or signal.get("_cache_last_updated") or "")
    if not timestamp:
        return 2.0
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        age_hours = (datetime.now(UTC) - parsed.astimezone(UTC)).total_seconds() / 3600
    except ValueError:
        return 2.0
    if age_hours <= 6:
        return 14.0
    if age_hours <= 48:
        return 9.0
    return 3.0


def _safe_number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0
