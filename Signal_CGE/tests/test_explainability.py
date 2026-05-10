from __future__ import annotations

import unittest

from explainability import format_key_drivers_markdown, generate_prediction_explanation


class ExplainabilityTests(unittest.TestCase):
    def test_explanation_identifies_expected_drivers(self) -> None:
        explanation = generate_prediction_explanation(
            {
                "likes": 180,
                "comments": 52,
                "shares": 30,
                "searches": 210,
                "engagement_intensity": 0.74,
                "purchase_intent_score": 0.81,
                "trend_growth": 0.58,
                "noise_score": 0.22,
                "unmet_need_signal": 0.18,
            },
            {
                "demand_classification": "Strong Demand Momentum",
                "confidence_score": 0.88,
                "investment_opportunity_interpretation": "Strong Investment Opportunity",
                "unmet_demand_flag": False,
            },
        )

        markdown = format_key_drivers_markdown(explanation)
        self.assertIn("high likes", explanation["key_drivers"])
        self.assertIn("strong purchase intent", explanation["key_drivers"])
        self.assertIn("- high likes", markdown)
        self.assertTrue(explanation["driver_summary"].startswith("Signal classified this topic"))


if __name__ == "__main__":
    unittest.main()
