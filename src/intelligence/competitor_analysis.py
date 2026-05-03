"""Competitor and market-gap intelligence."""

from __future__ import annotations

import pandas as pd


def analyze_competitor_gaps(predictions: pd.DataFrame, competitors: pd.DataFrame) -> pd.DataFrame:
    """Attach competitor, price, service, delivery, and unserved-county signals."""

    output = predictions.merge(competitors, on=["county", "category"], how="left")
    output["competitor_count"] = output["competitor_count"].fillna(0)
    output["average_price_index"] = output["average_price_index"].fillna(1.0)
    output["service_quality_index"] = output["service_quality_index"].fillna(0.5)
    output["delivery_reliability_index"] = output["delivery_reliability_index"].fillna(0.5)
    output["competitor_gap"] = output.apply(_competitor_gap, axis=1)
    output["price_gap"] = output["average_price_index"].apply(
        lambda value: "high affordability gap" if value < 0.85 else "moderate price gap"
    )
    output["service_gap"] = output["service_quality_index"].apply(
        lambda value: "service quality gap" if value < 0.6 else "limited service gap"
    )
    output["delivery_gap"] = output["delivery_reliability_index"].apply(
        lambda value: "delivery reliability gap" if value < 0.55 else "limited delivery gap"
    )
    output["customer_dissatisfaction"] = output["unmet_demand_probability"].apply(
        lambda value: "high dissatisfaction" if value >= 0.55 else "moderate dissatisfaction"
    )
    output["unserved_county"] = output["competitor_count"] <= 1
    return output


def _competitor_gap(row: pd.Series) -> str:
    if row["competitor_count"] <= 1:
        return f"low competitor coverage in {row['county']}"
    if row["service_quality_index"] < 0.6:
        return f"service gap in {row['category']}"
    return f"differentiation gap in {row['category']}"
