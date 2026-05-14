from __future__ import annotations

from Behavioral_Signals_AI.demand_intelligence import map_trend_to_demand_signal, map_trends_to_demand_signals
from Behavioral_Signals_AI.live_trends.fallback_demo_provider import get_demo_trends
from Behavioral_Signals_AI.recommendation_engine import generate_trend_recommendation


def test_trend_to_demand_mapping_returns_interpretable_signal():
    signal = map_trend_to_demand_signal(
        {
            "trend_name": "Fuel prices",
            "category": "prices",
            "volume": 120000,
            "confidence": 0.8,
            "relevance_to_demand": 0.75,
            "location": "Kenya",
        }
    )

    assert signal["trend_name"] == "Fuel prices"
    assert "price" in signal["inferred_demand_category"]
    assert signal["demand_signal_strength"] > 50
    assert signal["possible_unmet_demand"] > 50
    assert signal["urgency"] in {"Medium", "High"}
    assert signal["affected_county_or_scope"] == "National scope"
    assert signal["business_implication"]
    assert signal["policy_implication"]
    assert signal["confidence_score"] > 50


def test_missing_volume_fields_are_handled_gracefully():
    signal = map_trend_to_demand_signal(
        {
            "trend_name": "Healthcare access",
            "category": "health",
            "confidence": 0.6,
            "location": "Nairobi",
        }
    )

    assert signal["demand_signal_strength"] > 0
    assert signal["possible_unmet_demand"] > 0
    assert signal["affected_county_or_scope"] == "Nairobi County"


def test_demo_fallback_trends_map_to_demand_signals():
    trends = get_demo_trends("Kenya", limit=3)
    signals = map_trends_to_demand_signals(trends)

    assert len(signals) == 3
    assert all(signal["recommendation"] for signal in signals)
    assert all("trend_name" in signal for signal in signals)


def test_recommendation_generation_uses_signal_context():
    recommendation = generate_trend_recommendation(
        {
            "trend_name": "Nairobi transport",
            "inferred_demand_category": "transport and logistics demand",
            "urgency": "High",
            "unmet_demand_likelihood": 80,
        }
    )

    assert "Prioritize" in recommendation
    assert "transport" in recommendation.lower()