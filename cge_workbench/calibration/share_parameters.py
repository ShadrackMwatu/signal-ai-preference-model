"""Share-parameter calibration for Signal CGE prototype blocks."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .account_classifier import AccountClassification


def calibrate_share_parameters(sam: pd.DataFrame, classification: AccountClassification) -> dict[str, Any]:
    matrix = sam.astype(float)
    return {
        "production": _column_shares(matrix, classification.factors + classification.commodities, classification.activities),
        "household_demand": _column_shares(matrix, classification.commodities, classification.households),
        "government_demand": _column_shares(matrix, classification.commodities, classification.government),
        "investment_demand": _column_shares(matrix, classification.commodities, classification.investment),
        "trade_imports": _row_shares(matrix, classification.imports + classification.rest_of_world, classification.commodities),
        "trade_exports": _column_shares(matrix, classification.commodities, classification.exports + classification.rest_of_world),
        "factor_payments": _column_shares(matrix, classification.factors, classification.activities),
    }


def _column_shares(matrix: pd.DataFrame, rows: list[str], columns: list[str]) -> dict[str, dict[str, float]]:
    valid_rows = [row for row in rows if row in matrix.index]
    valid_columns = [column for column in columns if column in matrix.columns]
    if not valid_rows or not valid_columns:
        return {}
    sub = matrix.loc[valid_rows, valid_columns]
    totals = sub.sum(axis=0).replace(0, 1)
    shares = sub.divide(totals, axis=1).fillna(0.0).round(8)
    return {column: shares[column].to_dict() for column in shares.columns}


def _row_shares(matrix: pd.DataFrame, rows: list[str], columns: list[str]) -> dict[str, dict[str, float]]:
    valid_rows = [row for row in rows if row in matrix.index]
    valid_columns = [column for column in columns if column in matrix.columns]
    if not valid_rows or not valid_columns:
        return {}
    sub = matrix.loc[valid_rows, valid_columns]
    totals = sub.sum(axis=1).replace(0, 1)
    shares = sub.divide(totals, axis=0).fillna(0.0).round(8)
    return {row: shares.loc[row].to_dict() for row in shares.index}
