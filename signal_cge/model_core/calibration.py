"""Calibration helpers for building a CGE benchmark dataset from a SAM."""

from __future__ import annotations

from typing import Any

import pandas as pd

from signal_cge.calibration.calibration_pipeline import calibrate_signal_cge


def calibrate_from_sam(sam: pd.DataFrame) -> dict[str, Any]:
    """Build a deterministic benchmark calibration summary from a SAM-like matrix.

    This function is retained as the model-core entry point and delegates to
    the open-source calibration pipeline to avoid duplicated calibration logic.
    """

    dataset = calibrate_signal_cge(sam)
    classification = dataset["account_classification"]
    flows = dataset["benchmark_flows"]
    row_totals = flows["row_totals"]
    column_totals = flows["column_totals"]
    return {
        "accounts": list(row_totals),
        "activities": classification["activities"],
        "commodities": classification["commodities"],
        "factors": classification["factors"],
        "households": classification["households"],
        "government": classification["government"],
        "row_totals": row_totals,
        "column_totals": column_totals,
        "total_flow": float(sum(row_totals.values())),
        "share_parameters": dataset["share_parameters"],
        "kenya_gender_care_supported": len(classification["care_factors"]) == 8,
        "diagnostics": dataset["diagnostics"],
        "calibration_dataset": dataset,
    }
