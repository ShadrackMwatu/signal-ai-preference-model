"""Market access planning outputs."""

from __future__ import annotations

import pandas as pd


def generate_market_access(predictions: pd.DataFrame) -> pd.DataFrame:
    """Generate market access planning metrics and entry strategy."""

    output = predictions.copy()
    output["pricing_power"] = (
        output["aggregate_demand_score"] * (1 - output["unmet_demand_probability"] * 0.35)
    ).clip(0, 1).round(4)
    output["customer_reach"] = (
        output["behavioral_signal_score"] * (1 + output["emerging_trend_probability"] * 0.25)
    ).clip(0, 1).round(4)
    output["inventory_planning"] = (
        output["aggregate_demand_score"] * 0.55 + output["opportunity_score"] * 0.45
    ).clip(0, 1).round(4)
    output["sales_forecasting"] = (
        output["demand_forecast"] * 0.65 + output["opportunity_score"] * 0.35
    ).clip(0, 1).round(4)
    output["market_entry_strategy"] = output.apply(_market_entry_strategy, axis=1)
    return output


def _market_entry_strategy(row: pd.Series) -> str:
    category = str(row["category"]).replace("_", " ")
    if row.get("unserved_county", False):
        return f"partner-led entry for {category} in underserved {row['county']}"
    if row["opportunity_score"] >= 0.62:
        return f"digital-first launch for {category} in {row['county']}"
    return f"pilot and validate {category} demand in {row['county']}"
