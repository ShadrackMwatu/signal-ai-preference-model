"""Aggregate feature tables without exposing individual-level records."""

from __future__ import annotations

import pandas as pd

from src.data_pipeline.privacy_filter import MIN_GROUP_SIZE, aggregate_only_columns


AGGREGATION_KEYS = ["country", "county", "category", "consumer_segment", "time_period"]


def aggregate_features(feature_frame: pd.DataFrame, min_group_size: int = MIN_GROUP_SIZE) -> pd.DataFrame:
    """Aggregate features by country/county/category/segment/time period."""

    safe = feature_frame[feature_frame["observation_count"] >= min_group_size].copy()
    numeric_columns = [
        column
        for column in safe.select_dtypes(include="number").columns
        if column != "observation_count"
    ]
    categorical_columns = [
        column
        for column in [
            "demand_classification",
            "trend_direction",
            "nlp_topic",
            "topic_keywords",
        ]
        if column in safe.columns
    ]
    aggregated = safe.groupby(AGGREGATION_KEYS, as_index=False).agg(
        {
            **{column: "mean" for column in numeric_columns},
            **{column: _mode for column in categorical_columns},
            "observation_count": "sum",
        }
    )
    return aggregate_only_columns(aggregated)


def _mode(values: pd.Series):
    modes = values.mode()
    return modes.iloc[0] if not modes.empty else values.iloc[0]
