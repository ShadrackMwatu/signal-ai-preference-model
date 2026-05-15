"""Historical forecasting for Behavioral Signals AI."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.signal_engine.historical_adaptation_engine import find_similar_historical_episodes
from Behavioral_Signals_AI.signal_engine.historical_memory import append_forecast_memory


def add_historical_forecast(signal: dict[str, Any]) -> dict[str, Any]:
    matches = find_similar_historical_episodes(signal)
    direction = _forecast_direction(signal, matches)
    confidence = _forecast_confidence(signal, matches)
    likely_next = _likely_next_development(signal, direction, matches)
    lesson = signal.get("historical_lesson_used") or _historical_lesson(matches)
    forecasted = dict(signal)
    forecasted.update(
        {
            "forecast_direction": direction,
            "forecast_confidence": confidence,
            "forecast_reasoning": _forecast_reasoning(signal, matches, direction),
            "likely_next_development": likely_next,
            "historical_lesson_used": lesson,
            "likely_affected_sectors": _likely_sectors(signal, matches),
            "likely_affected_counties": _likely_counties(signal, matches),
            "likely_policy_concern": _likely_policy_concern(signal, matches),
            "likely_market_opportunity": _likely_market_opportunity(signal, matches),
        }
    )
    return forecasted


def persist_forecasts(signals: list[dict[str, Any]]) -> dict[str, Any]:
    return append_forecast_memory(signals)


def _forecast_direction(signal: dict[str, Any], matches: list[dict[str, Any]]) -> str:
    predicted = str(signal.get("predicted_direction", "stable")).lower()
    if predicted == "rising":
        return "Rising"
    if predicted == "declining":
        return "Declining"
    high_matches = sum(1 for record in matches if record.get("future_relevance") == "High")
    if high_matches >= 2:
        return "Rising"
    return "Stable"


def _forecast_confidence(signal: dict[str, Any], matches: list[dict[str, Any]]) -> float:
    base = _num(signal.get("forecast_confidence"), _num(signal.get("confidence_score"), 50))
    base += min(16.0, len(matches) * 3.0)
    if signal.get("historical_pattern_match") and signal.get("historical_pattern_match") != "No close historical pattern yet":
        base += 5.0
    return round(max(20.0, min(96.0, base)), 1)


def _likely_next_development(signal: dict[str, Any], direction: str, matches: list[dict[str, Any]]) -> str:
    category = str(signal.get("signal_category", "aggregate demand"))
    if direction == "Rising":
        return f"The {category} signal may persist or spread if related affordability, supply, or public concern signals also rise."
    if direction == "Declining":
        return f"The {category} signal may fade unless confirmed by new aggregate sources."
    return f"The {category} signal is likely to remain watch-listed while the system checks persistence."


def _forecast_reasoning(signal: dict[str, Any], matches: list[dict[str, Any]], direction: str) -> str:
    pieces = [f"Forecast is {direction.lower()} based on current momentum and adaptive confidence"]
    if matches:
        pieces.append(f"{len(matches)} similar historical episode(s) were found")
    if signal.get("seasonal_recurrence") not in {None, "None detected"}:
        pieces.append(f"seasonal recurrence is {signal.get('seasonal_recurrence')}")
    if signal.get("county_recurrence"):
        pieces.append(str(signal.get("county_recurrence")))
    return "; ".join(pieces) + "."


def _historical_lesson(matches: list[dict[str, Any]]) -> str:
    for record in matches:
        if record.get("lessons_learned"):
            return str(record.get("lessons_learned"))
    return "Historical memory is still accumulating lessons for this signal type."


def _likely_sectors(signal: dict[str, Any], matches: list[dict[str, Any]]) -> list[str]:
    sectors = {str(signal.get("signal_category", "other"))}
    sectors.update(str(record.get("category")) for record in matches if record.get("category"))
    return sorted(sector for sector in sectors if sector and sector != "None")[:6]


def _likely_counties(signal: dict[str, Any], matches: list[dict[str, Any]]) -> list[str]:
    counties = {str(signal.get("geographic_scope", "Kenya-wide"))}
    counties.update(str(record.get("county_or_scope")) for record in matches if record.get("county_or_scope"))
    return sorted(county for county in counties if county and county != "None")[:8]


def _likely_policy_concern(signal: dict[str, Any], matches: list[dict[str, Any]]) -> str:
    category = str(signal.get("signal_category", "other"))
    if category in {"food and agriculture", "cost of living", "water and sanitation", "health", "jobs and labour market"}:
        return "Moderate to high if signal persistence and public concern increase."
    return "Monitor for policy relevance as validation evidence accumulates."


def _likely_market_opportunity(signal: dict[str, Any], matches: list[dict[str, Any]]) -> str:
    opportunity = signal.get("business_opportunity") or signal.get("recommended_action")
    return str(opportunity or "Monitor for emerging supply, affordability, and service delivery opportunities.")


def _num(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default
