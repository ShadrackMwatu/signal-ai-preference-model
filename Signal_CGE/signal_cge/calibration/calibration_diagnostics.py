"""Diagnostics for Signal CGE calibration readiness."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .benchmark_extractor import validate_sam_matrix


REQUIRED_FOR_PROTOTYPE = ["activities", "commodities", "factors", "households", "government"]


def run_calibration_diagnostics(
    sam_df: pd.DataFrame,
    account_classification: dict[str, list[str]],
    tolerance: float = 1e-6,
) -> dict[str, Any]:
    """Assess SAM quality and readiness for multiplier/CGE calibration use."""

    matrix = validate_sam_matrix(sam_df)
    row_totals = matrix.sum(axis=1)
    column_totals = matrix.sum(axis=0).reindex(matrix.index)
    imbalance = row_totals - column_totals
    warnings: list[str] = [
        "Full CGE equations are still placeholders; this calibration prepares benchmark data only."
    ]
    errors: list[str] = []

    zero_rows = row_totals[row_totals == 0].index.tolist()
    zero_columns = column_totals[column_totals == 0].index.tolist()
    negative_count = int((matrix < 0).sum().sum())
    missing_categories = [
        category for category in REQUIRED_FOR_PROTOTYPE if not account_classification.get(category)
    ]
    if not bool((imbalance.abs() <= tolerance).all()):
        warnings.append("SAM row-column balance exceeds tolerance for one or more accounts.")
    if zero_rows:
        warnings.append("Zero-row accounts detected: " + ", ".join(zero_rows))
    if zero_columns:
        warnings.append("Zero-column accounts detected: " + ", ".join(zero_columns))
    if negative_count:
        warnings.append(f"SAM contains {negative_count} negative value(s).")
    if missing_categories:
        warnings.append("Missing account categories: " + ", ".join(missing_categories))

    cge_ready = not missing_categories and not zero_columns and negative_count == 0
    full_ready = cge_ready and bool((imbalance.abs() <= tolerance).all())
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "max_absolute_imbalance": float(imbalance.abs().max()) if not imbalance.empty else 0.0,
        "zero_row_accounts": zero_rows,
        "zero_column_accounts": zero_columns,
        "negative_value_count": negative_count,
        "missing_account_categories": missing_categories,
        "readiness": {
            "sam_multiplier_analysis": "ready" if not errors else "not_ready",
            "prototype_cge_calibration": "ready_with_warnings" if cge_ready else "limited",
            "full_equilibrium_cge_solving": "not_ready_placeholder_equations" if full_ready else "not_ready",
        },
    }
