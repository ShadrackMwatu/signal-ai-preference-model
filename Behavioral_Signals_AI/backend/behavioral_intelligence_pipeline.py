"""AI-native behavioral-economic intelligence pipeline."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.analytics import compute_signal_metrics
from Behavioral_Signals_AI.adaptive_learning.online_calibrator import calibrate_prediction
from Behavioral_Signals_AI.adaptive_learning.prediction_memory import build_prediction_snapshot, load_prediction_memory, save_prediction_snapshot
from Behavioral_Signals_AI.backend.signal_ingestion import ingest_aggregate_trends
from Behavioral_Signals_AI.behavioral_inference import infer_aggregate_behavior
from Behavioral_Signals_AI.demand_intelligence import map_trend_to_demand_signal
from Behavioral_Signals_AI.forecasting import forecast_demand, forecast_opportunity, forecast_trend_persistence, estimate_signal_persistence
from Behavioral_Signals_AI.market_intelligence import summarize_market_intelligence
from Behavioral_Signals_AI.opportunity_engine import infer_opportunity
from Behavioral_Signals_AI.revealed_preference_engine import infer_revealed_preference


def run_behavioral_intelligence_pipeline(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Run the full aggregate trend to revealed-demand intelligence pipeline."""

    sanitized = ingest_aggregate_trends(records)
    history = load_prediction_memory(limit=200)
    enriched = []
    for trend in sanitized:
        metrics = compute_signal_metrics(trend)
        calibration = calibrate_prediction({**trend, **metrics}, history)
        preference = infer_revealed_preference(trend, {**metrics, **calibration})
        behavior = infer_aggregate_behavior(trend, metrics)
        opportunity = infer_opportunity(trend, metrics, preference)
        persistence = estimate_signal_persistence(trend, history)
        trend_forecast = forecast_trend_persistence(trend, {**metrics, **persistence})
        demand_signal = map_trend_to_demand_signal({**trend, **metrics, **calibration})
        demand_forecast = forecast_demand({**demand_signal, **metrics, **calibration, **persistence})
        opportunity_forecast = forecast_opportunity({**demand_signal, **opportunity, **calibration, **demand_forecast})
        signal = {
            **trend,
            **demand_signal,
            **metrics,
            **calibration,
            **preference,
            **behavior,
            **opportunity,
            **persistence,
            **trend_forecast,
            **demand_forecast,
            **opportunity_forecast,
        }
        save_prediction_snapshot(build_prediction_snapshot(signal))
        enriched.append(signal)
    return {"signals": enriched, "market_summary": summarize_market_intelligence(enriched)}