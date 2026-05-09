"""Calibration helpers for building a CGE benchmark dataset from a SAM."""

from __future__ import annotations

from typing import Any

import pandas as pd


CARE_FACTOR_SUFFIXES = {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"}


def calibrate_from_sam(sam: pd.DataFrame) -> dict[str, Any]:
    """Build a deterministic benchmark calibration summary from a SAM-like matrix."""

    matrix = _validate_sam_like(sam)
    row_totals = matrix.sum(axis=1)
    column_totals = matrix.sum(axis=0)
    total_flow = float(matrix.to_numpy().sum())
    accounts = [str(account) for account in matrix.index]
    activities = _classify_accounts(accounts, ["act", "activity", "prod", "care", "manufacturing", "transport"])
    factors = _classify_accounts(accounts, ["lab", "labor", "capital", *CARE_FACTOR_SUFFIXES])
    households = _classify_accounts(accounts, ["household", "hh"])
    government = _classify_accounts(accounts, ["government", "gov"])
    commodities = [account for account in accounts if account not in set(factors + households + government)]
    return {
        "accounts": accounts,
        "activities": activities,
        "commodities": commodities,
        "factors": factors,
        "households": households,
        "government": government,
        "row_totals": row_totals.round(8).to_dict(),
        "column_totals": column_totals.round(8).to_dict(),
        "total_flow": total_flow,
        "share_parameters": _column_shares(matrix),
        "kenya_gender_care_supported": CARE_FACTOR_SUFFIXES.issubset({account.lower() for account in accounts}),
        "diagnostics": _balance_diagnostics(row_totals, column_totals),
    }


def _validate_sam_like(sam: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(sam, pd.DataFrame):
        raise TypeError("SAM calibration requires a pandas DataFrame.")
    if sam.empty:
        raise ValueError("SAM calibration requires a non-empty DataFrame.")
    if sam.shape[0] != sam.shape[1]:
        raise ValueError("SAM calibration requires a square matrix.")
    if set(map(str, sam.index)) != set(map(str, sam.columns)):
        raise ValueError("SAM row and column accounts must match.")
    matrix = sam.copy()
    matrix.index = [str(account) for account in matrix.index]
    matrix.columns = [str(account) for account in matrix.columns]
    return matrix.apply(pd.to_numeric, errors="raise").astype(float)


def _column_shares(matrix: pd.DataFrame) -> dict[str, dict[str, float]]:
    totals = matrix.sum(axis=0).replace(0, 1)
    shares = matrix.divide(totals, axis=1).round(8)
    return {column: shares[column].to_dict() for column in shares.columns}


def _balance_diagnostics(row_totals: pd.Series, column_totals: pd.Series) -> dict[str, Any]:
    imbalance = row_totals - column_totals.reindex(row_totals.index)
    return {
        "max_absolute_imbalance": float(imbalance.abs().max()),
        "balanced": bool((imbalance.abs() <= 1e-6).all()),
    }


def _classify_accounts(accounts: list[str], markers: list[str]) -> list[str]:
    lowered_markers = [marker.lower() for marker in markers]
    return [account for account in accounts if any(marker in account.lower() for marker in lowered_markers)]
