"""Experimental fixed-point fallback solver."""

from __future__ import annotations

from typing import Any

from .base_solver import BaseSolver


class FixedPointSolver(BaseSolver):
    name = "fixed_point"
    production_grade = False

    def solve(self, model_spec: Any, data: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        options = options or {}
        shock_size = float(data.get("shock_size", 0.0))
        value = 1.0
        iterations = int(options.get("iterations", 25))
        for _ in range(iterations):
            value = 0.7 * value + 0.3 * (1 + shock_size)
        return {
            "status": "ok",
            "backend": self.name,
            "message": "Experimental fixed-point fallback completed; not production-grade.",
            "metrics": _metrics_from_value(value, shock_size),
        }


def _metrics_from_value(value: float, shock_size: float) -> dict[str, float]:
    return {
        "gdp_impact": round((value - 1) * 100, 4),
        "household_welfare_impact": round((value - 1) * 65, 4),
        "sectoral_output_impact": round((value - 1) * 100, 4),
        "employment_factor_income_impact": round((value - 1) * 55, 4),
        "government_revenue_impact": round(shock_size * 18, 4),
        "trade_impact": round(shock_size * 8, 4),
        "distributional_impact": round((value - 1) * 20, 4),
    }
