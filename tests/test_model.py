import unittest
from pathlib import Path

from src.data import load_examples
from src.model import PreferenceModel
from src.schemas import PreferenceRequest


class ModelTests(unittest.TestCase):
    def test_model_trains_predicts_and_evaluates(self) -> None:
        examples = load_examples(Path("data/sample_preferences.csv"))
        model = PreferenceModel().train(examples)

        prediction = model.predict(
            PreferenceRequest(
                user_id="user_001",
                item_id="dashboard_plus",
                category="analytics",
                price=24.0,
                rating=4.7,
                popularity=0.8,
            )
        )
        metrics = model.evaluate(examples)

        self.assertEqual(prediction.item_id, "dashboard_plus")
        self.assertGreaterEqual(prediction.score, 0)
        self.assertLessEqual(prediction.score, 1)
        self.assertTrue(prediction.drivers)
        self.assertIn("preference", prediction.policy_signal)
        self.assertNotEqual(prediction.cge_sam_account, "unmapped")
        self.assertIn("accuracy", metrics)
        self.assertIn("positive_rate", metrics)

    def test_model_persistence_round_trip(self) -> None:
        examples = load_examples(Path("data/sample_preferences.csv"))
        request = PreferenceRequest(
            user_id="user_002",
            item_id="policy_digest",
            category="research",
            price=12.0,
            rating=4.8,
            popularity=0.88,
        )

        temp_dir = Path("tests/_tmp")
        temp_dir.mkdir(exist_ok=True)
        model_path = temp_dir / "signal_model.joblib"

        model = PreferenceModel().train(examples)
        before = model.predict(request)
        model.save(model_path)
        after = PreferenceModel.load(model_path).predict(request)

        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
