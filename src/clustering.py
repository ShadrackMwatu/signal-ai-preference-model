"""Consumer segment and county-pattern clustering."""

from __future__ import annotations

import os

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .features import FEATURE_COLUMNS


class CountySegmentClusterer:
    """Cluster anonymized aggregate rows into demand segments."""

    def __init__(self, segment_clusters: int = 4, county_clusters: int = 3, random_state: int = 42) -> None:
        self.segment_clusters = segment_clusters
        self.county_clusters = county_clusters
        self.random_state = random_state
        self.segment_pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("cluster", KMeans(n_clusters=segment_clusters, random_state=random_state, n_init=10)),
            ]
        )
        self.county_pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("cluster", KMeans(n_clusters=county_clusters, random_state=random_state, n_init=10)),
            ]
        )
        self.is_trained = False

    def fit(self, features: pd.DataFrame) -> "CountySegmentClusterer":
        self.segment_pipeline.fit(features[FEATURE_COLUMNS])
        county_features = _county_feature_frame(features)
        self.county_pipeline.fit(county_features[FEATURE_COLUMNS])
        self.county_cluster_map = dict(
            zip(
                county_features["county"],
                self.county_pipeline.predict(county_features[FEATURE_COLUMNS]),
                strict=True,
            )
        )
        self.is_trained = True
        return self

    def transform(self, features: pd.DataFrame) -> pd.DataFrame:
        if not self.is_trained:
            raise RuntimeError("CountySegmentClusterer must be fitted before transform")

        clustered = features.copy()
        clustered["segment_cluster"] = self.segment_pipeline.predict(features[FEATURE_COLUMNS])
        clustered["county_pattern_cluster"] = clustered["county"].map(self.county_cluster_map).fillna(-1).astype(int)
        return clustered

    def fit_transform(self, features: pd.DataFrame) -> pd.DataFrame:
        return self.fit(features).transform(features)

    def summarize_county_patterns(self, features: pd.DataFrame) -> list[dict[str, int | str]]:
        clustered = self.transform(features)
        rows = clustered[["county", "county_pattern_cluster"]].drop_duplicates()
        return [
            {"county": row["county"], "county_pattern_cluster": int(row["county_pattern_cluster"])}
            for _, row in rows.sort_values("county").iterrows()
        ]


def _county_feature_frame(features: pd.DataFrame) -> pd.DataFrame:
    return features.groupby("county", as_index=False)[FEATURE_COLUMNS].mean()
