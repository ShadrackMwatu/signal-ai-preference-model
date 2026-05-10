"""Feature engineering for Signal ML extensions."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


BASE_SIGNAL_COLUMNS = ["likes", "comments", "shares", "searches"]
OPTIONAL_SIGNAL_COLUMNS = ["clicks", "views", "saves", "complaints", "purchase_intent_phrases"]
ENGINEERED_FEATURE_COLUMNS = [
    "engagement_intensity",
    "purchase_intent_score",
    "trend_growth",
    "complaint_rate",
]


def build_behavioral_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create stable numeric features for demand, regression, and anomaly models."""

    features = frame.copy()
    for column in BASE_SIGNAL_COLUMNS + OPTIONAL_SIGNAL_COLUMNS:
        if column not in features.columns:
            features[column] = 0
        features[column] = pd.to_numeric(features[column], errors="coerce").fillna(0)

    engagement = features["likes"] + features["comments"] + features["shares"] + features["searches"]
    views = features["views"].replace(0, np.nan)
    if "engagement_intensity" not in features.columns:
        features["engagement_intensity"] = (engagement / views).fillna(
            engagement / engagement.max() if engagement.max() else 0
        )
    if "purchase_intent_score" not in features.columns:
        features["purchase_intent_score"] = (
            (features["searches"] + features["purchase_intent_phrases"]) / (engagement + 1)
        )
    if "trend_growth" not in features.columns:
        features["trend_growth"] = _growth_by_group(features, engagement)
    if "complaint_rate" not in features.columns:
        features["complaint_rate"] = features["complaints"] / (features["comments"] + 1)

    for column in ENGINEERED_FEATURE_COLUMNS:
        features[column] = pd.to_numeric(features[column], errors="coerce").fillna(0).replace([np.inf, -np.inf], 0)
    return features


def select_numeric_features(
    frame: pd.DataFrame,
    preferred_columns: Iterable[str] | None = None,
) -> list[str]:
    """Select numeric feature columns, preferring Signal behavioral features when present."""

    preferred = list(preferred_columns or BASE_SIGNAL_COLUMNS + ENGINEERED_FEATURE_COLUMNS)
    available = [column for column in preferred if column in frame.columns]
    if available:
        return available
    return list(frame.select_dtypes(include="number").columns)


def _growth_by_group(frame: pd.DataFrame, engagement: pd.Series) -> pd.Series:
    if not {"county", "category", "time_period"}.issubset(frame.columns):
        maximum = float(engagement.max() or 1)
        return (engagement / maximum).clip(lower=0, upper=1)

    grouped = frame[["county", "category", "time_period"]].copy()
    grouped["engagement"] = engagement
    grouped["_order"] = grouped["time_period"].map(_time_order)
    ordered = grouped.sort_values(["county", "category", "_order"])
    previous = ordered.groupby(["county", "category"])["engagement"].shift(1)
    growth = ((ordered["engagement"] - previous) / previous.replace(0, np.nan)).fillna(0)
    return growth.reindex(frame.index).fillna(0).clip(lower=0)


def _time_order(value: object) -> int:
    text = str(value)
    if "-Q" in text:
        year, quarter = text.split("-Q", maxsplit=1)
        return int(year) * 4 + int(quarter)
    return 0
