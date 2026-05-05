"""Prediction interface with safe fallback behavior for Signal ML models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from .feature_engineering import build_behavioral_features, select_numeric_features


class PredictionEngine:
    """Load trained models and produce source-aware predictions."""

    def __init__(self, model_path: str | Path | None = None, feature_columns: list[str] | None = None) -> None:
        self.model_path = Path(model_path) if model_path else None
        self.feature_columns = feature_columns
        self.model = self._load_model()

    def predict(self, frame: pd.DataFrame) -> dict[str, Any]:
        features = build_behavioral_features(frame)
        columns = self.feature_columns or select_numeric_features(features)
        if self.model is None:
            return {
                "predictions": _fallback_demand_class(features[columns]),
                "prediction_source": "fallback rule",
                "model_loaded": False,
            }
        predictions = self.model.predict(features[columns])
        response: dict[str, Any] = {
            "predictions": [str(value) for value in predictions],
            "prediction_source": "trained ML model",
            "model_loaded": True,
        }
        if hasattr(self.model, "predict_proba"):
            response["confidence"] = [float(row.max()) for row in self.model.predict_proba(features[columns])]
        return response

    def _load_model(self) -> Any | None:
        if self.model_path is None or not self.model_path.exists():
            return None
        return joblib.load(self.model_path)


def _fallback_demand_class(feature_frame: pd.DataFrame) -> list[str]:
    signal_strength = feature_frame.mean(axis=1)
    low = float(signal_strength.quantile(0.33))
    high = float(signal_strength.quantile(0.66))
    labels = []
    for value in signal_strength:
        if value >= high:
            labels.append("High")
        elif value <= low:
            labels.append("Low")
        else:
            labels.append("Moderate")
    return labels
