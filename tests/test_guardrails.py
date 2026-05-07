from __future__ import annotations

import unittest

import app


class GuardrailTests(unittest.TestCase):
    def test_low_demand_high_opportunity_becomes_unmet_demand_investigation(self) -> None:
        result = app._apply_guardrails(  # noqa: SLF001
            {
                "demand_classification": "Low Demand",
                "demand_band": "Low Demand",
                "confidence_score": 0.74,
                "aggregate_demand_score": 30.0,
                "opportunity_score": 72.0,
                "unmet_demand_probability": 0.38,
                "emerging_trend_probability": 0.4,
                "prediction_source": "Trained ML Model",
                "model_source_components": ["Trained ML Model"],
                "explanation_note": "Primary prediction produced by the trained local Signal model.",
            },
            {"unmet_need_signal": 0.84, "noise_score": 0.22, "searches": 180, "engagement_intensity": 0.34},
        )
        self.assertEqual(result["investment_opportunity_interpretation"], "Investigate Anomaly / Possible Unmet Demand")
        self.assertIn("Guardrail Adjustment", result["model_source_label"])

    def test_high_demand_low_confidence_becomes_monitor_further(self) -> None:
        result = app._apply_guardrails(  # noqa: SLF001
            {
                "demand_classification": "High Demand",
                "demand_band": "High Demand",
                "confidence_score": 0.51,
                "aggregate_demand_score": 68.0,
                "opportunity_score": 63.0,
                "unmet_demand_probability": 0.22,
                "emerging_trend_probability": 0.33,
                "prediction_source": "Trained ML Model",
                "model_source_components": ["Trained ML Model"],
                "explanation_note": "Primary prediction produced by the trained local Signal model.",
            },
            {"noise_score": 0.18, "searches": 80, "engagement_intensity": 0.82},
        )
        self.assertEqual(result["investment_opportunity_interpretation"], "Monitor Further")


if __name__ == "__main__":
    unittest.main()
