from __future__ import annotations

from Behavioral_Signals_AI.backend import run_behavioral_intelligence_pipeline
from Behavioral_Signals_AI.analytics import compute_signal_metrics
from Behavioral_Signals_AI.revealed_preference_engine import infer_revealed_preference


def test_behavioral_pipeline_returns_revealed_demand_signals():
    result = run_behavioral_intelligence_pipeline(
        [
            {
                "trend_name": "Fuel prices",
                "category": "prices",
                "location": "Kenya",
                "volume": 120000,
                "rank": 1,
                "confidence": 0.82,
                "relevance_to_demand": 0.78,
            }
        ]
    )

    assert result["signals"]
    signal = result["signals"][0]
    assert signal["revealed_aggregate_demand"] in {"High revealed demand", "Moderate revealed demand", "Emerging revealed demand"}
    assert signal["opportunity_type"]
    assert signal["forecast_outlook"]
    assert signal["recommendation"]
    assert result["market_summary"]["headline"]


def test_signal_metrics_are_normalized_without_personal_data():
    metrics = compute_signal_metrics({"trend_name": "Healthcare access", "category": "health", "rank": 2})

    assert 0 <= metrics["signal_strength"] <= 100
    assert 0 <= metrics["economic_pressure"] <= 100
    assert 0 <= metrics["persistence"] <= 100


def test_revealed_preference_inference_is_aggregate():
    preference = infer_revealed_preference(
        {"trend_name": "Digital lending", "category": "finance"},
        {"signal_strength": 64, "economic_pressure": 58, "persistence": 61},
    )

    assert "revealed_interest" in preference
    assert "revealed_aggregate_demand" in preference
    assert "individual" not in str(preference).lower()