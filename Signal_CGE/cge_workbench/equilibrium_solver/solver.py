"""SciPy-backed static equilibrium CGE solver for Signal CGE."""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.optimize import least_squares, root

from .calibration import calibrate_static_cge
from .closures import normalize_closure
from .diagnostics import run_diagnostics, write_latest_diagnostics
from .equations import EQUATIONS, VARIABLES, build_variable_vector, equilibrium_residuals, unpack_variables
from .results import build_result_tables, save_outputs
from .shocks import normalize_shock


def solve_static_cge(
    sam: Any,
    shock: dict[str, Any] | None = None,
    closure: dict[str, Any] | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Calibrate, solve baseline, solve counterfactual, compare, and report."""

    options = options or {}
    calibration = calibrate_static_cge(sam, options.get("account_mapping"))
    closure_payload = normalize_closure(closure)
    baseline = solve_baseline(calibration, closure_payload, options)
    if not baseline["success"]:
        diagnostics = run_diagnostics(calibration, baseline, options.get("tolerance", 1e-6))
        write_latest_diagnostics(diagnostics)
        return {
            "success": False,
            "solver_name": baseline["solver_name"],
            "message": "Baseline equilibrium failed convergence diagnostics.",
            "baseline": baseline,
            "counterfactual": {},
            "percentage_changes": {},
            "diagnostics": diagnostics,
        }
    counterfactual = solve_counterfactual(calibration, normalize_shock(shock), closure_payload, baseline["x"], options)
    result = compare_results(baseline, counterfactual)
    result.update(
        {
            "success": bool(counterfactual["success"]),
            "solver_name": counterfactual["solver_name"],
            "message": (
                "Signal Static CGE Solver active: results are generated from the open-source equilibrium solver using calibrated benchmark equations and the selected macro closure."
                if counterfactual["success"]
                else "Static equilibrium solve did not pass convergence diagnostics."
            ),
            "shock": normalize_shock(shock),
            "closure": closure_payload,
            "calibration": {key: value for key, value in calibration.items() if key != "sam"},
            "residual_norm": counterfactual["residual_norm"],
            "max_abs_residual": counterfactual["max_abs_residual"],
            "iterations": counterfactual.get("iterations"),
        }
    )
    diagnostics = run_diagnostics(calibration, counterfactual, options.get("tolerance", 1e-6))
    result["diagnostics"] = diagnostics
    result["tables"] = build_result_tables(result)
    result["downloads"] = save_outputs(result)
    write_latest_diagnostics(diagnostics)
    return result


def solve_baseline(calibration: dict[str, Any], closure: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
    """Solve the calibrated benchmark equilibrium."""

    return _solve(calibration, None, normalize_closure(closure), options or {})


def solve_counterfactual(
    calibration: dict[str, Any],
    shock: dict[str, Any],
    closure: dict[str, Any] | None = None,
    initial_x: np.ndarray | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Solve a counterfactual equilibrium after applying a shock."""

    return _solve(calibration, normalize_shock(shock), normalize_closure(closure), options or {}, initial_x=initial_x)


def compare_results(baseline: dict[str, Any], counterfactual: dict[str, Any]) -> dict[str, Any]:
    """Compare baseline and counterfactual solved values."""

    base = baseline.get("values", {})
    policy = counterfactual.get("values", {})
    changes = {}
    for key, base_value in base.items():
        policy_value = float(policy.get(key, base_value))
        changes[key] = _pct(policy_value, float(base_value))
    return {
        "baseline": baseline,
        "counterfactual": counterfactual,
        "percentage_changes": changes,
    }


def _solve(
    calibration: dict[str, Any],
    shock: dict[str, Any] | None,
    closure: dict[str, Any],
    options: dict[str, Any],
    initial_x: np.ndarray | None = None,
) -> dict[str, Any]:
    tolerance = float(options.get("tolerance", 1e-6))
    x0 = initial_x if initial_x is not None else build_variable_vector(calibration)
    attempts = [
        ("scipy.root.hybr", lambda: root(lambda x: equilibrium_residuals(x, calibration, shock, closure), x0, method="hybr")),
        ("scipy.root.lm", lambda: root(lambda x: equilibrium_residuals(x, calibration, shock, closure), x0, method="lm")),
        (
            "scipy.least_squares",
            lambda: least_squares(
                lambda x: equilibrium_residuals(x, calibration, shock, closure),
                x0,
                xtol=1e-12,
                ftol=1e-12,
                gtol=1e-12,
                max_nfev=int(options.get("max_nfev", 5000)),
            ),
        ),
    ]
    best: dict[str, Any] | None = None
    for solver_name, solve in attempts:
        raw = solve()
        x = np.array(raw.x, dtype=float)
        residual_vector = equilibrium_residuals(x, calibration, shock, closure)
        residual_norm = float(np.linalg.norm(residual_vector))
        max_abs_residual = float(np.max(np.abs(residual_vector)))
        values = unpack_variables(x, calibration)
        success = bool(getattr(raw, "success", False) and residual_norm <= tolerance and max_abs_residual <= tolerance and _finite(values))
        candidate = {
            "success": success,
            "solver_name": solver_name,
            "message": str(getattr(raw, "message", "")),
            "residual_norm": residual_norm,
            "max_abs_residual": max_abs_residual,
            "iterations": int(getattr(raw, "nfev", 0)),
            "x": x,
            "values": values,
            "equation_residuals": {name: float(value) for name, value in zip(EQUATIONS, residual_vector, strict=False)},
            "variables": VARIABLES,
            "equations": EQUATIONS,
        }
        if success:
            return candidate
        if best is None or candidate["residual_norm"] < best["residual_norm"]:
            best = candidate
    return best or {"success": False, "solver_name": "not_run", "message": "No solver attempt completed."}


def _pct(policy: float, benchmark: float) -> float:
    if abs(benchmark) < 1e-12:
        return 0.0
    return round(((policy - benchmark) / abs(benchmark)) * 100.0, 8)


def _finite(values: dict[str, float]) -> bool:
    return all(np.isfinite(float(value)) for value in values.values())
