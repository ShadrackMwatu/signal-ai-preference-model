import unittest

import pandas as pd

from src.data_pipeline.data_loader import load_behavioral_signals
from src.features.aggregation import aggregate_features
from src.features.feature_engineering import build_feature_table
from src.models.drift_detection import detect_drift
from src.models.retraining_loop import AdaptiveRetrainingLoop
from src.models.train_demand_model import train_demand_models


class DriftDetectionTests(unittest.TestCase):
    def test_detects_feature_drift_and_retraining_trigger(self) -> None:
        raw = load_behavioral_signals("Behavioral_Signals_AI/data/sample_behavioral_signals.csv")
        features = aggregate_features(build_feature_table(raw))
        bundle = train_demand_models(features, "tests/_tmp/test_drift_bundle.joblib")
        drifted = raw.copy()
        drifted["clicks"] = drifted["clicks"] * 4
        drifted["searches"] = drifted["searches"] * 3
        drifted_features = aggregate_features(build_feature_table(drifted))
        feedback = pd.read_csv("Behavioral_Signals_AI/data/sample_feedback.csv")

        drift = detect_drift(bundle.feature_baseline, drifted_features, threshold=0.05)
        decision = AdaptiveRetrainingLoop(bundle, "tests/_tmp/test_drift_bundle.joblib").run(
            drifted,
            feedback,
            threshold=0.05,
        )

        self.assertTrue(drift["retraining_triggered"])
        self.assertTrue(decision.retraining_triggered)
        self.assertGreaterEqual(decision.model_version, 2)


if __name__ == "__main__":
    unittest.main()
