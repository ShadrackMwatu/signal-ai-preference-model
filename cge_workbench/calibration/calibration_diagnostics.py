"""Diagnostics for the Signal CGE calibration prototype."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .account_classifier import AccountClassification, CARE_FACTOR_SUFFIXES


def run_calibration_diagnostics(sam: pd.DataFrame, classification: AccountClassification) -> dict[str, Any]:
    matrix = sam.astype(float)
    row_totals = matrix.sum(axis=1)
    column_totals = matrix.sum(axis=0).reindex(matrix.index)
    imbalance = row_totals - column_totals
    warnings: list[str] = [
        "Full CGE behavioural equations are placeholders; calibration currently prepares benchmark shares only.",
        "Use the Python SAM multiplier for screening until an open-source equilibrium solver is configured.",
    ]
    errors: list[str] = []
    if matrix.shape[0] != matrix.shape[1]:
        errors.append("SAM is not square.")
    if set(matrix.index) != set(matrix.columns):
        errors.append("SAM row and column accounts do not match.")
    if (matrix < 0).any().any():
        warnings.append("SAM contains negative values; confirm whether these are intended accounting entries.")
    zero_columns = column_totals[column_totals == 0].index.tolist()
    if zero_columns:
        warnings.append("Zero-column accounts detected: " + ", ".join(map(str, zero_columns)))
    if not classification.activities:
        warnings.append("No activity accounts were identified.")
    if not classification.factors:
        warnings.append("No factor accounts were identified.")
    if classification.kenya_gender_care_factors and not CARE_FACTOR_SUFFIXES.issubset({item.lower() for item in classification.kenya_gender_care_factors}):
        missing = sorted(CARE_FACTOR_SUFFIXES.difference({item.lower() for item in classification.kenya_gender_care_factors}))
        warnings.append("Partial Kenya gender-care factor coverage; missing: " + ", ".join(missing))
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "max_absolute_imbalance": float(imbalance.abs().max()) if not imbalance.empty else 0.0,
        "balanced": bool((imbalance.abs() <= 1e-6).all()) if not imbalance.empty else False,
        "zero_columns": zero_columns,
    }
