"""Share-parameter calibration for the Signal CGE prototype."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .benchmark_extractor import validate_sam_matrix


def calibrate_share_parameters(sam_df: pd.DataFrame, account_classification: dict[str, list[str]]) -> dict[str, Any]:
    """Compute simple benchmark shares with zero-safe denominators."""

    matrix = validate_sam_matrix(sam_df)
    groups = account_classification
    commodities = groups.get("commodities", [])
    activities = groups.get("activities", [])
    factors = groups.get("factors", [])
    households = groups.get("households", [])
    government = groups.get("government", [])
    savings_investment = groups.get("savings_investment", [])
    rest_of_world = groups.get("rest_of_world", [])

    return _clean_nested(
        {
            "production_input_shares": _column_shares(matrix, factors + commodities, activities),
            "household_expenditure_shares": _column_shares(matrix, commodities, households),
            "government_demand_shares": _column_shares(matrix, commodities, government),
            "investment_demand_shares": _column_shares(matrix, commodities, savings_investment),
            "export_shares": _column_shares(matrix, commodities, rest_of_world),
            "import_shares": _row_shares(matrix, rest_of_world, commodities),
            "factor_income_shares": _row_shares(matrix, factors, activities),
        }
    )


def _column_shares(matrix: pd.DataFrame, rows: list[str], columns: list[str]) -> dict[str, dict[str, float]]:
    valid_rows = [row for row in rows if row in matrix.index]
    valid_columns = [column for column in columns if column in matrix.columns]
    if not valid_rows or not valid_columns:
        return {}
    sub = matrix.loc[valid_rows, valid_columns]
    totals = sub.sum(axis=0)
    shares = {
        column: {row: _safe_divide(float(sub.loc[row, column]), float(totals[column])) for row in valid_rows}
        for column in valid_columns
    }
    return shares


def _row_shares(matrix: pd.DataFrame, rows: list[str], columns: list[str]) -> dict[str, dict[str, float]]:
    valid_rows = [row for row in rows if row in matrix.index]
    valid_columns = [column for column in columns if column in matrix.columns]
    if not valid_rows or not valid_columns:
        return {}
    sub = matrix.loc[valid_rows, valid_columns]
    totals = sub.sum(axis=1)
    shares = {
        row: {column: _safe_divide(float(sub.loc[row, column]), float(totals[row])) for column in valid_columns}
        for row in valid_rows
    }
    return shares


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    value = numerator / denominator
    if value != value or value in {float("inf"), float("-inf")}:
        return 0.0
    return round(float(value), 8)


def _clean_nested(payload: dict[str, Any]) -> dict[str, Any]:
    """Ensure the returned structure contains plain finite floats only."""

    return payload
