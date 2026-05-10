from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from ml.model_registry import ModelRegistry
from ml.model_training import train_demand_classifier
from ml.prediction_engine import PredictionEngine


class MLPredictionTests(unittest.TestCase):
    def test_prediction_engine_reports_source(self) -> None:
        frame = pd.DataFrame(
            {
                "likes": [5, 12, 18, 25, 120, 150, 160, 170, 240, 260, 280, 300],
                "comments": [1, 2, 3, 4, 20, 24, 26, 28, 50, 55, 58, 62],
                "shares": [0, 1, 1, 2, 15, 16, 18, 19, 30, 32, 35, 38],
                "searches": [5, 8, 12, 15, 100, 120, 130, 145, 220, 240, 255, 270],
                "views": [200, 210, 230, 250, 600, 650, 680, 710, 900, 920, 950, 980],
                "demand_class": ["Low"] * 4 + ["Moderate"] * 4 + ["High"] * 4,
            }
        )
        scratch = Path("tests") / "_scratch" / "ml_prediction"
        scratch.mkdir(parents=True, exist_ok=True)
        result = train_demand_classifier(
            frame,
            output_dir=scratch,
            registry=ModelRegistry(scratch / "registry.json"),
            model_name="signal_demand_classifier_ml_prediction",
        )
        prediction = PredictionEngine(
            result["model_path"],
            feature_columns=result["feature_columns"],
        ).predict(frame.head(2))
        fallback = PredictionEngine(model_path=scratch / "missing.joblib").predict(frame.head(2))

        self.assertEqual(prediction["prediction_source"], "trained ML model")
        self.assertTrue(prediction["model_loaded"])
        self.assertEqual(len(prediction["predictions"]), 2)
        self.assertEqual(fallback["prediction_source"], "fallback rule")
        self.assertFalse(fallback["model_loaded"])


if __name__ == "__main__":
    unittest.main()
