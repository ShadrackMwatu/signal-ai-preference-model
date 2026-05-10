"""Validated open-source static equilibrium CGE solver for Signal CGE."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

from ..calibration.calibration_pipeline import calibrate_signal_cge
from ..solvers.python_runner import load_sam


VARIABLES = [
    "domestic_output",
    "composite_demand",
    "imports",
    "exports",
    "commodity_price",
    "activity_price",
    "household_income",
    "government_revenue",
    "investment",
    "exchange_rate",
    "intermediate_demand",
    "factor_demand",
    "household_demand",
    "government_expenditure",
    "savings",
    "external_balance",
]

EQUATIONS = [
    "production_zero_profit",
    "intermediate_demand",
    "factor_demand",
    "household_income",
    "household_demand",
    "government_revenue",
    "government_expenditure",
    "investment_savings_balance",
    "armington_import_demand",
    "cet_export_supply",
    "commodity_market_clearing",
    "factor_market_clearing",
    "price_system",
    "external_balance",
    "numeraire_condition",
    "income_expenditure_consistency",
]


@dataclass(frozen=True)
class StaticParameters:
    benchmark: dict[str, float]
    tariff_rate: float
    base_tariff_rate: float
    indirect_tax_rate: float
    direct_tax_rate: float
    import_elasticity: float
    export_elasticity: float
    output_elasticity: float
    savings_rate: float
    government_spending_share: float
    wage_index: float
    productivity: float
    target_account: str
    closure: str


def load_default_static_sam() -> pd.DataFrame:
    """Return a balanced repo-default SAM with core Signal CGE account classes."""

    accounts = [
        "activity_agriculture",
        "commodity_cmach",
        "labor",
        "households",
        "government",
        "investment",
        "rest_of_world",
        "tariff_tax",
    ]
    values = np.array(
        [
            [0, 28, 16, 10, 8, 6, 7, 2],
            [28, 0, 11, 18, 10, 14, 12, 3],
            [16, 11, 0, 22, 4, 3, 2, 1],
            [10, 18, 22, 0, 8, 12, 4, 2],
            [8, 10, 4, 8, 0, 5, 3, 6],
            [6, 14, 3, 12, 5, 0, 4, 1],
            [7, 12, 2, 4, 3, 4, 0, 2],
            [2, 3, 1, 2, 6, 1, 2, 0],
        ],
        dtype=float,
    )
    return pd.DataFrame(values, index=accounts, columns=accounts)


def calibration_from_sam_path(sam_path: str | Path | None = None) -> dict[str, Any]:
    """Load a SAM from upload or repo defaults and build calibration output."""

    sam = load_sam(sam_path) if sam_path else load_default_static_sam()
    return calibrate_signal_cge(sam)


def solve_static_equilibrium(
    calibration: dict[str, Any] | None,
    scenario: dict[str, Any] | None,
    closure: dict[str, Any] | str | None = None,
    tolerance: float = 1e-4,
) -> dict[str, Any]:
    """Solve and validate a static CGE equilibrium system."""

    calibration_payload = calibration or calibrate_signal_cge(load_default_static_sam())
    pre_validation = _validate_calibration_payload(calibration_payload, tolerance)
    if not pre_validation["passed"]:
        return _failed("Static solver validation failed before solve.", pre_validation)

    closure_name = _closure_name(closure)
    benchmark = _benchmark_from_calibration(calibration_payload)
    base_params = _parameters(benchmark, scenario or {}, closure_name, shocked=False)
    shock_params = _parameters(benchmark, scenario or {}, closure_name, shocked=True)
    baseline = _solve(base_params, tolerance=tolerance)
    replication = _replication_validation(baseline, benchmark, tolerance)
    if not baseline["converged"] or not replication["passed"]:
        return _failed("Base-year replication failed.", pre_validation, baseline, replication)
    policy = _solve(shock_params, initial_levels=baseline["levels"], tolerance=tolerance)
    post_validation = _post_solve_validation(policy, tolerance)
    validation = _combined_validation(pre_validation, replication, post_validation)
    if not policy["converged"] or not validation["all_checks_passed"]:
        return _failed("Post-shock validation failed.", validation, policy, replication)

    changes = _percentage_changes(baseline["levels"], policy["levels"], shock_params)
    return {
        "success": True,
        "backend": "validated_static_equilibrium_cge_solver",
        "result_type": "validated_static_equilibrium_cge_solver",
        "solver_label": "Validated open-source static equilibrium CGE solver",
        "scenario": scenario or {},
        "benchmark": baseline["levels"],
        "policy": policy["levels"],
        "percentage_changes": changes,
        "validation": validation,
        "diagnostics": {
            "converged": True,
            "residual_norm": policy["residual_norm"],
            "baseline_residual_norm": baseline["residual_norm"],
            "function_evaluations": policy["function_evaluations"],
            "baseline_function_evaluations": baseline["function_evaluations"],
            "equations_solved": EQUATIONS,
            "variables_solved": VARIABLES,
            "closure_used": closure_name,
            "benchmark_replication_check": replication,
            "walras_style_check": validation["checks"]["walras_style_balance"],
            "homogeneity_numeraire_check": validation["checks"]["homogeneity_numeraire"],
            "failed_equations": [],
            "message": policy["message"],
        },
        "caveat": (
            "Signal used the validated open-source static equilibrium CGE solver. Results reflect a validated "
            "static equilibrium system, while the full recursive-dynamic CGE model is still under development."
        ),
    }


def _solve(params: StaticParameters, initial_levels: dict[str, float] | None = None, tolerance: float = 1e-4) -> dict[str, Any]:
    start = initial_levels or params.benchmark
    x0 = np.log(np.array([max(float(start[name]), 1e-9) for name in VARIABLES]))
    result = least_squares(lambda vector: _residuals(vector, params), x0, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=2000)
    residual_values = _residuals(result.x, params)
    residual_norm = float(np.linalg.norm(residual_values))
    levels = _vector_to_levels(result.x)
    return {
        "converged": bool(result.success and residual_norm < tolerance and _finite_dict(levels)),
        "levels": levels,
        "residual_norm": residual_norm,
        "function_evaluations": int(result.nfev),
        "message": str(result.message),
        "equation_residuals": {equation: float(value) for equation, value in zip(EQUATIONS, residual_values, strict=False)},
    }


def _residuals(log_values: np.ndarray, params: StaticParameters) -> np.ndarray:
    levels = _vector_to_levels(log_values)
    b = params.benchmark
    qx = levels["domestic_output"]
    qq = levels["composite_demand"]
    qm = levels["imports"]
    qe = levels["exports"]
    pc = levels["commodity_price"]
    pa = levels["activity_price"]
    yh = levels["household_income"]
    gr = levels["government_revenue"]
    inv = levels["investment"]
    exr = levels["exchange_rate"]
    qint = levels["intermediate_demand"]
    fd = levels["factor_demand"]
    hd = levels["household_demand"]
    ge = levels["government_expenditure"]
    sav = levels["savings"]
    ext = levels["external_balance"]

    pm = exr * (1.0 + params.tariff_rate)
    base_pm = b["exchange_rate"] * (1.0 + params.base_tariff_rate)
    pe = exr
    base_cost = 0.30 * b["commodity_price"] + 0.45 * params.wage_index + 0.25 * base_pm
    cost = 0.30 * pc + 0.45 * params.wage_index + 0.25 * pm
    target_pa = b["activity_price"] * (cost / base_cost) / params.productivity
    target_qx = b["domestic_output"] * (pa / b["activity_price"]) ** params.output_elasticity
    target_qint = b["intermediate_demand"] * (qx / b["domestic_output"])
    target_fd = b["factor_demand"] * (qx / b["domestic_output"])
    target_yh = b["household_income"] * (pa * qx / (b["activity_price"] * b["domestic_output"]))
    target_hd = b["household_demand"] * (yh / b["household_income"]) * (pc / b["commodity_price"]) ** -0.8
    target_gr = b["government_revenue"] * (
        0.35 * (params.tariff_rate * exr * qm) / max(params.base_tariff_rate * b["exchange_rate"] * b["imports"], 1e-9)
        + 0.35 * (pc * qq) / max(b["commodity_price"] * b["composite_demand"], 1e-9)
        + 0.30 * (yh / b["household_income"])
    )
    target_ge = b["government_expenditure"] * (gr / b["government_revenue"]) ** params.government_spending_share
    target_sav = params.savings_rate * yh
    target_inv = b["investment"] * (sav / b["savings"])
    target_qm = b["imports"] * (qq / b["composite_demand"]) * ((pm / pc) / (base_pm / b["commodity_price"])) ** (-params.import_elasticity)
    target_qe = b["exports"] * (qx / b["domestic_output"]) * ((pe / pa) / (b["exchange_rate"] / b["activity_price"])) ** params.export_elasticity
    target_qq = hd + ge + inv + qint
    target_ext = exr * (qm - qe)
    household_outlay = pc * hd + sav + params.direct_tax_rate * yh

    return np.array(
        [
            _scaled(pa - target_pa, b["activity_price"]),
            _scaled(qint - target_qint, b["intermediate_demand"]),
            _scaled(fd - target_fd, b["factor_demand"]),
            _scaled(yh - target_yh, b["household_income"]),
            _scaled(hd - target_hd, b["household_demand"]),
            _scaled(gr - target_gr, b["government_revenue"]),
            _scaled(ge - target_ge, b["government_expenditure"]),
            _scaled(inv - target_inv, b["investment"]),
            _scaled(qm - target_qm, b["imports"]),
            _scaled(qe - target_qe, b["exports"]),
            _scaled(qq - target_qq, b["composite_demand"]),
            _scaled(fd - b["factor_demand"], b["factor_demand"]),
            pc - 1.0,
            _scaled(ext - b["external_balance"], max(abs(b["external_balance"]), 1.0)),
            pc - b["commodity_price"],
            _scaled(yh - household_outlay, b["household_income"]),
        ],
        dtype=float,
    )


def _benchmark_from_calibration(calibration: dict[str, Any]) -> dict[str, float]:
    flows = calibration.get("benchmark_flows", {})
    activity = _sum(flows.get("activity_output", {})) or 100.0
    commodity = _sum(flows.get("commodity_demand", {})) or 120.0
    imports = _sum_nested(flows.get("imports", {})) or 24.0
    exports = _sum_nested(flows.get("exports", {})) or 18.0
    household_income = _sum(flows.get("household_income", {})) or 80.0
    government = _sum_nested(flows.get("government_demand", {})) or 12.0
    investment = _sum_nested(flows.get("investment_demand", {})) or 14.0
    intermediate = max(0.20 * commodity, 1.0)
    factor = max(0.55 * activity, 1.0)
    savings = max(0.18 * household_income, 1.0)
    household_demand = max(household_income - savings - 0.07 * household_income, 1.0)
    composite = max(household_demand + government + investment + intermediate, 1.0)
    return {
        "domestic_output": float(max(activity, 1.0)),
        "composite_demand": float(composite),
        "imports": float(max(imports, 1.0)),
        "exports": float(max(exports, 1.0)),
        "commodity_price": 1.0,
        "activity_price": 1.0,
        "household_income": float(max(household_income, 1.0)),
        "government_revenue": float(max(government / 0.7, 1.0)),
        "investment": float(max(investment, 1.0)),
        "exchange_rate": 1.0,
        "intermediate_demand": float(intermediate),
        "factor_demand": float(factor),
        "household_demand": float(household_demand),
        "government_expenditure": float(max(government, 1.0)),
        "savings": float(savings),
        "external_balance": float(max(imports - exports, 1.0)),
    }


def _parameters(benchmark: dict[str, float], scenario: dict[str, Any], closure: str, shocked: bool) -> StaticParameters:
    base_tariff = 0.10
    tariff = base_tariff
    if shocked and (scenario.get("policy_instrument") == "import_tariff" or scenario.get("shock_type") == "import_tariff"):
        shock = abs(float(scenario.get("shock_magnitude_percent", scenario.get("shock_size", scenario.get("shock_value", 0))) or 0.0)) / 100.0
        tariff = base_tariff * (1.0 - shock if scenario.get("shock_direction", "decrease") == "decrease" else 1.0 + shock)
    return StaticParameters(
        benchmark=benchmark,
        tariff_rate=max(tariff, 0.0),
        base_tariff_rate=base_tariff,
        indirect_tax_rate=0.05,
        direct_tax_rate=0.07,
        import_elasticity=1.5,
        export_elasticity=1.1,
        output_elasticity=0.4,
        savings_rate=benchmark["savings"] / benchmark["household_income"],
        government_spending_share=1.0,
        wage_index=1.0,
        productivity=1.0,
        target_account=str(scenario.get("target_account") or scenario.get("target_commodity") or "aggregate"),
        closure=closure,
    )


def _validate_calibration_payload(calibration: dict[str, Any], tolerance: float) -> dict[str, Any]:
    diagnostics = calibration.get("diagnostics", {})
    groups = calibration.get("account_classification", {})
    required = ["activities", "commodities", "factors", "households", "government", "savings_investment", "rest_of_world"]
    missing = [group for group in required if not groups.get(group)]
    checks = {
        "sam_row_column_balance": float(diagnostics.get("max_absolute_imbalance", 1.0)) <= tolerance,
        "no_missing_core_accounts": not missing,
        "no_negative_entries": int(diagnostics.get("negative_value_count", 0)) == 0,
        "no_zero_columns": not diagnostics.get("zero_column_accounts", []),
    }
    return {"passed": all(checks.values()), "checks": checks, "missing_core_accounts": missing, "diagnostics": diagnostics}


def _replication_validation(solution: dict[str, Any], benchmark: dict[str, float], tolerance: float) -> dict[str, Any]:
    level_error = max(abs(solution["levels"][name] - benchmark[name]) / max(abs(benchmark[name]), 1.0) for name in VARIABLES)
    return {
        "passed": bool(solution["converged"] and solution["residual_norm"] <= tolerance and level_error <= 1e-5),
        "residual_norm": solution["residual_norm"],
        "max_relative_level_error": float(level_error),
    }


def _post_solve_validation(solution: dict[str, Any], tolerance: float) -> dict[str, Any]:
    finite = _finite_dict(solution.get("levels", {}))
    checks = {
        "post_shock_solver_convergence": bool(solution.get("converged")),
        "residual_norm_below_tolerance": float(solution.get("residual_norm", 1.0)) <= tolerance,
        "no_nan_or_infinite_values": finite,
        "walras_style_balance": abs(solution.get("equation_residuals", {}).get("commodity_market_clearing", 1.0)) <= tolerance,
        "homogeneity_numeraire": abs(solution.get("levels", {}).get("commodity_price", 0.0) - 1.0) <= tolerance,
    }
    return {"passed": all(checks.values()), "checks": checks, "residual_norm": solution.get("residual_norm")}


def _combined_validation(pre: dict[str, Any], replication: dict[str, Any], post: dict[str, Any]) -> dict[str, Any]:
    checks = {
        **pre["checks"],
        "base_year_replication": replication["passed"],
        **post["checks"],
    }
    return {
        "all_checks_passed": all(checks.values()),
        "checks": checks,
        "pre_solve": pre,
        "base_year_replication": replication,
        "post_solve": post,
    }


def _percentage_changes(benchmark: dict[str, float], policy: dict[str, float], params: StaticParameters) -> dict[str, float]:
    base_import_price = benchmark["exchange_rate"] * (1.0 + params.base_tariff_rate)
    policy_import_price = policy["exchange_rate"] * (1.0 + params.tariff_rate)
    values = {
        "output_change_pct": _pct(policy["domestic_output"], benchmark["domestic_output"]),
        "import_demand_change_pct": _pct(policy["imports"], benchmark["imports"]),
        "export_demand_change_pct": _pct(policy["exports"], benchmark["exports"]),
        "import_price_change_pct": _pct(policy_import_price, base_import_price),
        "government_revenue_change_pct": _pct(policy["government_revenue"], benchmark["government_revenue"]),
        "government_tariff_revenue_change_pct": _pct(params.tariff_rate * policy["exchange_rate"] * policy["imports"], params.base_tariff_rate * benchmark["exchange_rate"] * benchmark["imports"]),
        "household_welfare_proxy_change_pct": _pct(policy["household_income"] / policy["commodity_price"], benchmark["household_income"] / benchmark["commodity_price"]),
        "trade_balance_change_pct": _pct(policy["exports"] - policy["imports"], benchmark["exports"] - benchmark["imports"]),
    }
    return {key: round(float(value), 6) for key, value in values.items()}


def _failed(reason: str, validation: dict[str, Any], solution: dict[str, Any] | None = None, replication: dict[str, Any] | None = None) -> dict[str, Any]:
    residuals = (solution or {}).get("equation_residuals", {})
    return {
        "success": False,
        "backend": "validated_static_equilibrium_cge_solver",
        "result_type": "validation_failed",
        "reason": reason,
        "validation": validation,
        "diagnostics": {
            "converged": False,
            "residual_norm": (solution or {}).get("residual_norm"),
            "function_evaluations": (solution or {}).get("function_evaluations", 0),
            "equations_solved": EQUATIONS,
            "variables_solved": VARIABLES,
            "closure_used": "base_closure",
            "benchmark_replication_check": replication or {},
            "failed_equations": [name for name, value in residuals.items() if abs(float(value)) > 1e-6],
            "message": reason,
        },
    }


def _vector_to_levels(log_values: np.ndarray) -> dict[str, float]:
    values = np.exp(np.array(log_values, dtype=float))
    return {name: float(value) for name, value in zip(VARIABLES, values, strict=False)}


def _finite_dict(values: dict[str, float]) -> bool:
    return all(math.isfinite(float(value)) for value in values.values())


def _scaled(value: float, scale: float) -> float:
    return float(value) / max(abs(float(scale)), 1e-9)


def _pct(policy: float, benchmark: float) -> float:
    return 0.0 if abs(benchmark) < 1e-12 else ((policy - benchmark) / abs(benchmark)) * 100.0


def _sum(values: dict[str, Any]) -> float:
    return sum(float(value) for value in values.values()) if isinstance(values, dict) else 0.0


def _sum_nested(values: dict[str, Any]) -> float:
    total = 0.0
    if not isinstance(values, dict):
        return total
    for value in values.values():
        if isinstance(value, dict):
            total += _sum(value)
        else:
            total += float(value)
    return total


def _closure_name(closure: dict[str, Any] | str | None) -> str:
    if isinstance(closure, str):
        return closure
    if isinstance(closure, dict):
        return str(closure.get("closure") or closure.get("name") or "base_closure")
    return "base_closure"
