"""Benchmark flow extraction from a SAM-like matrix."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .account_classifier import AccountClassification


def extract_benchmark_flows(sam: pd.DataFrame, classification: AccountClassification) -> dict[str, Any]:
    matrix = sam.astype(float)
    row_totals = matrix.sum(axis=1)
    column_totals = matrix.sum(axis=0)
    return {
        "row_totals": row_totals.round(8).to_dict(),
        "column_totals": column_totals.round(8).to_dict(),
        "intermediate_flows": _submatrix(matrix, classification.commodities, classification.activities),
        "factor_payments": _submatrix(matrix, classification.factors, classification.activities),
        "household_consumption": _submatrix(matrix, classification.commodities, classification.households),
        "government_demand": _submatrix(matrix, classification.commodities, classification.government),
        "investment_demand": _submatrix(matrix, classification.commodities, classification.investment),
        "imports": _submatrix(matrix, classification.imports + classification.rest_of_world, classification.commodities),
        "exports": _submatrix(matrix, classification.commodities, classification.exports + classification.rest_of_world),
        "tax_payments": _submatrix(matrix, classification.taxes, list(matrix.columns)),
        "total_absorption": float(row_totals.sum()),
        "total_activity_cost": {activity: float(column_totals.get(activity, 0.0)) for activity in classification.activities},
    }


def _submatrix(matrix: pd.DataFrame, rows: list[str], columns: list[str]) -> dict[str, dict[str, float]]:
    valid_rows = [row for row in rows if row in matrix.index]
    valid_columns = [column for column in columns if column in matrix.columns]
    if not valid_rows or not valid_columns:
        return {}
    data = matrix.loc[valid_rows, valid_columns].round(8)
    return {row: data.loc[row].to_dict() for row in data.index}
