"""Canonical solver orchestration service for Signal CGE."""

from __future__ import annotations

from typing import Any

from Signal_CGE.signal_cge.solvers.gams_runner import GAMSRunner
from Signal_CGE.signal_cge.solvers.python_runner import PythonSAMRunner
from Signal_CGE.signal_cge.solvers.runner_interface import RunnerConfig


DEFAULT_BACKEND = "python_sam_multiplier"


def run_solver(
    scenario: dict[str, Any],
    backend: str = DEFAULT_BACKEND,
    sam_path: str | None = None,
    model_path: str | None = None,
) -> dict[str, Any]:
    """Run the requested Signal CGE backend with safe fallback."""

    backend = (backend or DEFAULT_BACKEND).lower()
    config = RunnerConfig(model_type="Signal CGE", sam_path=sam_path, model_path=model_path)

    if "gams" in backend:
        result = GAMSRunner(config).run(scenario)
        if result.success:
            return {
                "backend": "gams_optional_solver",
                "success": True,
                "results": result.results,
                "diagnostics": result.diagnostics,
                "artifacts": result.artifacts,
            }

    fallback = PythonSAMRunner(config).run(scenario)
    return {
        "backend": "python_sam_multiplier",
        "success": fallback.success,
        "results": fallback.results,
        "diagnostics": fallback.diagnostics,
        "artifacts": fallback.artifacts,
    }
