"""Behavioral feature engineering for demand models."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .text_features import TextFeatureExtractor


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
    "complaint_score",
    "topic_confidence",
]

TARGET_COLUMNS = [
    "demand_classification",
    "aggregate_demand_score",
    "opportunity_score",
    "emerging_trend_probability",
    "unmet_demand_probability",
    "market_gap",
    "supply_shortage",
    "scalability",
    "competition_intensity",
    "trend_direction",
]


def build_feature_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert raw aggregate behavioral actions into model-ready features."""

    working = frame.copy().reset_index(drop=True)
    text_features = TextFeatureExtractor().transform(working["text"]).reset_index(drop=True)
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

    features = working[
        ["country", "county", "category", "consumer_segment", "time_period", "observation_count"]
    ].copy()
    features["engagement_intensity"] = np.log1p(engagement) / np.log1p(working["views"] + working["observation_count"])
    features["repetition_score"] = working["repeated_engagement"] / (working["clicks"] + 1)
    features["trend_growth"] = _trend_growth(working, engagement)
    features["location_relevance"] = _location_relevance(working, engagement)
    features["price_sensitivity"] = (
        working["complaints"] + working["ignored_content"] + working["delayed_responses"]
    ) / (active_need + response_base)
    features["noise_score"] = (working["ignored_content"] + working["delayed_responses"]) / (
        working["views"] + working["comments"] + 1
    )
    features["behavioral_signal_score"] = (
        features["engagement_intensity"] * 0.45
        + features["repetition_score"].clip(upper=1) * 0.25
        + (working["purchase_intent_phrases"] / (working["searches"] + 1)).clip(upper=1) * 0.3
    ).round(4)

    features = pd.concat([features, text_features], axis=1)
    for column in FEATURE_COLUMNS + ["behavioral_signal_score"]:
        features[column] = features[column].replace([np.inf, -np.inf], 0).fillna(0).clip(lower=0, upper=1)

    for column in TARGET_COLUMNS:
        if column in working.columns:
            features[column] = working[column]

    return features


def _trend_growth(frame: pd.DataFrame, engagement: pd.Series) -> pd.Series:
    ordered = frame[["county", "category", "time_period"]].copy()
    ordered["engagement"] = engagement
    ordered["time_order"] = ordered["time_period"].map(_time_order)
    ordered = ordered.sort_values(["county", "category", "time_order"])
    previous = ordered.groupby(["county", "category"])["engagement"].shift(1)
    growth = ((ordered["engagement"] - previous) / previous.replace(0, np.nan)).fillna(0)
    return growth.reindex(frame.index).fillna(0).clip(lower=0, upper=1)


def _location_relevance(frame: pd.DataFrame, engagement: pd.Series) -> pd.Series:
    grouped = frame[["county", "category"]].copy()
    grouped["engagement"] = engagement
    county_total = grouped.groupby("county")["engagement"].transform("sum").replace(0, np.nan)
    county_category = grouped.groupby(["county", "category"])["engagement"].transform("sum")
    return (county_category / county_total).fillna(0).clip(lower=0, upper=1)


def _time_order(value: str) -> int:
    year, quarter = str(value).split("-Q", maxsplit=1)
    return (int(year) * 4) + int(quarter)
