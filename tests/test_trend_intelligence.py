from __future__ import annotations

import unittest

import trend_intelligence


class TrendIntelligenceTests(unittest.TestCase):
    def test_analyze_trend_signal_returns_expected_shape(self) -> None:
        record = {
            "trend_name": "#KenyaBudget",
            "rank": 1,
            "tweet_volume": 185000,
            "location": "Kenya",
            "fetched_at": "2026-05-07T00:00:00+00:00",
            "source": "Demo fallback - X API not connected",
        }

        result = trend_intelligence.analyze_trend_signal(record)
        required = {
            "trend_name",
            "location",
            "rank",
            "tweet_volume",
            "source",
            "demand_classification",
            "confidence_score",
            "aggregate_demand_score",
            "opportunity_score",
            "emerging_trend_probability",
            "unmet_demand_probability",
            "investment_policy_interpretation",
            "model_source_explanation",
        }

        self.assertTrue(required.issubset(result.keys()))
        self.assertIsInstance(result["model_source_explanation"], str)

    def test_batch_summary_mentions_proxy_estimates(self) -> None:
        analyses = [
            {
                "trend_name": "#AIWorkflows",
                "opportunity_score": 74.5,
                "emerging_trend_probability": 72.0,
                "unmet_demand_probability": 38.0,
            },
            {
                "trend_name": "Digital Payments",
                "opportunity_score": 61.2,
                "emerging_trend_probability": 43.0,
                "unmet_demand_probability": 66.0,
            },
        ]

        summary = trend_intelligence.summarize_trend_batch("Global", analyses)

        self.assertIn("Global", summary)
        self.assertIn("proxy estimates", summary)


if __name__ == "__main__":
    unittest.main()
