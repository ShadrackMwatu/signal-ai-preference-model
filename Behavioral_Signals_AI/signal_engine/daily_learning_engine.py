"""Daily learning summaries for Behavioral Signals AI."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.signal_engine.historical_memory import HISTORY_ROOT, update_historical_memory, write_json


def summarize_daily_signals(signals: list[dict[str, Any]], date: str | None = None) -> dict[str, Any]:
    day = date or datetime.now(UTC).date().isoformat()
    ordered = sorted(signals, key=lambda item: float(item.get("confidence_score", 0)), reverse=True)
    summary = {
        "period": "daily",
        "date": day,
        "top_signals": [signal.get("signal_topic") for signal in ordered[:5]],
        "emerging_signals": [signal.get("signal_topic") for signal in signals if signal.get("momentum") in {"Rising", "Breakout"}][:8],
        "declining_signals": [signal.get("signal_topic") for signal in signals if signal.get("momentum") == "Declining"][:8],
        "persistent_signals": [signal.get("signal_topic") for signal in signals if signal.get("persistence_badge") == "Persistent"][:8],
        "validated_signals": [signal.get("signal_topic") for signal in signals if signal.get("validation_status") == "validated"][:8],
        "false_positive_candidates": [signal.get("signal_topic") for signal in signals if signal.get("validation_status") == "unvalidated" and float(signal.get("confidence_score", 0)) < 45],
        "sectors_under_pressure": _top_counts(signal.get("signal_category") for signal in signals),
        "counties_with_recurring_signals": _top_counts(signal.get("geographic_scope") for signal in signals if signal.get("geographic_scope") != "Kenya-wide"),
        "opportunities_detected": [signal.get("business_opportunity") or signal.get("recommended_action") for signal in ordered[:5]],
        "policy_concerns_detected": [signal.get("policy_opportunity") for signal in signals if signal.get("policy_opportunity")][:5],
        "generated_at": datetime.now(UTC).isoformat(),
    }
    target = HISTORY_ROOT / "daily" / f"{day}.json"
    write_json(target, summary)
    update_historical_memory(signals, period="daily")
    return summary


def _top_counts(values: Any) -> dict[str, int]:
    counter = Counter(str(value) for value in values if value)
    return dict(counter.most_common(8))
