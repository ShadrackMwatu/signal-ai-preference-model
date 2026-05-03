"""Train supervised demand intelligence models."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.features.feature_engineering import FEATURE_COLUMNS


MODEL_DIR = Path(__file__).resolve().parents[2] / "models" / "saved_models"
MODEL_PATH = MODEL_DIR / "demand_model_bundle.joblib"
CATEGORICAL_COLUMNS = ["country", "county", "category", "consumer_segment", "time_period", "nlp_topic"]
NUMERIC_COLUMNS = FEATURE_COLUMNS + ["behavioral_signal_score"]
TARGET_LABELS = (
    "High demand",
    "Moderate demand",
    "Low demand",
    "Emerging demand",
    "Declining demand",
    "Unmet demand",
)


@dataclass
class DemandModelBundle:
    """Container for all trained demand models and metadata."""

    demand_classifier: Pipeline
    aggregate_regressor: Pipeline
    opportunity_regressor: Pipeline
    emerging_classifier: Pipeline
    unmet_classifier: Pipeline
    feature_baseline: dict[str, dict[str, float]]
    model_version: int = 1
    training_rows: int = 0
    retraining_logs: list[dict[str, object]] = field(default_factory=list)


def train_demand_models(feature_frame: pd.DataFrame, save_path: str | Path = MODEL_PATH) -> DemandModelBundle:
    """Train the supervised demand model suite and persist it locally."""

    inputs = feature_frame[CATEGORICAL_COLUMNS + NUMERIC_COLUMNS]
    bundle = DemandModelBundle(
        demand_classifier=_demand_classifier().fit(inputs, feature_frame["demand_classification"]),
        aggregate_regressor=_aggregate_regressor().fit(inputs, feature_frame["aggregate_demand_score"]),
        opportunity_regressor=_opportunity_regressor().fit(inputs, feature_frame["opportunity_score"]),
        emerging_classifier=_binary_classifier().fit(
            inputs,
            (feature_frame["emerging_trend_probability"] >= 0.55).astype(int),
        ),
        unmet_classifier=_binary_classifier().fit(
            inputs,
            (feature_frame["unmet_demand_probability"] >= 0.5).astype(int),
        ),
        feature_baseline=_feature_baseline(feature_frame),
        training_rows=len(feature_frame),
    )
    save_model_bundle(bundle, save_path)
    return bundle


def save_model_bundle(bundle: DemandModelBundle, save_path: str | Path = MODEL_PATH) -> None:
    output_path = Path(save_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, output_path)


def _preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
            ("numeric", StandardScaler(), NUMERIC_COLUMNS),
        ]
    )


def _demand_classifier() -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", _preprocessor()),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=55,
                    min_samples_leaf=2,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def _aggregate_regressor() -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", _preprocessor()),
            ("model", RandomForestRegressor(n_estimators=60, min_samples_leaf=2, random_state=42)),
        ]
    )


def _opportunity_regressor() -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", _preprocessor()),
            ("model", GradientBoostingRegressor(random_state=42)),
        ]
    )


def _binary_classifier() -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", _preprocessor()),
            ("model", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )


def _feature_baseline(feature_frame: pd.DataFrame) -> dict[str, dict[str, float]]:
    return {
        column: {
            "mean": round(float(feature_frame[column].mean()), 6),
            "std": round(float(feature_frame[column].std(ddof=0)), 6),
        }
        for column in NUMERIC_COLUMNS
    }
