"""Lightweight prediction memory for aggregate Behavioral Signals AI outputs."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MEMORY_DIR = Path(__file__).resolve().parents[1] / "data" / "prediction_memory"
MEMORY_FILE = MEMORY_DIR / "prediction_memory.jsonl"
PERSONAL_FIELDS = {"username", "user_id", "screen_name", "author_id", "profile_url", "email", "phone", "text", "raw_post"}


def prediction_memory_path() -> Path:
    override = os.getenv("SIGNAL_PREDICTION_MEMORY_PATH", "").strip()
    return Path(override) if override else MEMORY_FILE


def save_prediction_snapshot(prediction: dict[str, Any], path: str | Path | None = None) -> dict[str, Any]:
    """Append one privacy-safe aggregate prediction snapshot."""

    record = _sanitize_prediction(prediction)
    record.setdefault("timestamp", datetime.now(UTC).isoformat())
    target = Path(path) if path else prediction_memory_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")
    return record


def load_prediction_memory(limit: int = 100, path: str | Path | None = None) -> list[dict[str, Any]]:
    target = Path(path) if path else prediction_memory_path()
    if not target.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows[-max(1, int(limit)):]


def build_prediction_snapshot(signal: dict[str, Any]) -> dict[str, Any]:
    """Create the standard memory record from an enriched demand signal."""

    return _sanitize_prediction(
        {
            "timestamp": datetime.now(UTC).isoformat(),
            "signal_name": signal.get("trend_name") or signal.get("signal_name"),
            "category": signal.get("category") or signal.get("inferred_demand_category"),
            "source": signal.get("source"),
            "predicted_demand_level": signal.get("revealed_aggregate_demand") or signal.get("demand_signal_strength"),
            "predicted_opportunity": signal.get("opportunity_score") or signal.get("opportunity_type"),
            "confidence": signal.get("confidence_score") or signal.get("confidence"),
            "actual_follow_up_signal_strength": signal.get("actual_follow_up_signal_strength"),
            "persistence_score": signal.get("persistence") or signal.get("demand_persistence"),
            "accuracy_result": signal.get("accuracy_result", "pending"),
            "privacy_level": "aggregate_public",
        }
    )


def _sanitize_prediction(prediction: dict[str, Any]) -> dict[str, Any]:
    sanitized = {key: value for key, value in dict(prediction).items() if key not in PERSONAL_FIELDS}
    sanitized["privacy_level"] = "aggregate_public"
    return sanitized