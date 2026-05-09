"""Evaluation metrics for Signal ML models."""

from __future__ import annotations

import math
from typing import Any

from sklearn.metrics import accuracy_score, classification_report, mean_squared_error


def evaluate_classification(y_true: Any, y_pred: Any) -> dict[str, Any]:
    """Return accuracy and a full classification report."""

    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 6),
        "classification_report": classification_report(y_true, y_pred, output_dict=True, zero_division=0),
    }


def evaluate_regression(y_true: Any, y_pred: Any) -> dict[str, float]:
    """Return regression RMSE and MSE."""

    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "mse": round(mse, 6),
        "rmse": round(math.sqrt(mse), 6),
    }
