import unittest

from src.data_pipeline.data_loader import load_behavioral_signals
from src.features.aggregation import aggregate_features
from src.features.feature_engineering import FEATURE_COLUMNS, build_feature_table
from src.features.text_features import extract_text_features


class FeatureEngineeringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_behavioral_signals("data/sample_behavioral_signals.csv")

    def test_text_features_extract_nlp_signals(self) -> None:
        features = extract_text_features("ready to buy solar kits but complaints about delays")

        self.assertGreater(features["purchase_intent_score"], 0)
        self.assertGreater(features["complaint_score"], 0)
        self.assertGreater(features["urgency_score"], 0)
        self.assertIn("solar", features["topic_keywords"])

    def test_feature_table_contains_required_features(self) -> None:
        features = build_feature_table(self.raw)

        for column in FEATURE_COLUMNS:
            self.assertIn(column, features.columns)
            self.assertFalse(features[column].isna().any())
        self.assertIn("behavioral_signal_score", features.columns)

    def test_aggregation_has_no_individual_level_outputs(self) -> None:
        aggregated = aggregate_features(build_feature_table(self.raw))

        self.assertIn("county", aggregated.columns)
        self.assertIn("consumer_segment", aggregated.columns)
        self.assertNotIn("signal_id", aggregated.columns)
        self.assertNotIn("text", aggregated.columns)


if __name__ == "__main__":
    unittest.main()
