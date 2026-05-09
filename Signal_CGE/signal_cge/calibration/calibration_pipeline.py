"""End-to-end calibration pipeline for the Signal CGE prototype."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .account_classifier import classify_sam_accounts
from .benchmark_extractor import extract_benchmark_flows, validate_sam_matrix
from .calibration_diagnostics import run_calibration_diagnostics
from .share_parameters import calibrate_share_parameters


def calibrate_signal_cge(
    sam_df: pd.DataFrame,
    account_map: dict[str, str] | None = None,
    tolerance: float = 1e-6,
) -> dict[str, Any]:
    """Prepare a SAM for future full Signal CGE equilibrium solving."""

    matrix = validate_sam_matrix(sam_df)
    account_classification = classify_sam_accounts(matrix, account_map=account_map)
    benchmark_flows = extract_benchmark_flows(matrix, account_classification)
    share_parameters = calibrate_share_parameters(matrix, account_classification)
    diagnostics = run_calibration_diagnostics(matrix, account_classification, tolerance=tolerance)
    warnings = diagnostics.get("warnings", [])
    return {
        "account_classification": account_classification,
        "benchmark_flows": benchmark_flows,
        "share_parameters": share_parameters,
        "diagnostics": diagnostics,
        "warnings": warnings,
        "cge_readiness_status": diagnostics["readiness"],
    }
