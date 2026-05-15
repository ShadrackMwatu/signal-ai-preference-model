"""Forecasting foundation for Behavioral Signals AI."""

from .trend_forecaster import forecast_trend_persistence
from .demand_forecaster import forecast_demand
from .opportunity_forecaster import forecast_opportunity
from .signal_persistence_model import estimate_signal_persistence

__all__ = ["forecast_trend_persistence", "forecast_demand", "forecast_opportunity", "estimate_signal_persistence"]