"""Feature drift detection using mean and standard-deviation shifts."""

from __future__ import annotations

import pandas as pd

from src.features.feature_engineering import FEATURE_COLUMNS
from src.models.train_demand_model import NUMERIC_COLUMNS


def detect_drift(
    baseline_profile: dict[str, dict[str, float]],
    current_features: pd.DataFrame,
    threshold: float = 0.2,
) -> dict[str, object]:
    """Compare current feature distributions against training baseline."""

    drifted_features: list[str] = []
    distances: list[float] = []
    for column in NUMERIC_COLUMNS:
        baseline = baseline_profile[column]
        std = max(float(baseline["std"]), 0.01)
        distance = abs(float(current_features[column].mean()) - float(baseline["mean"])) / std
        distances.append(distance)
        if distance > threshold:
            drifted_features.append(column)

    drift_score = round(float(sum(distances) / len(distances)), 4)
    return {
        "drift_score": drift_score,
        "drifted_features": drifted_features,
        "threshold": threshold,
        "retraining_triggered": bool(drifted_features),
    }


def feature_profile(feature_frame: pd.DataFrame) -> dict[str, dict[str, float]]:
    return {
        column: {
            "mean": round(float(feature_frame[column].mean()), 6),
            "std": round(float(feature_frame[column].std(ddof=0)), 6),
        }
        for column in NUMERIC_COLUMNS
    }
