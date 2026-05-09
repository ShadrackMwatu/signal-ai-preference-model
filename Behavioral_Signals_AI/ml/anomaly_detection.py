"""Anomaly detection for unusual Signal demand patterns."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import IsolationForest

from .feature_engineering import build_behavioral_features, select_numeric_features


class SignalAnomalyDetector:
    """IsolationForest wrapper for aggregate county/topic/household anomalies."""

    def __init__(self, contamination: float = 0.1, random_state: int = 42) -> None:
        self.model = IsolationForest(contamination=contamination, random_state=random_state)
        self.feature_columns: list[str] = []
        self.is_fitted = False

    def fit(self, frame: pd.DataFrame, feature_columns: list[str] | None = None) -> "SignalAnomalyDetector":
        features = build_behavioral_features(frame)
        self.feature_columns = feature_columns or select_numeric_features(features)
        self.model.fit(features[self.feature_columns])
        self.is_fitted = True
        return self

    def detect(self, frame: pd.DataFrame) -> pd.DataFrame:
        if not self.is_fitted:
            raise RuntimeError("SignalAnomalyDetector must be fitted before detect")
        features = build_behavioral_features(frame)
        output = frame.copy()
        output["anomaly_label"] = self.model.predict(features[self.feature_columns])
        output["is_anomaly"] = output["anomaly_label"] == -1
        output["anomaly_score"] = self.model.decision_function(features[self.feature_columns])
        output["prediction_source"] = "anomaly detection"
        return output


def detect_anomalies(frame: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
    """Fit and run IsolationForest in one call."""

    detector = SignalAnomalyDetector(**kwargs).fit(frame)
    return detector.detect(frame)
