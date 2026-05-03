"""Evaluation and drift detection for Signal market intelligence."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, precision_score, recall_score

from .features import FEATURE_COLUMNS


def classification_metrics(y_true, y_pred) -> dict[str, float]:
    """Return standard classification metrics."""

    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, average="weighted", zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, average="weighted", zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, average="weighted", zero_division=0)), 4),
    }


def regression_metrics(y_true, y_pred) -> dict[str, float]:
    """Return RMSE and MAE for model score predictions."""

    mse = mean_squared_error(y_true, y_pred)
    return {
        "rmse": round(float(np.sqrt(mse)), 4),
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
    }


def feature_profile(features: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Profile feature means and standard deviations for drift detection."""

    return {
        column: {
            "mean": round(float(features[column].mean()), 6),
            "std": round(float(features[column].std(ddof=0)), 6),
        }
        for column in FEATURE_COLUMNS
    }


def detect_feature_drift(
    baseline_profile: dict[str, dict[str, float]],
    current_features: pd.DataFrame,
    threshold: float = 0.15,
) -> dict[str, object]:
    """Detect feature distribution drift from baseline training data."""

    current_profile = feature_profile(current_features)
    drifted: list[str] = []
    distances: list[float] = []
    for column in FEATURE_COLUMNS:
        baseline_mean = baseline_profile[column]["mean"]
        baseline_std = max(baseline_profile[column]["std"], 0.01)
        distance = abs(current_profile[column]["mean"] - baseline_mean) / baseline_std
        distances.append(distance)
        if distance > threshold:
            drifted.append(column)

    drift_score = round(float(np.mean(distances)), 4)
    return {
        "drift_score": drift_score,
        "drifted_features": drifted,
        "threshold": threshold,
        "retraining_recommended": bool(drifted),
    }


def evaluate_signal_system(system, frame: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Evaluate trained demand classifiers and regressors against labeled data."""

    predictions = pd.DataFrame(system.predict(frame)["records"])
    return {
        "classification": classification_metrics(frame["demand_classification"], predictions["demand_classification"]),
        "aggregate_demand_score": regression_metrics(
            frame["aggregate_demand_score_target"],
            predictions["aggregate_demand_score"],
        ),
        "opportunity_score": regression_metrics(frame["opportunity_score_target"], predictions["opportunity_score"]),
        "market_gap": regression_metrics(frame["market_gap_target"], predictions["market_gap"]),
    }
