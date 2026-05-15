"""Learning registry summaries for Behavioral Signals AI."""

from __future__ import annotations

from .accuracy_tracker import summarize_accuracy
from .model_updater import suggest_model_updates, update_adaptive_weights
from .prediction_memory import load_prediction_memory


def summarize_learning_state(limit: int = 100) -> dict:
    records = load_prediction_memory(limit=limit)
    return {
        "memory_records": len(records),
        "accuracy": summarize_accuracy(records),
        "adaptive_weights": update_adaptive_weights(records),
        "model_update_suggestions": suggest_model_updates(records),
        "privacy_level": "aggregate_public",
    }