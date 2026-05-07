from __future__ import annotations

import unittest

import app


class PredictDemandTests(unittest.TestCase):
    def test_predict_demand_returns_legacy_shape(self) -> None:
        result = app.predict_demand(180, 50, 35, 220, 0.68, 0.82, 0.6)

        self.assertEqual(len(result), 3)
        self.assertIn(result[0], {"High Demand", "Moderate Demand", "Low Demand"})
        self.assertIsInstance(result[1], float)
        self.assertIsInstance(result[2], float)

    def test_predict_demand_details_include_intelligence_fields(self) -> None:
        result = app.predict_demand_details(180, 50, 35, 220, 0.68, 0.82, 0.6)
        required = {
            "demand_classification",
            "demand_band",
            "confidence_score",
            "aggregate_demand_score",
            "opportunity_score",
            "emerging_trend_probability",
            "unmet_demand_probability",
            "investment_opportunity_interpretation",
            "key_drivers",
            "key_driver_summary",
            "model_source_label",
        }
        self.assertTrue(required.issubset(result.keys()))


if __name__ == "__main__":
    unittest.main()
