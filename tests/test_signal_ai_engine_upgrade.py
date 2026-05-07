from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

import joblib
import pandas as pd

import app
from adaptive_learning import aggregate_feedback_for_retraining, record_feedback
from train_model import generate_training_data, train_signal_model


class SignalAIMLEngineUpgradeTests(unittest.TestCase):
    def test_training_script_creates_model_and_metadata(self) -> None:
        scratch = Path("tests") / "_scratch" / "signal_ai_engine"
        scratch.mkdir(parents=True, exist_ok=True)
        data_path = scratch / "signal_training_data.csv"
        model_path = scratch / "model.pkl"
        metadata_path = scratch / "metadata.json"

        generate_training_data(data_path, n_rows=240, random_state=7)
        result = train_signal_model(data_path=data_path, model_path=model_path, metadata_path=metadata_path)

        self.assertTrue(model_path.exists())
        self.assertTrue(metadata_path.exists())
        artifact = joblib.load(model_path)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.assertIn("model", artifact)
        self.assertIn("feature_columns", artifact)
        self.assertGreater(result.accuracy_score, 0.7)
        self.assertIn("accuracy_score", metadata)

    def test_predict_demand_returns_expected_tuple_structure(self) -> None:
        result = app.predict_demand(180, 50, 35, 220, 0.68, 0.82, 0.6)

        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], float)
        self.assertIsInstance(result[2], float)

    def test_fallback_works_when_model_missing(self) -> None:
        with patch.object(app, "PRIMARY_MODEL_PATH", Path("tests/_tmp/missing_model.pkl")), patch.object(
            app, "LEGACY_MODEL_PATH", Path("tests/_tmp/missing_legacy.pkl")
        ):
            details = app.predict_demand_details(40, 6, 3, 70, 0.44, 0.41, 0.2)

        self.assertIn("fallback model", details["prediction_source"])
        self.assertIn(details["demand_classification"], {"Low Demand", "Moderate Demand", "High Demand"})

    def test_guardrails_flag_low_demand_high_opportunity_contradiction(self) -> None:
        guarded = app._apply_guardrails(  # noqa: SLF001 - targeted test for guardrail behavior.
            {
                "demand_classification": "Low Demand",
                "confidence_score": 0.61,
                "aggregate_demand_score": 32.0,
                "opportunity_score": 74.0,
                "unmet_demand_probability": 0.45,
                "emerging_trend_probability": 0.41,
                "prediction_source": "trained model",
                "explanation_note": "Primary prediction produced by the trained local Signal model.",
            },
            {
                "unmet_need_signal": 0.82,
                "noise_score": 0.22,
            },
        )

        self.assertEqual(guarded["investment_opportunity_interpretation"], "Investigate Anomaly / Possible Unmet Demand")
        self.assertTrue(guarded["unmet_demand_flag"])

    def test_feedback_log_remains_aggregate_and_blocks_individual_fields(self) -> None:
        scratch = Path("tests") / "_scratch" / "signal_ai_feedback"
        scratch.mkdir(parents=True, exist_ok=True)
        feedback_path = scratch / "feedback_log.csv"
        row = record_feedback(
            {
                "county": "Nairobi",
                "topic": "retail",
                "time_period": "2026-Q2",
                "prediction_source": "trained model",
                "predicted_demand_classification": "High Demand",
                "observed_demand_classification": "Moderate Demand",
                "opportunity_score": 71.0,
                "confidence_score": 0.86,
                "username": "should_not_store",
                "email": "blocked@example.com",
            },
            path=feedback_path,
        )
        aggregated = aggregate_feedback_for_retraining(feedback_path)

        self.assertNotIn("username", row)
        self.assertNotIn("email", row)
        self.assertEqual(len(aggregated), 1)
        self.assertIn("feedback_count", aggregated.columns)


if __name__ == "__main__":
    unittest.main()
