"""Model readiness dashboard for Signal CGE."""

from __future__ import annotations

from typing import Any


def get_model_readiness(calibration_result: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return readiness status for each Signal CGE layer."""

    calibration_ready = "partial"
    if calibration_result:
        readiness = calibration_result.get("cge_readiness_status", {})
        calibration_ready = "ready" if readiness.get("prototype_cge_calibration", "").startswith("ready") else "partial"
    return {
        "sam_multiplier_readiness": "ready",
        "calibration_readiness": calibration_ready,
        "prototype_cge_readiness": "partial",
        "full_cge_solver_readiness": "placeholder",
        "recursive_dynamic_readiness": "placeholder",
        "available_statuses": ["ready", "partial", "placeholder", "unavailable"],
    }
