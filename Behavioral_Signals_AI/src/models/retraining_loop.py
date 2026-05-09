"""Adaptive feedback and retraining loop."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.features.feature_engineering import build_feature_table
from src.models.drift_detection import detect_drift
from src.models.predict_demand import DemandPredictor
from src.models.train_demand_model import MODEL_PATH, DemandModelBundle, save_model_bundle, train_demand_models


@dataclass(frozen=True)
class RetrainingDecision:
    drift_score: float
    drifted_features: list[str]
    retraining_triggered: bool
    model_version: int
    records_used: int


class AdaptiveRetrainingLoop:
    """new data -> features -> prediction -> feedback -> drift check -> retraining trigger."""

    def __init__(self, bundle: DemandModelBundle, model_path: str | Path = MODEL_PATH) -> None:
        self.bundle = bundle
        self.model_path = Path(model_path)

    def run(
        self,
        new_behavioral_data: pd.DataFrame,
        feedback_data: pd.DataFrame | None = None,
        threshold: float = 0.2,
        force: bool = False,
    ) -> RetrainingDecision:
        features = build_feature_table(new_behavioral_data)
        _ = DemandPredictor(self.bundle).predict(new_behavioral_data)
        drift = detect_drift(self.bundle.feature_baseline, features, threshold=threshold)
        feedback_trigger = _feedback_trigger(feedback_data)
        should_retrain = force or bool(drift["retraining_triggered"]) or feedback_trigger

        if should_retrain:
            self.bundle = train_demand_models(features, save_path=self.model_path)
            self.bundle.model_version += 1
            self.bundle.retraining_logs.append(
                {
                    "model_version": self.bundle.model_version,
                    "drift_score": drift["drift_score"],
                    "drifted_features": drift["drifted_features"],
                    "feedback_triggered": feedback_trigger,
                    "records_used": len(features),
                }
            )
            save_model_bundle(self.bundle, self.model_path)

        return RetrainingDecision(
            drift_score=float(drift["drift_score"]),
            drifted_features=list(drift["drifted_features"]),
            retraining_triggered=should_retrain,
            model_version=self.bundle.model_version,
            records_used=len(features),
        )


def _feedback_trigger(feedback_data: pd.DataFrame | None) -> bool:
    if feedback_data is None or feedback_data.empty:
        return False
    return bool((feedback_data["observed_complaint_rate"] > 0.14).any())
