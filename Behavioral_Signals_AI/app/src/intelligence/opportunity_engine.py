"""Opportunity engine from revealed demand to value proposition."""

from __future__ import annotations

import pandas as pd


def generate_opportunities(predictions: pd.DataFrame) -> pd.DataFrame:
    """Add value proposition, product/service opportunity, and revenue model."""

    output = predictions.copy()
    output["recommended_value_proposition"] = output.apply(_value_proposition, axis=1)
    output["product_or_service_opportunity"] = output.apply(_product_or_service, axis=1)
    output["revenue_model"] = output.apply(_revenue_model, axis=1)
    output["market_gap"] = output["unmet_demand_probability"].round(4)
    return output


def _value_proposition(row: pd.Series) -> str:
    category = str(row["category"]).replace("_", " ")
    if row["unmet_demand_probability"] >= 0.55:
        return f"accessible {category} with faster fulfillment"
    if row["aggregate_demand_score"] >= 0.65:
        return f"trusted {category} with transparent pricing"
    return f"low-friction {category} discovery for underserved buyers"


def _product_or_service(row: pd.Series) -> str:
    category = row["category"]
    unmet = row["unmet_demand_probability"] >= 0.55
    if category == "agri_inputs":
        return "bundled input ordering service" if unmet else "verified farm input marketplace"
    if category == "clean_energy":
        return "solar maintenance network" if unmet else "pay as you go solar kits"
    if category == "digital_services":
        return "SME analytics assistant" if unmet else "mobile business dashboard"
    if category == "transport":
        return "last mile logistics coordination" if unmet else "route tracking service"
    return "county retail availability platform"


def _revenue_model(row: pd.Series) -> str:
    if row["category"] in {"digital_services", "clean_energy"} and row["opportunity_score"] >= 0.55:
        return "subscription"
    if row["opportunity_score"] >= 0.62:
        return "commission"
    return "transaction_fee"
