"""Feature extraction for privacy-preserving demand intelligence."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .data_pipeline import BEHAVIOR_COLUMNS, validate_behavioral_schema, validate_privacy
from .nlp import SignalNLPModel


FEATURE_COLUMNS = [
    "engagement_intensity",
    "sentiment_score",
    "purchase_intent_score",
    "repetition_score",
    "trend_growth",
    "location_relevance",
    "urgency_score",
    "price_sensitivity",
    "noise_score",
]


class BehavioralFeatureExtractor:
    """Fit NLP components and transform aggregate behavioral data into ML features."""

    def __init__(self, nlp_model: SignalNLPModel | None = None) -> None:
        self.nlp_model = nlp_model or SignalNLPModel()
        self.is_trained = False

    def fit(self, frame: pd.DataFrame) -> "BehavioralFeatureExtractor":
        validate_behavioral_schema(frame)
        validate_privacy(frame)
        self.nlp_model.fit(frame)
        self.is_trained = True
        return self

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        if not self.is_trained:
            raise RuntimeError("BehavioralFeatureExtractor must be fitted before transform")

        validate_behavioral_schema(frame)
        validate_privacy(frame)
        working = frame.copy().reset_index(drop=True)
        nlp_features = self.nlp_model.transform(working["text"]).reset_index(drop=True)

        engagement = (
            working["clicks"]
            + working["likes"]
            + working["comments"]
            + working["shares"]
            + working["saves"]
            + working["searches"]
            + working["hashtags"]
            + working["mentions"]
        )
        active_need = working["purchase_intent_phrases"] + working["complaints"] + working["delayed_responses"]
        response_base = working["comments"] + working["shares"] + working["saves"] + 1

        features = working[["county", "category", "time_period", "anonymized_segment", "segment_size"]].copy()
        features["country"] = working["country"]
        features["engagement_intensity"] = np.log1p(engagement) / np.log1p(working["views"] + working["segment_size"])
        features["repetition_score"] = working["repeated_engagement"] / (working["clicks"] + 1)
        features["trend_growth"] = _trend_growth(working, engagement)
        features["location_relevance"] = _location_relevance(working, engagement)
        features["price_sensitivity"] = (
            working["complaints"] + working["ignored_content"] + working["delayed_responses"]
        ) / (active_need + response_base)
        features["noise_score"] = (working["ignored_content"] + working["delayed_responses"]) / (
            working["views"] + working["comments"] + 1
        )

        features = pd.concat([features, nlp_features], axis=1)
        for column in FEATURE_COLUMNS:
            features[column] = features[column].replace([np.inf, -np.inf], 0).fillna(0).clip(lower=0)
        features["dissatisfaction_score"] = (
            features["dissatisfaction_score"].replace([np.inf, -np.inf], 0).fillna(0).clip(lower=0, upper=1)
        )

        return features

    def fit_transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        return self.fit(frame).transform(frame)


def _trend_growth(frame: pd.DataFrame, engagement: pd.Series) -> pd.Series:
    working = frame[["county", "category", "time_period"]].copy()
    working["engagement"] = engagement
    working["time_order"] = working["time_period"].map(_time_order)
    working = working.sort_values(["county", "category", "time_order"])
    previous = working.groupby(["county", "category"])["engagement"].shift(1)
    growth = ((working["engagement"] - previous) / previous.replace(0, np.nan)).fillna(0)
    return growth.reindex(frame.index).fillna(0).clip(lower=0)


def _location_relevance(frame: pd.DataFrame, engagement: pd.Series) -> pd.Series:
    working = frame[["county", "category"]].copy()
    working["engagement"] = engagement
    county_total = working.groupby("county")["engagement"].transform("sum").replace(0, np.nan)
    county_category = working.groupby(["county", "category"])["engagement"].transform("sum")
    return (county_category / county_total).fillna(0)


def _time_order(value: str) -> int:
    year, quarter = str(value).split("-Q", maxsplit=1)
    return (int(year) * 4) + int(quarter)
