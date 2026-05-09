"""Benchmark flow extraction for the Signal CGE calibration prototype."""

from __future__ import annotations

from typing import Any

import pandas as pd


def validate_sam_matrix(sam_df: pd.DataFrame) -> pd.DataFrame:
    """Validate and normalize a square SAM matrix."""

    if not isinstance(sam_df, pd.DataFrame):
        raise TypeError("SAM must be provided as a pandas DataFrame.")
    if sam_df.empty:
        raise ValueError("SAM must not be empty.")
    if sam_df.shape[0] != sam_df.shape[1]:
        raise ValueError("SAM must be a square matrix.")
    row_labels = [str(item) for item in sam_df.index]
    column_labels = [str(item) for item in sam_df.columns]
    if set(row_labels) != set(column_labels):
        raise ValueError("SAM row and column labels must match.")
    matrix = sam_df.copy()
    matrix.index = row_labels
    matrix.columns = column_labels
    return matrix.apply(pd.to_numeric, errors="raise").astype(float)


def extract_benchmark_flows(sam_df: pd.DataFrame, account_classification: dict[str, list[str]]) -> dict[str, Any]:
    """Extract benchmark flows needed for future CGE calibration."""

    matrix = validate_sam_matrix(sam_df)
    row_totals = matrix.sum(axis=1)
    column_totals = matrix.sum(axis=0).reindex(matrix.index)
    groups = account_classification
    commodities = groups.get("commodities", [])
    activities = groups.get("activities", [])
    factors = groups.get("factors", [])
    households = groups.get("households", [])
    government = groups.get("government", [])
    savings_investment = groups.get("savings_investment", [])
    rest_of_world = groups.get("rest_of_world", [])

    return {
        "row_totals": row_totals.round(8).to_dict(),
        "column_totals": column_totals.round(8).to_dict(),
        "imbalance": (row_totals - column_totals).round(8).to_dict(),
        "activity_output": {account: float(row_totals.get(account, 0.0)) for account in activities},
        "commodity_demand": {account: float(row_totals.get(account, 0.0)) for account in commodities},
        "factor_payments": _submatrix(matrix, factors, activities),
        "household_income": {account: float(row_totals.get(account, 0.0)) for account in households},
        "government_demand": _submatrix(matrix, commodities, government),
        "investment_demand": _submatrix(matrix, commodities, savings_investment),
        "imports": _submatrix(matrix, rest_of_world, commodities),
        "exports": _submatrix(matrix, commodities, rest_of_world),
    }


def _submatrix(matrix: pd.DataFrame, rows: list[str], columns: list[str]) -> dict[str, dict[str, float]]:
    valid_rows = [row for row in rows if row in matrix.index]
    valid_columns = [column for column in columns if column in matrix.columns]
    if not valid_rows or not valid_columns:
        return {}
    frame = matrix.loc[valid_rows, valid_columns].round(8)
    return {row: frame.loc[row].to_dict() for row in frame.index}
