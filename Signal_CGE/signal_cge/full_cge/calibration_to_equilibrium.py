"""Bridge SAM calibration outputs into solver-ready Signal CGE dictionaries."""

from __future__ import annotations

from typing import Any

from .closure_manager import default_closure_payload
from .equation_registry import get_equation_registry
from .parameter_registry import get_parameter_registry
from .variable_registry import get_variable_registry


def build_solver_ready_payload(calibration_output: dict[str, Any], closure_name: str = "base_closure") -> dict[str, Any]:
    """Convert prototype calibration output into a future solver payload."""

    benchmark = calibration_output.get("benchmark_flows", {})
    shares = calibration_output.get("share_parameters", {})
    diagnostics = calibration_output.get("diagnostics", {})
    benchmark_variables = _flatten_numeric_dict(benchmark)
    benchmark_parameters = _flatten_numeric_dict(shares)
    return {
        "status": "solver_ready_blueprint",
        "benchmark_variables": benchmark_variables,
        "benchmark_parameters": benchmark_parameters,
        "initial_values": {key: value for key, value in benchmark_variables.items()},
        "equation_inputs": {
            "equations": get_equation_registry(),
            "variables": get_variable_registry(),
            "parameters": get_parameter_registry(),
        },
        "closure_settings": default_closure_payload(closure_name),
        "diagnostics": diagnostics,
        "warnings": [
            "Elasticities and nonlinear equation forms are placeholders.",
            "Payload is structured for a future full-equilibrium solver, not solved yet.",
        ],
    }


def _flatten_numeric_dict(payload: dict[str, Any], prefix: str = "") -> dict[str, float]:
    flat: dict[str, float] = {}
    for key, value in payload.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            flat.update(_flatten_numeric_dict(value, path))
        else:
            try:
                flat[path] = float(value)
            except (TypeError, ValueError):
                continue
    return flat
