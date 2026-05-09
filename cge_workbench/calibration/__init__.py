"""Compatibility wrapper for `signal_cge.calibration`."""

from signal_cge.calibration import (
    CARE_SUFFIXES,
    calibrate_share_parameters,
    calibrate_signal_cge,
    classify_sam_accounts,
    extract_benchmark_flows,
    run_calibration_diagnostics,
    validate_sam_matrix,
)

build_calibration_dataset = calibrate_signal_cge

__all__ = [
    "CARE_SUFFIXES",
    "calibrate_share_parameters",
    "calibrate_signal_cge",
    "classify_sam_accounts",
    "extract_benchmark_flows",
    "run_calibration_diagnostics",
    "validate_sam_matrix",
    "build_calibration_dataset",
]
