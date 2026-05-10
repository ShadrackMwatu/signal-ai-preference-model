"""Privacy-safe feedback logging for adaptive Signal retraining."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


FEEDBACK_LOG_PATH = Path("data") / "feedback" / "feedback_log.csv"
FEEDBACK_COLUMNS = [
    "timestamp",
    "county",
    "topic",
    "time_period",
    "prediction_source",
    "predicted_demand_classification",
    "observed_demand_classification",
    "opportunity_score",
    "confidence_score",
    "feedback_note",
]
BLOCKED_FIELDS = {"user_id", "username", "name", "email", "phone", "gps", "exact_location"}


def initialize_feedback_log(path: str | Path = FEEDBACK_LOG_PATH) -> Path:
    feedback_path = Path(path)
    feedback_path.parent.mkdir(parents=True, exist_ok=True)
    if not feedback_path.exists():
        pd.DataFrame(columns=FEEDBACK_COLUMNS).to_csv(feedback_path, index=False)
    return feedback_path


def record_feedback(
    feedback: dict[str, Any],
    path: str | Path = FEEDBACK_LOG_PATH,
) -> dict[str, Any]:
    safe_feedback = {key: value for key, value in feedback.items() if key not in BLOCKED_FIELDS}
    row = {
        "timestamp": datetime.now(UTC).isoformat(),
        "county": safe_feedback.get("county", "aggregate"),
        "topic": safe_feedback.get("topic", "general"),
        "time_period": safe_feedback.get("time_period", "unspecified"),
        "prediction_source": safe_feedback.get("prediction_source", "unknown"),
        "predicted_demand_classification": safe_feedback.get("predicted_demand_classification", ""),
        "observed_demand_classification": safe_feedback.get("observed_demand_classification", ""),
        "opportunity_score": float(safe_feedback.get("opportunity_score", 0) or 0),
        "confidence_score": float(safe_feedback.get("confidence_score", 0) or 0),
        "feedback_note": str(safe_feedback.get("feedback_note", "")),
    }

    feedback_path = initialize_feedback_log(path)
    history = pd.read_csv(feedback_path)
    if history.empty:
        updated = pd.DataFrame([row], columns=FEEDBACK_COLUMNS)
    else:
        updated = pd.concat([history, pd.DataFrame([row])], ignore_index=True)
    updated.to_csv(feedback_path, index=False)
    return row


def load_feedback(path: str | Path = FEEDBACK_LOG_PATH) -> pd.DataFrame:
    feedback_path = initialize_feedback_log(path)
    return pd.read_csv(feedback_path)


def aggregate_feedback_for_retraining(path: str | Path = FEEDBACK_LOG_PATH) -> pd.DataFrame:
    frame = load_feedback(path)
    if frame.empty:
        return frame
    return (
        frame.groupby(["county", "topic", "time_period", "predicted_demand_classification"], dropna=False)
        .agg(
            feedback_count=("predicted_demand_classification", "size"),
            average_opportunity_score=("opportunity_score", "mean"),
            average_confidence_score=("confidence_score", "mean"),
            most_recent_feedback=("timestamp", "max"),
        )
        .reset_index()
    )
