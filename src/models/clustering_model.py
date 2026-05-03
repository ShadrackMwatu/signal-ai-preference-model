"""KMeans clustering for anonymized consumer and county preference patterns."""

from __future__ import annotations

import os

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.features.aggregation import aggregate_features
from src.features.feature_engineering import FEATURE_COLUMNS


class SegmentClusterer:
    """Cluster aggregate feature rows without individual-level data."""

    def __init__(self, n_clusters: int = 4, random_state: int = 42) -> None:
        self.pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)),
            ]
        )
        self.is_trained = False

    def fit(self, feature_frame: pd.DataFrame) -> "SegmentClusterer":
        aggregated = aggregate_features(feature_frame)
        self.pipeline.fit(aggregated[FEATURE_COLUMNS])
        self.is_trained = True
        return self

    def predict(self, feature_frame: pd.DataFrame) -> pd.DataFrame:
        if not self.is_trained:
            raise RuntimeError("SegmentClusterer must be fitted before predict")
        aggregated = aggregate_features(feature_frame)
        clustered = aggregated[["country", "county", "category", "consumer_segment", "time_period"]].copy()
        clustered["segment_cluster"] = self.pipeline.predict(aggregated[FEATURE_COLUMNS])
        return clustered
