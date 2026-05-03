import unittest

import pandas as pd

from src.intelligence.competitor_analysis import analyze_competitor_gaps
from src.intelligence.market_access import generate_market_access
from src.intelligence.opportunity_engine import generate_opportunities
from src.intelligence.recommendations import generate_recommendations


class OpportunityEngineTests(unittest.TestCase):
    def test_opportunity_chain_generates_market_recommendations(self) -> None:
        predictions = pd.DataFrame(
            [
                {
                    "country": "Kenya",
                    "county": "Turkana",
                    "category": "clean_energy",
                    "consumer_segment": "budget_seekers",
                    "time_period": "2026-Q4",
                    "behavioral_signal_score": 0.64,
                    "aggregate_demand_score": 0.72,
                    "opportunity_score": 0.81,
                    "emerging_trend_probability": 0.74,
                    "unmet_demand_probability": 0.69,
                    "demand_classification": "Unmet demand",
                    "trend_direction": "rising",
                    "demand_forecast": 0.78,
                }
            ]
        )
        competitors = pd.DataFrame(
            [
                {
                    "county": "Turkana",
                    "category": "clean_energy",
                    "competitor_count": 1,
                    "average_price_index": 0.75,
                    "service_quality_index": 0.41,
                    "delivery_reliability_index": 0.35,
                }
            ]
        )

        enriched = generate_recommendations(
            generate_market_access(analyze_competitor_gaps(generate_opportunities(predictions), competitors))
        )

        self.assertEqual(enriched.loc[0, "product_or_service_opportunity"], "solar maintenance network")
        self.assertIn("partner-led", enriched.loc[0, "market_entry_strategy"])
        self.assertEqual(enriched.loc[0, "supplier_recommendation"], "regional supplier pooling")
        self.assertEqual(enriched.loc[0, "payment_recommendation"], "pay in installments")


if __name__ == "__main__":
    unittest.main()
