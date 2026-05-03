"""End-to-end adaptive ML models for Signal revealed demand intelligence."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .clustering import CountySegmentClusterer
from .data_pipeline import load_behavioral_data, validate_privacy
from .evaluation import detect_feature_drift, feature_profile
from .features import FEATURE_COLUMNS, BehavioralFeatureExtractor


CLASSIFIER_TARGETS = {
    "demand_classification": "demand_classification",
    "trend_direction": "trend_direction_label",
    "recommended_value_proposition": "value_proposition_label",
    "product_service_opportunity": "product_service_label",
    "revenue_model": "revenue_model_label",
    "supplier_recommendation": "supplier_recommendation_label",
    "logistics_recommendation": "logistics_recommendation_label",
    "payment_recommendation": "payment_recommendation_label",
    "competitor_gap": "competitor_gap_label",
    "customer_dissatisfaction_signal": "customer_dissatisfaction_label",
}

REGRESSION_TARGETS = {
    "behavioral_signal_score": "behavioral_signal_score_target",
    "aggregate_demand_score": "aggregate_demand_score_target",
    "opportunity_score": "opportunity_score_target",
    "emerging_trend_probability": "emerging_trend_target",
    "unmet_demand_probability": "unmet_demand_target",
    "market_gap": "market_gap_target",
    "pricing_power": "pricing_power_target",
    "customer_reach": "customer_reach_target",
    "inventory_planning": "inventory_planning_target",
    "sales_forecasting": "sales_forecast_target",
}

CATEGORICAL_MODEL_COLUMNS = ["county", "category", "time_period", "nlp_topic", "anonymized_segment"]
NUMERIC_MODEL_COLUMNS = FEATURE_COLUMNS + ["topic_confidence", "segment_cluster", "county_pattern_cluster"]


@dataclass
class AdaptiveLearningLog:
    """Summary of an adaptive learning cycle."""

    drift_score: float
    drifted_features: list[str]
    retraining_triggered: bool
    records_used: int


class SignalDemandIntelligenceSystem:
    """Market intelligence system trained end to end from anonymized behavioral data."""

    def __init__(self, random_state: int = 42) -> None:
        self.random_state = random_state
        self.feature_extractor = BehavioralFeatureExtractor()
        self.clusterer = CountySegmentClusterer(random_state=random_state)
        self.classifiers: dict[str, Pipeline] = {}
        self.regressors: dict[str, Pipeline] = {}
        self.baseline_profile: dict[str, dict[str, float]] | None = None
        self.training_data: pd.DataFrame | None = None
        self.is_trained = False

    def fit(self, frame: pd.DataFrame) -> "SignalDemandIntelligenceSystem":
        validate_privacy(frame)
        features = self.feature_extractor.fit_transform(frame)
        model_frame = self.clusterer.fit_transform(features)
        self._fit_estimators(model_frame, frame)
        self.baseline_profile = feature_profile(model_frame)
        self.training_data = frame.copy()
        self.is_trained = True
        return self

    def predict(self, frame: pd.DataFrame) -> dict[str, object]:
        if not self.is_trained:
            raise RuntimeError("SignalDemandIntelligenceSystem must be fitted before predict")

        validate_privacy(frame)
        features = self.feature_extractor.transform(frame)
        model_frame = self.clusterer.transform(features)
        predictions = self._predict_records(model_frame)
        records = _attach_context(frame, predictions)
        return {
            "records": records,
            "dashboard": build_market_dashboard(records),
            "county_patterns": self.clusterer.summarize_county_patterns(features),
        }

    def detect_drift(self, frame: pd.DataFrame, threshold: float = 0.15) -> dict[str, object]:
        if self.baseline_profile is None:
            raise RuntimeError("System must be fitted before drift detection")

        features = self.feature_extractor.transform(frame)
        return detect_feature_drift(self.baseline_profile, features, threshold=threshold)

    def retrain_if_needed(
        self,
        new_frame: pd.DataFrame,
        *,
        drift_threshold: float = 0.15,
        force: bool = False,
    ) -> AdaptiveLearningLog:
        drift = self.detect_drift(new_frame, threshold=drift_threshold)
        should_retrain = force or bool(drift["retraining_recommended"])
        records_used = len(new_frame)
        if should_retrain:
            base = self.training_data if self.training_data is not None else pd.DataFrame()
            combined = pd.concat([base, new_frame], ignore_index=True)
            self.fit(combined)
            records_used = len(combined)

        return AdaptiveLearningLog(
            drift_score=float(drift["drift_score"]),
            drifted_features=list(drift["drifted_features"]),
            retraining_triggered=should_retrain,
            records_used=records_used,
        )

    def save(self, path: str | Path) -> None:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, output_path)

    @classmethod
    def load(cls, path: str | Path) -> "SignalDemandIntelligenceSystem":
        return joblib.load(path)

    def _fit_estimators(self, model_frame: pd.DataFrame, labels: pd.DataFrame) -> None:
        inputs = model_frame[CATEGORICAL_MODEL_COLUMNS + NUMERIC_MODEL_COLUMNS]
        for output_name, target_column in CLASSIFIER_TARGETS.items():
            pipeline = _classifier_pipeline(self.random_state)
            pipeline.fit(inputs, labels[target_column])
            self.classifiers[output_name] = pipeline

        for output_name, target_column in REGRESSION_TARGETS.items():
            pipeline = _regressor_pipeline(self.random_state)
            pipeline.fit(inputs, labels[target_column])
            self.regressors[output_name] = pipeline

    def _predict_records(self, model_frame: pd.DataFrame) -> pd.DataFrame:
        inputs = model_frame[CATEGORICAL_MODEL_COLUMNS + NUMERIC_MODEL_COLUMNS]
        output = pd.DataFrame(index=model_frame.index)
        for output_name, pipeline in self.classifiers.items():
            output[output_name] = pipeline.predict(inputs)
        for output_name, pipeline in self.regressors.items():
            output[output_name] = pipeline.predict(inputs).clip(0, 1).round(4)
        return output


def train_default_system(path: str | Path | None = None) -> SignalDemandIntelligenceSystem:
    """Train a system from the default behavioral dataset."""

    frame = load_behavioral_data(path) if path else load_behavioral_data()
    return SignalDemandIntelligenceSystem().fit(frame)


def build_market_dashboard(records: list[dict[str, object]]) -> dict[str, object]:
    """Build dashboard-ready aggregate market intelligence outputs."""

    frame = pd.DataFrame(records)
    county_index = _index_records(frame, "county", "aggregate_demand_score", "county_demand_index")
    category_index = _index_records(frame, "category", "aggregate_demand_score", "category_preference_index")
    forecast = (
        frame.groupby(["time_period", "category"], as_index=False)["sales_forecasting"].mean().round(4)
        .rename(columns={"sales_forecasting": "demand_forecast"})
        .to_dict(orient="records")
    )
    opportunities = (
        frame.sort_values("opportunity_score", ascending=False)
        .head(10)[
            [
                "county",
                "category",
                "opportunity_score",
                "demand_classification",
                "recommended_value_proposition",
                "product_service_opportunity",
                "revenue_model",
                "supplier_recommendation",
                "logistics_recommendation",
                "payment_recommendation",
            ]
        ]
        .to_dict(orient="records")
    )
    unmet = (
        frame.groupby("county", as_index=False)["unmet_demand_probability"].mean().round(4)
        .sort_values("unmet_demand_probability", ascending=False)
        .to_dict(orient="records")
    )
    competitor = (
        frame.groupby(["category", "competitor_gap"], as_index=False)["market_gap"].mean().round(4)
        .sort_values("market_gap", ascending=False)
        .head(10)
        .rename(columns={"market_gap": "gap_strength"})
        .to_dict(orient="records")
    )

    return {
        "national_aggregate_demand_index": round(float(frame["aggregate_demand_score"].mean()), 4),
        "county_demand_index": county_index,
        "category_preference_index": category_index,
        "demand_forecast": forecast,
        "trend_direction": _mode(frame["trend_direction"]),
        "market_opportunities": opportunities,
        "competitor_analysis": {
            "gaps": competitor,
            "customer_dissatisfaction_signals": _index_records(
                frame,
                "customer_dissatisfaction_signal",
                "unmet_demand_probability",
                "signal_strength",
            ),
        },
        "unserved_counties": unmet,
        "planning": {
            "pricing_power": round(float(frame["pricing_power"].mean()), 4),
            "customer_reach": round(float(frame["customer_reach"].mean()), 4),
            "inventory_planning": round(float(frame["inventory_planning"].mean()), 4),
            "sales_forecasting": round(float(frame["sales_forecasting"].mean()), 4),
        },
    }


def _model_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_MODEL_COLUMNS),
            ("numeric", StandardScaler(), NUMERIC_MODEL_COLUMNS),
        ]
    )


def _classifier_pipeline(random_state: int) -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", _model_preprocessor()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=35,
                    min_samples_leaf=2,
                    random_state=random_state,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def _regressor_pipeline(random_state: int) -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", _model_preprocessor()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=40,
                    min_samples_leaf=2,
                    random_state=random_state,
                ),
            ),
        ]
    )


def _attach_context(frame: pd.DataFrame, predictions: pd.DataFrame) -> list[dict[str, object]]:
    context = frame[["county", "category", "time_period", "anonymized_segment"]].reset_index(drop=True)
    combined = pd.concat([context, predictions.reset_index(drop=True)], axis=1)
    return combined.to_dict(orient="records")


def _index_records(frame: pd.DataFrame, group_column: str, value_column: str, output_name: str) -> list[dict[str, object]]:
    return (
        frame.groupby(group_column, as_index=False)[value_column].mean().round(4)
        .rename(columns={value_column: output_name})
        .sort_values(output_name, ascending=False)
        .to_dict(orient="records")
    )


def _mode(values: pd.Series) -> object:
    modes = values.mode()
    return modes.iloc[0] if not modes.empty else None
