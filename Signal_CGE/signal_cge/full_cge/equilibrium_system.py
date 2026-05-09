"""Solver-neutral equilibrium system assembly for Signal CGE."""

from __future__ import annotations

from typing import Any

from .closure_manager import default_closure_payload
from .equation_registry import get_equation_registry, validate_equation_registry
from .parameter_registry import get_parameter_registry
from .variable_registry import get_variable_registry


def build_equilibrium_system(calibration_payload: dict[str, Any] | None = None, closure_name: str = "base_closure") -> dict[str, Any]:
    """Assemble a solver-neutral full-CGE system blueprint."""

    equations = get_equation_registry()
    return {
        "status": "solver_blueprint",
        "equations": equations,
        "variables": get_variable_registry(),
        "parameters": get_parameter_registry(),
        "closure": default_closure_payload(closure_name),
        "calibration_payload": calibration_payload or {},
        "validation": validate_equation_registry(equations),
    }


def validate_before_solving(system: dict[str, Any]) -> dict[str, Any]:
    """Run deterministic pre-solve checks that do not require a numerical solver."""

    calibration = system.get("calibration_payload", {})
    diagnostics = calibration.get("diagnostics", {}) if isinstance(calibration, dict) else {}
    warnings = []
    if diagnostics.get("negative_accounts"):
        warnings.append("SAM contains negative entries.")
    if diagnostics.get("zero_row_accounts") or diagnostics.get("zero_column_accounts"):
        warnings.append("SAM contains zero rows or columns.")
    if not system.get("closure", {}).get("validation", {}).get("valid", False):
        warnings.append("Closure is not fully valid.")
    warnings.extend(
        [
            "Walras-style balance check is a placeholder until full equations are solved.",
            "Homogeneity and numeraire checks are placeholders until price equations are active.",
            "Base-year replication check requires a numerical equilibrium solver.",
        ]
    )
    return {"ready_for_numerical_solver": False, "warnings": warnings}
