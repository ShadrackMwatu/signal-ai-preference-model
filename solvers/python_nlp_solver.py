"""Experimental Python nonlinear solver backend."""

from __future__ import annotations

from typing import Any

from .base_solver import BaseSolver
from .fixed_point_solver import FixedPointSolver


class PythonNLPSolver(BaseSolver):
    name = "python_nlp"
    production_grade = False

    def solve(self, model_spec: Any, data: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        shock_size = float(data.get("shock_size", 0.0))
        try:
            from scipy.optimize import minimize
        except Exception:
            result = FixedPointSolver().solve(model_spec, data, options)
            result["message"] = "SciPy unavailable; used experimental fixed-point fallback."
            return result

        objective = lambda x: (x[0] - (1 + shock_size)) ** 2
        solution = minimize(objective, x0=[1.0], method="Nelder-Mead")
        value = float(solution.x[0])
        return {
            "status": "ok" if solution.success else "failed",
            "backend": self.name,
            "message": "Experimental Python NLP backend; not production-grade.",
            "metrics": {
                "gdp_impact": round((value - 1) * 100, 4),
                "household_welfare_impact": round((value - 1) * 62, 4),
                "sectoral_output_impact": round((value - 1) * 100, 4),
                "employment_factor_income_impact": round((value - 1) * 50, 4),
                "government_revenue_impact": round(shock_size * 16, 4),
                "trade_impact": round(shock_size * 7, 4),
                "distributional_impact": round((value - 1) * 18, 4),
            },
        }
