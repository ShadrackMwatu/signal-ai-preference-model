"""Prediction evaluation helpers."""

from __future__ import annotations

from Behavioral_Signals_AI.adaptive_learning.accuracy_tracker import evaluate_prediction_accuracy


def evaluate_prediction_batch(records: list[dict]) -> list[dict]:
    return [{**record, **evaluate_prediction_accuracy(record)} for record in records]