"""Aggregate model metrics for Behavioral Signals AI."""

from __future__ import annotations

from Behavioral_Signals_AI.adaptive_learning.accuracy_tracker import summarize_accuracy


def compute_model_metrics(records: list[dict]) -> dict:
    summary = summarize_accuracy(records)
    return {
        "prediction_count": len(records),
        "evaluated_predictions": summary["evaluated_predictions"],
        "average_accuracy": summary["average_accuracy"],
        "pending_predictions": summary["pending_predictions"],
        "privacy_level": "aggregate_public",
    }