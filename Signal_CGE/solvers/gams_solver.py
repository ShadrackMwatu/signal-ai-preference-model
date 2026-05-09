"""GAMS execution backend for Signal."""

from __future__ import annotations

from typing import Any

from backends.gams.gams_runner import GAMS_UNAVAILABLE_MESSAGE, run_gams

from .base_solver import BaseSolver
from .python_nlp_solver import PythonNLPSolver


class GamsSolver(BaseSolver):
    name = "gams"
    production_grade = True

    def solve(self, model_spec: Any, data: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        options = options or {}
        gms_path = options.get("gms_path")
        if not gms_path:
            return {"status": "validation_only", "backend": self.name, "message": "No GMS path supplied."}
        gams_result = run_gams(gms_path, options.get("workdir", "outputs"))
        if gams_result["status"] == "unavailable":
            fallback = PythonNLPSolver().solve(model_spec, data, options)
            fallback["message"] = f"{GAMS_UNAVAILABLE_MESSAGE} {fallback['message']}"
            fallback["requested_backend"] = self.name
            return fallback
        return {
            "status": gams_result["status"],
            "backend": self.name,
            "message": gams_result["message"],
            "metrics": data.get("baseline_metrics", {}),
            "gams": gams_result,
        }
