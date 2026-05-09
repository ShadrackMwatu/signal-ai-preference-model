"""SAM validation checks for the Signal CGE Workbench."""

from __future__ import annotations

from typing import Any

import pandas as pd


def validate_sam(sam: pd.DataFrame, tolerance: float = 1e-6) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    if sam.empty:
        errors.append("SAM is empty.")
        return {"valid": False, "errors": errors, "warnings": warnings}
    if list(sam.index) != list(sam.columns):
        errors.append("SAM row and column accounts do not match in the same order.")
    numeric = sam.apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any():
        errors.append("SAM contains non-numeric or missing values.")
    if (numeric < 0).any().any():
        warnings.append("SAM contains negative values; confirm whether these are intentional accounting entries.")
    row_totals = numeric.sum(axis=1)
    column_totals = numeric.sum(axis=0).reindex(numeric.index)
    imbalance = row_totals - column_totals
    max_base = pd.concat([row_totals.abs(), column_totals.abs()], axis=1).max(axis=1).replace(0, 1)
    imbalance_ratio = (imbalance / max_base).fillna(0)
    unbalanced = imbalance_ratio[imbalance_ratio.abs() > tolerance]
    if not unbalanced.empty:
        warnings.append(f"{len(unbalanced)} account(s) have row-column imbalance above tolerance.")
    zero_columns = column_totals[column_totals == 0].index.tolist()
    if zero_columns:
        warnings.append(f"Zero-column accounts detected: {', '.join(map(str, zero_columns))}.")
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "row_column_balance": imbalance_ratio.round(8).to_dict(),
        "zero_columns": zero_columns,
    }
