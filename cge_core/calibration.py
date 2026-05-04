"""Calibration utilities derived from SAM data."""

from __future__ import annotations

import pandas as pd

from .accounts import classify_accounts


def calibrate_from_sam(matrix: pd.DataFrame) -> dict[str, object]:
    """Calibrate output, expenditure, and income shares from a SAM matrix."""

    sam = matrix.astype(float)
    classifications = classify_accounts(sam)
    row_totals = sam.sum(axis=1)
    column_totals = sam.sum(axis=0).reindex(sam.index)
    total_activity = float(row_totals.sum())
    if total_activity <= 0:
        raise ValueError("SAM total activity must be positive for calibration")

    output_shares = (row_totals / total_activity).round(6).to_dict()
    expenditure_shares = {
        account: (sam.loc[account] / row_totals[account]).fillna(0).round(6).to_dict()
        for account in sam.index
    }
    return {
        "total_activity": total_activity,
        "row_totals": row_totals.round(6).to_dict(),
        "column_totals": column_totals.round(6).to_dict(),
        "output_shares": output_shares,
        "expenditure_shares": expenditure_shares,
        "account_classification": classifications,
    }
