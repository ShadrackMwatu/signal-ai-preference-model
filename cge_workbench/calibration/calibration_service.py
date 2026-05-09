"""High-level calibration service for the open-source Signal CGE prototype."""

from __future__ import annotations

from typing import Any

import pandas as pd

from cge_workbench.model_core.calibration import calibrate_from_sam

from .account_classifier import classify_sam_accounts
from .benchmark_flows import extract_benchmark_flows
from .calibration_diagnostics import run_calibration_diagnostics
from .share_parameters import calibrate_share_parameters


def build_calibration_dataset(sam: pd.DataFrame) -> dict[str, Any]:
    """Return a structured calibration dataset from a SAM-like DataFrame."""

    matrix = _normalize_sam(sam)
    classification = classify_sam_accounts(matrix)
    benchmark_flows = extract_benchmark_flows(matrix, classification)
    share_parameters = calibrate_share_parameters(matrix, classification)
    diagnostics = run_calibration_diagnostics(matrix, classification)
    core_summary = calibrate_from_sam(matrix)
    return {
        "model": "Signal CGE Model",
        "status": "calibration_prototype",
        "classification": classification.to_dict(),
        "benchmark_flows": benchmark_flows,
        "share_parameters": share_parameters,
        "diagnostics": diagnostics,
        "model_core_summary": core_summary,
    }


def _normalize_sam(sam: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(sam, pd.DataFrame):
        raise TypeError("Calibration requires a pandas DataFrame.")
    if sam.empty:
        raise ValueError("Calibration requires a non-empty SAM.")
    matrix = sam.copy()
    matrix.index = [str(account) for account in matrix.index]
    matrix.columns = [str(account) for account in matrix.columns]
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Calibration requires a square SAM.")
    if set(matrix.index) != set(matrix.columns):
        raise ValueError("Calibration requires matching row and column accounts.")
    return matrix.apply(pd.to_numeric, errors="raise").astype(float)
