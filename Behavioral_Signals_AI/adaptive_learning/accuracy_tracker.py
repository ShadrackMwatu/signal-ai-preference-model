"""Accuracy tracking for aggregate demand and opportunity predictions."""

from __future__ import annotations

from typing import Any


def evaluate_prediction_accuracy(prediction: dict[str, Any]) -> dict[str, Any]:
    predicted = _score(prediction.get("demand_signal_strength") or prediction.get("predicted_demand_level"))
    actual = _score(prediction.get("actual_follow_up_signal_strength"))
    if actual is None:
        return {"accuracy_result": "pending", "accuracy_score": None, "prediction_error": None}
    error = abs(float(predicted or 0.0) - float(actual))
    return {
        "accuracy_result": "accurate" if error <= 15 else "directionally_useful" if error <= 30 else "missed",
        "accuracy_score": round(max(0.0, 100.0 - error), 2),
        "prediction_error": round(error, 2),
    }


def summarize_accuracy(records: list[dict[str, Any]]) -> dict[str, Any]:
    evaluated = [evaluate_prediction_accuracy(row) for row in records]
    scored = [row["accuracy_score"] for row in evaluated if row.get("accuracy_score") is not None]
    return {
        "evaluated_predictions": len(scored),
        "average_accuracy": round(sum(scored) / len(scored), 2) if scored else None,
        "pending_predictions": sum(1 for row in evaluated if row.get("accuracy_result") == "pending"),
    }


def _score(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).lower()
    if "high" in text:
        return 82.0
    if "moderate" in text:
        return 60.0
    if "emerging" in text:
        return 45.0
    if "low" in text:
        return 25.0
    try:
        return float(text)
    except ValueError:
        return None