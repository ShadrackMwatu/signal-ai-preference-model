import unittest
from pathlib import Path

from app import signal_model
from api.app import predict_demand
from src.models.signal_demand_model import (
    DEMAND_CLASSES,
    MODEL_PATH,
    TRAINING_DATA_PATH,
    generate_training_dataset,
    predict_signal_demand,
    train_signal_model,
)


class SignalDemandModelTests(unittest.TestCase):
    def test_training_dataset_generator_creates_required_columns(self) -> None:
        frame = generate_training_dataset("tests/_scratch/signal_training_dataset.csv")

        self.assertIn("likes", frame.columns)
        self.assertIn("comments", frame.columns)
        self.assertIn("shares", frame.columns)
        self.assertIn("searches", frame.columns)
        self.assertIn("engagement_intensity", frame.columns)
        self.assertIn("purchase_intent_score", frame.columns)
        self.assertIn("trend_growth", frame.columns)
        self.assertIn("demand_class", frame.columns)
        self.assertEqual(set(frame["demand_class"]), set(DEMAND_CLASSES))

    def test_train_saves_joblib_model(self) -> None:
        result = train_signal_model(
            data_path="tests/_scratch/signal_training_dataset.csv",
            model_path="tests/_scratch/signal_demand_classifier.joblib",
        )

        self.assertTrue(Path(result["model_path"]).exists())
        self.assertGreaterEqual(result["accuracy"], 0.7)

    def test_predict_returns_class_and_probability_score(self) -> None:
        prediction = predict_signal_demand(
            {
                "likes": 180,
                "comments": 50,
                "shares": 35,
                "searches": 220,
                "engagement_intensity": 0.68,
                "purchase_intent_score": 0.82,
                "trend_growth": 0.6,
            }
        )

        self.assertIn(prediction["demand_class"], DEMAND_CLASSES)
        self.assertGreaterEqual(prediction["score"], 0)
        self.assertLessEqual(prediction["score"], 1)
        self.assertTrue(Path(MODEL_PATH).exists())
        self.assertTrue(Path(TRAINING_DATA_PATH).exists())

    def test_root_app_signal_model_wrapper(self) -> None:
        demand_class, score = signal_model(180, 50, 35, 220, 0.68, 0.82, 0.6)

        self.assertIn(demand_class, DEMAND_CLASSES)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_api_single_prediction_path(self) -> None:
        prediction = predict_demand(180, 50, 35, 220, 0.68, 0.82, 0.6)

        self.assertIn(prediction["demand_class"], DEMAND_CLASSES)
        self.assertGreaterEqual(prediction["score"], 0)
        self.assertLessEqual(prediction["score"], 1)


if __name__ == "__main__":
    unittest.main()
