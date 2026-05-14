"""AI-native behavioral-economic intelligence pipeline."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.analytics import compute_signal_metrics
from Behavioral_Signals_AI.backend.signal_ingestion import ingest_aggregate_trends
from Behavioral_Signals_AI.behavioral_inference import infer_aggregate_behavior
from Behavioral_Signals_AI.demand_intelligence import map_trend_to_demand_signal
from Behavioral_Signals_AI.forecasting import forecast_trend_persistence
from Behavioral_Signals_AI.market_intelligence import summarize_market_intelligence
from Behavioral_Signals_AI.opportunity_engine import infer_opportunity
from Behavioral_Signals_AI.revealed_preference_engine import infer_revealed_preference


def run_behavioral_intelligence_pipeline(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Run the full aggregate trend to revealed-demand intelligence pipeline."""

    sanitized = ingest_aggregate_trends(records)
    enriched = []
    for trend in sanitized:
        metrics = compute_signal_metrics(trend)
        preference = infer_revealed_preference(trend, metrics)
        behavior = infer_aggregate_behavior(trend, metrics)
        opportunity = infer_opportunity(trend, metrics, preference)
        forecast = forecast_trend_persistence(trend, metrics)
        demand_signal = map_trend_to_demand_signal({**trend, **metrics})
        enriched.append({**demand_signal, **metrics, **preference, **behavior, **opportunity, **forecast})
    return {"signals": enriched, "market_summary": summarize_market_intelligence(enriched)}