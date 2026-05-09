"""Aggregate county-level supplier, logistics, and payment recommendations."""

from __future__ import annotations

import pandas as pd


def generate_recommendations(predictions: pd.DataFrame) -> pd.DataFrame:
    """Generate recommendations from county/category aggregate patterns."""

    output = predictions.copy()
    output["supplier_recommendation"] = output.apply(_supplier, axis=1)
    output["logistics_recommendation"] = output.apply(_logistics, axis=1)
    output["payment_recommendation"] = output.apply(_payment, axis=1)
    return output


def _supplier(row: pd.Series) -> str:
    if row.get("unserved_county", False):
        return "regional supplier pooling"
    if row["category"] in {"agri_inputs", "retail"}:
        return "multi-supplier marketplace"
    return "certified specialist suppliers"


def _logistics(row: pd.Series) -> str:
    if row["county"] in {"Turkana", "Machakos"}:
        return "hub and spoke delivery"
    if row["county"] in {"Nairobi", "Kiambu"}:
        return "same day courier"
    return "scheduled route delivery"


def _payment(row: pd.Series) -> str:
    if row["consumer_segment"] == "budget_seekers":
        return "pay in installments"
    if row["consumer_segment"] == "growth_smes":
        return "invoice and wallet rails"
    return "mobile money checkout"
