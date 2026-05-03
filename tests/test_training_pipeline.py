import unittest

from src.data_pipeline.data_loader import load_behavioral_signals
from src.features.aggregation import aggregate_features
from src.features.feature_engineering import build_feature_table
from src.models.train_demand_model import TARGET_LABELS, train_demand_models


class TrainingPipelineTests(unittest.TestCase):
    def test_training_pipeline_builds_all_models(self) -> None:
        raw = load_behavioral_signals("data/sample_behavioral_signals.csv")
        features = aggregate_features(build_feature_table(raw))

        bundle = train_demand_models(features, "tests/_scratch/test_training_bundle.joblib")

        self.assertEqual(bundle.training_rows, len(features))
        self.assertEqual(bundle.model_version, 1)
        self.assertTrue(set(bundle.demand_classifier.named_steps["model"].classes_).issubset(set(TARGET_LABELS)))
        self.assertTrue(bundle.feature_baseline)


if __name__ == "__main__":
    unittest.main()
