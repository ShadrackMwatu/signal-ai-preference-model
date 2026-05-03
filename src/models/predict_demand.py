"""Load trained models and generate aggregate demand predictions."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from src.features.feature_engineering import build_feature_table
from src.intelligence.competitor_analysis import analyze_competitor_gaps
from src.intelligence.market_access import generate_market_access
from src.intelligence.opportunity_engine import generate_opportunities
from src.intelligence.recommendations import generate_recommendations
from src.models.train_demand_model import CATEGORICAL_COLUMNS, MODEL_PATH, NUMERIC_COLUMNS, DemandModelBundle


class DemandPredictor:
    """Prediction interface for trained demand model bundles."""

    def __init__(self, bundle: DemandModelBundle) -> None:
        self.bundle = bundle

    def predict(self, raw_frame: pd.DataFrame, competitors: pd.DataFrame | None = None) -> pd.DataFrame:
        features = build_feature_table(raw_frame)
        inputs = features[CATEGORICAL_COLUMNS + NUMERIC_COLUMNS]
        output = features[["country", "county", "category", "consumer_segment", "time_period"]].copy()
        output["behavioral_signal_score"] = features["behavioral_signal_score"].round(4)
        output["demand_classification"] = self.bundle.demand_classifier.predict(inputs)
        output["aggregate_demand_score"] = self.bundle.aggregate_regressor.predict(inputs).clip(0, 1).round(4)
        output["opportunity_score"] = self.bundle.opportunity_regressor.predict(inputs).clip(0, 1).round(4)
        output["emerging_trend_probability"] = _positive_probability(self.bundle.emerging_classifier, inputs)
        output["unmet_demand_probability"] = _positive_probability(self.bundle.unmet_classifier, inputs)
        output["trend_direction"] = features.get("trend_direction", "stable")
        output["demand_forecast"] = (
            output["aggregate_demand_score"] * (1 + output["emerging_trend_probability"] * 0.2)
        ).clip(0, 1).round(4)

        output = generate_opportunities(output)
        if competitors is not None:
            output = analyze_competitor_gaps(output, competitors)
        output = generate_market_access(output)
        output = generate_recommendations(output)
        return output


def load_model_bundle(path: str | Path = MODEL_PATH) -> DemandModelBundle:
    return joblib.load(path)


def predict_from_saved_model(raw_frame: pd.DataFrame, model_path: str | Path = MODEL_PATH) -> pd.DataFrame:
    return DemandPredictor(load_model_bundle(model_path)).predict(raw_frame)


def _positive_probability(pipeline, inputs: pd.DataFrame) -> pd.Series:
    classes = list(pipeline.named_steps["model"].classes_)
    probabilities = pipeline.predict_proba(inputs)
    class_index = classes.index(1) if 1 in classes else 0
    return pd.Series(probabilities[:, class_index]).clip(0, 1).round(4)
