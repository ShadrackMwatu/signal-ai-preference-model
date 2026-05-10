"""Model readiness dashboard for Signal CGE."""

from __future__ import annotations

from typing import Any

from signal_cge.data.sam_loader import get_sam_status
from signal_cge.solvers.gams_runner import get_gams_status
from signal_cge.solvers.solver_registry import get_solver_registry


def get_model_readiness(calibration_result: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return readiness status for each Signal CGE layer."""

    calibration_ready = "partial"
    if calibration_result:
        readiness = calibration_result.get("cge_readiness_status", {})
        calibration_ready = "ready" if readiness.get("prototype_cge_calibration", "").startswith("ready") else "partial"

    sam_status = get_sam_status()
    gams_status = get_gams_status()

    return {
        "sam_multiplier_readiness": "ready",
        "calibration_readiness": calibration_ready,
        "prototype_cge_readiness": "partial",
        "full_cge_solver_readiness": "partial",
        "recursive_dynamic_readiness": "placeholder",
        "sam_status": sam_status,
        "gams_status": gams_status,
        "solver_registry": get_solver_registry(),
        "validation_checks": {
            "sam_found": sam_status.get("found", False),
            "sam_square": sam_status.get("square", False),
            "sam_balanced": sam_status.get("balanced", False),
            "zero_column_accounts_detected": bool(sam_status.get("zero_column_accounts", [])),
            "gams_available": gams_status.get("available", False),
        },
        "available_statuses": ["ready", "partial", "placeholder", "unavailable"],
    }
