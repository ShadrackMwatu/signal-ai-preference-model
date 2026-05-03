import unittest

import pandas as pd

from src.data_pipeline.data_loader import load_behavioral_signals
from src.features.aggregation import aggregate_features
from src.features.feature_engineering import build_feature_table
from src.models.predict_demand import DemandPredictor
from src.models.train_demand_model import train_demand_models


class PredictionOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_behavioral_signals("data/sample_behavioral_signals.csv")
        cls.competitors = pd.read_csv("data/sample_competitors.csv")
        cls.features = aggregate_features(build_feature_table(cls.raw))
        cls.bundle = train_demand_models(cls.features, "tests/_tmp/test_prediction_bundle.joblib")

    def test_prediction_outputs_include_dashboard_fields(self) -> None:
        predictions = DemandPredictor(self.bundle).predict(self.raw.head(30), self.competitors)
        required = {
            "behavioral_signal_score",
            "aggregate_demand_score",
            "opportunity_score",
            "demand_classification",
            "trend_direction",
            "demand_forecast",
            "recommended_value_proposition",
            "product_or_service_opportunity",
            "revenue_model",
            "competitor_gap",
            "supplier_recommendation",
            "logistics_recommendation",
            "payment_recommendation",
        }

        self.assertTrue(required.issubset(predictions.columns))
        self.assertNotIn("signal_id", predictions.columns)
        self.assertNotIn("text", predictions.columns)


if __name__ == "__main__":
    unittest.main()
