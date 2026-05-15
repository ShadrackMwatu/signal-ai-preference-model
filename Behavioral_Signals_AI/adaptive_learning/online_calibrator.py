"""Rule-based online calibration for aggregate Behavioral Signals predictions."""

from __future__ import annotations

from typing import Any

DEFAULT_WEIGHTS = {
    "source_reliability": 0.22,
    "signal_persistence": 0.18,
    "cross_provider_confirmation": 0.18,
    "historical_accuracy": 0.16,
    "trend_growth": 0.14,
    "search_intensity": 0.12,
}
SOURCE_PRIORS = {
    "Google Trends": 0.9,
    "SerpAPI Google Trends": 0.86,
    "pytrends": 0.78,
    "X": 0.68,
    "GDELT": 0.72,
    "News API": 0.7,
    "Demo fallback": 0.5,
}


def calibrate_prediction(signal: dict[str, Any], history: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Return adaptive calibration factors for one aggregate signal."""

    history = history or []
    source = str(signal.get("source", "Demo fallback"))
    repeated = _repeat_count(signal, history)
    cross_source = _cross_source_count(signal, history)
    history_accuracy = _historical_accuracy(signal, history)
    growth_score = _growth_score(signal.get("growth") or signal.get("growth_indicator"))
    search_intensity = _percent(signal.get("search_intensity") or signal.get("volume"), cap=250000)
    persistence = min(100.0, 45.0 + (repeated * 12.0))

    weighted = (
        SOURCE_PRIORS.get(source, 0.62) * 100 * DEFAULT_WEIGHTS["source_reliability"]
        + persistence * DEFAULT_WEIGHTS["signal_persistence"]
        + min(100.0, cross_source * 35.0) * DEFAULT_WEIGHTS["cross_provider_confirmation"]
        + history_accuracy * DEFAULT_WEIGHTS["historical_accuracy"]
        + growth_score * DEFAULT_WEIGHTS["trend_growth"]
        + search_intensity * DEFAULT_WEIGHTS["search_intensity"]
    )
    return {
        "adaptive_confidence": round(min(max(weighted, 5.0), 98.0), 2),
        "source_reliability": round(SOURCE_PRIORS.get(source, 0.62) * 100, 2),
        "signal_persistence": round(persistence, 2),
        "cross_provider_confirmation": cross_source,
        "historical_accuracy": round(history_accuracy, 2),
        "learning_status": "adaptive_rule_based",
    }


def _repeat_count(signal: dict[str, Any], history: list[dict[str, Any]]) -> int:
    key = _key(signal.get("signal_name") or signal.get("trend_name"))
    return sum(1 for row in history if _key(row.get("signal_name") or row.get("trend_name")) == key)


def _cross_source_count(signal: dict[str, Any], history: list[dict[str, Any]]) -> int:
    key = _key(signal.get("signal_name") or signal.get("trend_name"))
    sources = {str(row.get("source")) for row in history if _key(row.get("signal_name") or row.get("trend_name")) == key}
    if signal.get("source"):
        sources.add(str(signal.get("source")))
    return len(sources)


def _historical_accuracy(signal: dict[str, Any], history: list[dict[str, Any]]) -> float:
    category = str(signal.get("category") or signal.get("inferred_demand_category") or "").lower()
    scores = [float(row.get("accuracy_score")) for row in history if str(row.get("category", "")).lower() == category and row.get("accuracy_score") is not None]
    return sum(scores) / len(scores) if scores else 58.0


def _growth_score(value: Any) -> float:
    text = str(value or "").lower()
    if "breakout" in text:
        return 95.0
    if "rising" in text or "+" in text:
        return 78.0
    if "declin" in text or "down" in text:
        return 28.0
    return 55.0


def _percent(value: Any, cap: float = 100.0) -> float:
    if value is None:
        return 45.0
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 45.0
    if number <= 1:
        return number * 100
    return min((number / cap) * 100, 100.0)


def _key(value: Any) -> str:
    return " ".join(str(value or "").lower().replace("#", "").split()[:4])