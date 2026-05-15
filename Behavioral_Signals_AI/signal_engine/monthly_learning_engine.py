"""Monthly learning summaries for Behavioral Signals AI."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.signal_engine.historical_memory import HISTORICAL_MEMORY_PATH, HISTORY_ROOT, load_json, write_json


def summarize_monthly_patterns(month: str | None = None) -> dict[str, Any]:
    target_month = month or datetime.now(UTC).strftime("%Y-%m")
    records = _records_for_prefix(target_month)
    summary = {
        "period": "monthly",
        "month": target_month,
        "recurring_themes": _top_counts(record.get("signal_cluster") for record in records),
        "sector_patterns": _top_counts(record.get("category") for record in records),
        "county_patterns": _top_counts(record.get("county_or_scope") for record in records),
        "strongest_demand_categories": _top_by_average(records, "category", "demand_intelligence_score"),
        "most_persistent_unmet_needs": _top_counts(record.get("signal_topic") for record in records if record.get("future_relevance") == "High"),
        "signals_that_became_important": [record.get("signal_topic") for record in records if record.get("future_relevance") == "High"][-10:],
        "signals_that_faded": [record.get("signal_topic") for record in records if record.get("momentum_label") == "Declining"][-10:],
        "seasonal_patterns": _seasonal_note(records),
        "lessons_for_future_scoring": _lessons(records),
        "generated_at": datetime.now(UTC).isoformat(),
    }
    write_json(HISTORY_ROOT / "monthly" / f"{target_month}.json", summary)
    return summary


def _records_for_prefix(prefix: str) -> list[dict[str, Any]]:
    payload = load_json(HISTORICAL_MEMORY_PATH, {"records": []})
    records = payload.get("records", []) if isinstance(payload, dict) else []
    return [record for record in records if str(record.get("date", "")).startswith(prefix)]


def _top_counts(values: Any) -> dict[str, int]:
    return dict(Counter(str(value) for value in values if value).most_common(8))


def _top_by_average(records: list[dict[str, Any]], group_key: str, value_key: str) -> dict[str, float]:
    buckets: dict[str, list[float]] = {}
    for record in records:
        group = str(record.get(group_key) or "unknown")
        try:
            buckets.setdefault(group, []).append(float(record.get(value_key, 0)))
        except Exception:
            pass
    averaged = {key: round(sum(values) / len(values), 2) for key, values in buckets.items() if values}
    return dict(sorted(averaged.items(), key=lambda item: item[1], reverse=True)[:8])


def _seasonal_note(records: list[dict[str, Any]]) -> str:
    if not records:
        return "No monthly historical evidence yet."
    categories = _top_counts(record.get("category") for record in records)
    top = next(iter(categories), "aggregate demand")
    return f"This month currently shows recurring attention around {top}; future cycles will refine seasonality."


def _lessons(records: list[dict[str, Any]]) -> list[str]:
    lessons = [str(record.get("lessons_learned")) for record in records if record.get("lessons_learned")]
    return lessons[-12:]
