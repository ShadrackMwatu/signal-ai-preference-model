"""Connect the active Signal CGE SAM to calibration and solver payloads."""

from __future__ import annotations

from typing import Any

from ..data.sam_loader import load_default_signal_sam, validate_signal_sam
from .calibration_pipeline import calibrate_signal_cge


def calibrate_active_signal_sam(account_map: dict[str, str] | None = None) -> dict[str, Any]:
    """Calibrate the active KEN SAM when available, returning warnings otherwise."""

    diagnostics = validate_signal_sam()
    if not diagnostics["sam_loaded"]:
        return {
            "status": "sam_unavailable",
            "diagnostics": diagnostics,
            "warnings": diagnostics.get("warnings", []),
            "calibration": {},
        }
    sam = load_default_signal_sam()
    calibration = calibrate_signal_cge(sam, account_map=account_map)
    return {
        "status": "calibrated",
        "diagnostics": diagnostics,
        "warnings": calibration.get("warnings", []),
        "calibration": calibration,
        "benchmark_flows": calibration.get("benchmark_flows", {}),
        "share_parameters": calibration.get("share_parameters", {}),
        "account_classification": calibration.get("account_classification", {}),
    }
