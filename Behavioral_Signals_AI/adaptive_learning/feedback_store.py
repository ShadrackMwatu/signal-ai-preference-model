"""Feedback storage for later aggregate prediction evaluation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .prediction_memory import load_prediction_memory, save_prediction_snapshot


def record_feedback(signal_name: str, actual_signal_strength: float, path: str | Path | None = None) -> dict[str, Any]:
    record = {
        "signal_name": signal_name,
        "actual_follow_up_signal_strength": round(float(actual_signal_strength), 2),
        "accuracy_result": "feedback_recorded",
        "privacy_level": "aggregate_public",
    }
    return save_prediction_snapshot(record, path=path)


def latest_feedback(limit: int = 50, path: str | Path | None = None) -> list[dict[str, Any]]:
    return [row for row in load_prediction_memory(limit=limit, path=path) if row.get("actual_follow_up_signal_strength") is not None]