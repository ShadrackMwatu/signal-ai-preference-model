"""Yearly learning summaries for Behavioral Signals AI."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from Behavioral_Signals_AI.signal_engine.historical_memory import HISTORICAL_MEMORY_PATH, HISTORY_ROOT, load_json, write_json


def summarize_yearly_patterns(year: str | None = None) -> dict[str, Any]:
    target_year = year or datetime.now(UTC).strftime("%Y")
    records = _records_for_prefix(target_year)
    summary = {
        "period": "yearly",
        "year": target_year,
        "major_national_demand_shifts": _top_counts(record.get("signal_cluster") for record in records),
        "recurring_household_pressures": _top_counts(record.get("category") for record in records if record.get("category") in {"food and agriculture", "cost of living", "energy", "housing", "transport"}),
        "county_level_structural_signals": _top_counts(record.get("county_or_scope") for record in records if record.get("county_or_scope") != "Kenya-wide"),
        "policy_relevant_early_warnings": [record.get("signal_topic") for record in records if record.get("future_relevance") == "High"][-20:],
        "sectors_with_repeated_opportunity_signals": _top_counts(record.get("category") for record in records if float(record.get("opportunity_intelligence_score", 0)) >= 65),
        "historical_lessons": _lessons(records),
        "predictive_rules_learned": _predictive_rules(records),
        "generated_at": datetime.now(UTC).isoformat(),
    }
    write_json(HISTORY_ROOT / "yearly" / f"{target_year}.json", summary)
    return summary


def _records_for_prefix(prefix: str) -> list[dict[str, Any]]:
    payload = load_json(HISTORICAL_MEMORY_PATH, {"records": []})
    records = payload.get("records", []) if isinstance(payload, dict) else []
    return [record for record in records if str(record.get("date", "")).startswith(prefix)]


def _top_counts(values: Any) -> dict[str, int]:
    return dict(Counter(str(value) for value in values if value).most_common(10))


def _lessons(records: list[dict[str, Any]]) -> list[str]:
    lessons = [str(record.get("lessons_learned")) for record in records if record.get("lessons_learned")]
    return lessons[-20:]


def _predictive_rules(records: list[dict[str, Any]]) -> list[str]:
    rules: list[str] = []
    categories = _top_counts(record.get("category") for record in records if record.get("future_relevance") == "High")
    for category in list(categories)[:5]:
        rules.append(f"Give stronger attention to recurring {category} signals when confidence and urgency rise together.")
    if not rules:
        rules.append("Continue collecting validated outcomes before strengthening annual predictive rules.")
    return rules
