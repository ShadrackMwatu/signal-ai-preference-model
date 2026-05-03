import unittest
from pathlib import Path

from src.clustering import CountySegmentClusterer
from src.data_pipeline import (
    DEFAULT_BEHAVIORAL_DATA_PATH,
    BehavioralDataConfig,
    KENYA_COUNTIES,
    generate_behavioral_dataset,
    load_behavioral_data,
    validate_privacy,
    write_behavioral_dataset,
)
from src.evaluation import evaluate_signal_system
from src.features import FEATURE_COLUMNS, BehavioralFeatureExtractor
from src.models import SignalDemandIntelligenceSystem


DEMAND_CLASSES = {
    "High demand",
    "Moderate demand",
    "Low demand",
    "Emerging demand",
    "Declining demand",
    "Unmet demand",
}


class MarketIntelligenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.frame = load_behavioral_data(DEFAULT_BEHAVIORAL_DATA_PATH)
        cls.system = SignalDemandIntelligenceSystem().fit(cls.frame)

    def test_data_pipeline_generates_kenya_county_data(self) -> None:
        frame = generate_behavioral_dataset()

        self.assertEqual(set(KENYA_COUNTIES), set(frame["county"].unique()))
        self.assertIn("clicks", frame.columns)
        self.assertIn("purchase_intent_phrases", frame.columns)
        self.assertEqual(set(frame["country"]), {"Kenya"})
        self.assertNotIn("user_id", frame.columns)
        self.assertGreaterEqual(frame["segment_size"].min(), 30)

    def test_write_and_load_behavioral_dataset(self) -> None:
        output_path = Path("tests/_tmp/behavioral_signals.csv")
        config = BehavioralDataConfig(
            periods=("2026-Q1", "2026-Q2"),
            counties=("Nairobi", "Mombasa"),
            categories=("agri_inputs", "retail"),
            segments=("budget_seekers", "growth_smes"),
            seed=12,
        )

        written = write_behavioral_dataset(output_path, config)
        loaded = load_behavioral_data(output_path)

        self.assertEqual(len(written), len(loaded))
        self.assertEqual(set(loaded["county"]), {"Nairobi", "Mombasa"})

    def test_privacy_safeguards_reject_pii_and_small_segments(self) -> None:
        with_user_id = self.frame.copy()
        with_user_id["user_id"] = "person_001"
        with_email = self.frame.copy()
        with_email.loc[0, "text"] = "contact buyer@example.com"
        with_phone = self.frame.copy()
        with_phone.loc[0, "text"] = "call 0712345678"
        with_gps = self.frame.copy()
        with_gps["latitude"] = -1.286389
        with_psychological_targeting = self.frame.copy()
        with_psychological_targeting["personality_score"] = 0.7
        small_segment = self.frame.copy()
        small_segment.loc[0, "segment_size"] = 12

        with self.assertRaises(ValueError):
            validate_privacy(with_user_id)
        with self.assertRaises(ValueError):
            validate_privacy(with_email)
        with self.assertRaises(ValueError):
            validate_privacy(with_phone)
        with self.assertRaises(ValueError):
            validate_privacy(with_gps)
        with self.assertRaises(ValueError):
            validate_privacy(with_psychological_targeting)
        with self.assertRaises(ValueError):
            validate_privacy(small_segment)

    def test_feature_extraction_outputs_required_features(self) -> None:
        features = BehavioralFeatureExtractor().fit_transform(self.frame)

        for column in FEATURE_COLUMNS:
            self.assertIn(column, features.columns)
            self.assertFalse(features[column].isna().any())
        self.assertTrue(features["sentiment_score"].between(0, 1).all())
        self.assertTrue(features["purchase_intent_score"].between(0, 1).all())
        self.assertTrue(features["dissatisfaction_score"].between(0, 1).all())

    def test_clustering_identifies_segments_and_county_patterns(self) -> None:
        features = BehavioralFeatureExtractor().fit_transform(self.frame)
        clusterer = CountySegmentClusterer().fit(features)
        clustered = clusterer.transform(features)
        county_patterns = clusterer.summarize_county_patterns(features)

        self.assertIn("segment_cluster", clustered.columns)
        self.assertIn("county_pattern_cluster", clustered.columns)
        self.assertEqual(len(county_patterns), len(KENYA_COUNTIES))

    def test_market_model_outputs_revealed_demand_intelligence(self) -> None:
        result = self.system.predict(self.frame.head(40))
        record = result["records"][0]
        dashboard = result["dashboard"]

        self.assertEqual(record["country"], "Kenya")
        self.assertIn("consumer_segment", record)
        self.assertNotIn("user_id", record)
        self.assertNotIn("anonymized_segment", record)
        self.assertIn(record["demand_classification"], DEMAND_CLASSES)
        self.assertIn("behavioral_signal_score", record)
        self.assertIn("aggregate_demand_score", record)
        self.assertIn("opportunity_score", record)
        self.assertIn("emerging_trend_probability", record)
        self.assertIn("unmet_demand_probability", record)
        self.assertIn("likely_market_gap", record)
        self.assertIn("recommended_value_proposition", record)
        self.assertIn("product_service_opportunity", record)
        self.assertIn("revenue_model", record)
        self.assertIn("market_entry_strategy", record)
        self.assertIn("price_gap", record)
        self.assertIn("service_gap", record)
        self.assertIn("delivery_gap", record)
        self.assertIn("supplier_recommendation", record)
        self.assertIn("logistics_recommendation", record)
        self.assertIn("payment_recommendation", record)
        self.assertIn("model_version", dashboard)
        self.assertIn("national_aggregate_demand_index", dashboard)
        self.assertIn("consumer_segment_index", dashboard)
        self.assertIn("competitor_analysis", dashboard)
        self.assertIn("price_gaps", dashboard["competitor_analysis"])
        self.assertIn("service_gaps", dashboard["competitor_analysis"])
        self.assertIn("delivery_gaps", dashboard["competitor_analysis"])
        self.assertIn("unserved_counties", dashboard)

    def test_evaluation_reports_classification_and_regression_metrics(self) -> None:
        metrics = evaluate_signal_system(self.system, self.frame.head(100))

        self.assertIn("accuracy", metrics["classification"])
        self.assertIn("precision", metrics["classification"])
        self.assertIn("recall", metrics["classification"])
        self.assertIn("f1", metrics["classification"])
        self.assertIn("rmse", metrics["aggregate_demand_score"])
        self.assertIn("mae", metrics["opportunity_score"])

    def test_adaptive_loop_detects_drift_and_retrains(self) -> None:
        drift_frame = self.frame.copy()
        drift_frame["clicks"] = drift_frame["clicks"] * 4
        drift_frame["searches"] = drift_frame["searches"] * 3

        log = self.system.retrain_if_needed(drift_frame, drift_threshold=0.01)

        self.assertGreaterEqual(log.drift_score, 0)
        self.assertTrue(log.retraining_triggered)
        self.assertGreaterEqual(log.records_used, len(drift_frame))
        self.assertGreaterEqual(log.model_version, 2)
        self.assertTrue(self.system.retraining_logs)


if __name__ == "__main__":
    unittest.main()
