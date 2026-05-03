"""Opportunity score estimation from learned demand predictions and market factors."""

from __future__ import annotations

import os

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor


OPPORTUNITY_FEATURES = [
    "aggregate_demand_score",
    "unmet_demand_probability",
    "emerging_trend_probability",
    "market_gap",
    "supply_shortage",
    "scalability",
    "competition_intensity",
]


class OpportunityModel:
    """Learned opportunity estimator for market-gap analysis."""

    def __init__(self) -> None:
        self.model = GradientBoostingRegressor(random_state=42)
        self.is_trained = False

    def fit(self, frame: pd.DataFrame) -> "OpportunityModel":
        self.model.fit(frame[OPPORTUNITY_FEATURES], frame["opportunity_score"])
        self.is_trained = True
        return self

    def predict(self, frame: pd.DataFrame) -> pd.Series:
        if not self.is_trained:
            raise RuntimeError("OpportunityModel must be fitted before predict")
        return pd.Series(self.model.predict(frame[OPPORTUNITY_FEATURES])).clip(0, 1).round(4)
