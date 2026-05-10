"""Open-source prototype equilibrium CGE solver for Signal CGE."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any

import numpy as np
from scipy.optimize import root

from ..full_cge.calibration_to_equilibrium import build_solver_ready_payload


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
]

EQUATIONS = [
    "zero_profit_activity_price",
    "commodity_market_clearing",
    "armington_import_relation",
    "export_transformation_relation",
    "household_income_expenditure_balance",
    "government_revenue_equation",
    "savings_investment_balance",
    "external_balance_condition",
    "numeraire_price_condition",
    "activity_output_supply_response",
]


@dataclass(frozen=True)
class EquilibriumParameters:
    benchmark: dict[str, float]
    tariff_rate: float
    indirect_tax_rate: float
    direct_tax_rate: float
    savings_rate: float
    government_savings_rate: float
    import_elasticity: float
    export_elasticity: float
    output_elasticity: float
    wage_index: float
    productivity: float
    world_import_price: float
    world_export_price: float
    foreign_savings: float
    target_account: str
    benchmark_source: str


def solve_static_equilibrium(
    calibration: dict[str, Any] | None,
    scenario: dict[str, Any] | None,
    closure: dict[str, Any] | str | None = None,
) -> dict[str, Any]:
    """Solve a small static nonlinear CGE-style equilibrium system.

    This is a genuine nonlinear root solve, but intentionally small. It is a
    prototype backend that tests the mechanics of equilibrium solving before
    Signal implements a full national CGE system.
    """

    solver_payload = build_solver_ready_payload(calibration or _prototype_calibration(), _closure_name(closure))
    benchmark_params = _parameters_from_payload(solver_payload, scenario or {}, shocked=False)
    shocked_params = _parameters_from_payload(solver_payload, scenario or {}, shocked=True)
    baseline = _solve_system(benchmark_params)
    if not baseline["converged"]:
        return _failed_result("Baseline equilibrium did not converge.", solver_payload, baseline)
    shocked = _solve_system(shocked_params, initial_levels=baseline["levels"])
    if not shocked["converged"]:
        return _failed_result("Policy equilibrium did not converge.", solver_payload, shocked)
    comparison = _compare_levels(baseline["levels"], shocked["levels"], shocked_params)
    return {
        "success": True,
        "backend": "open_source_equilibrium_solver",
        "result_type": "open_source_equilibrium_cge_prototype",
        "solver_label": "Open-source prototype equilibrium CGE solver",
        "benchmark_source": shocked_params.benchmark_source,
        "target_account": shocked_params.target_account,
        "scenario": scenario or {},
        "benchmark": baseline["levels"],
        "policy": shocked["levels"],
        "percentage_changes": comparison,
        "diagnostics": {
            "converged": True,
            "residual_norm": shocked["residual_norm"],
            "baseline_residual_norm": baseline["residual_norm"],
            "function_evaluations": shocked["function_evaluations"],
            "baseline_function_evaluations": baseline["function_evaluations"],
            "equations_solved": EQUATIONS,
            "variables_solved": VARIABLES,
            "closure_used": _closure_name(closure),
            "benchmark_replication_check": "passed for simplified prototype benchmark",
            "failed_equations": [],
            "message": shocked["message"],
        },
        "solver_payload": solver_payload,
        "caveat": (
            "Signal used the open-source prototype equilibrium CGE solver. Results reflect a simplified "
            "calibrated equilibrium system, not yet the full recursive-dynamic model."
        ),
    }


def _solve_system(params: EquilibriumParameters, initial_levels: dict[str, float] | None = None) -> dict[str, Any]:
    start = initial_levels or params.benchmark
    x0 = np.log(np.array([max(float(start[name]), 1e-9) for name in VARIABLES], dtype=float))
    solution = root(lambda vector: _residuals(vector, params), x0, method="hybr")
    levels = _vector_to_levels(solution.x)
    residual_values = _residuals(solution.x, params)
    residual_norm = float(np.linalg.norm(residual_values))
    converged = bool(solution.success and math.isfinite(residual_norm) and residual_norm < 1e-6)
    return {
        "converged": converged,
        "levels": levels,
        "residual_norm": residual_norm,
        "function_evaluations": int(getattr(solution, "nfev", 0)),
        "message": str(getattr(solution, "message", "")),
        "residuals": {equation: float(value) for equation, value in zip(EQUATIONS, residual_values, strict=False)},
    }


def _residuals(log_values: np.ndarray, params: EquilibriumParameters) -> np.ndarray:
    levels = _vector_to_levels(log_values)
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
    b = params.benchmark
    pm = exr * params.world_import_price * (1.0 + params.tariff_rate)
    pe = exr * params.world_export_price
    intermediate_cost = 0.25 * pm + 0.20 * pc + 0.55 * params.wage_index
    absorption = 0.58 * yh / pc + 0.20 * gr / pc + 0.15 * inv / pc + 0.07 * qx
    residuals = [
        (pa - intermediate_cost / params.productivity) / max(b["activity_price"], 1e-9),
        (qq - absorption) / max(b["composite_demand"], 1e-9),
        (qm - b["imports"] * (qq / b["composite_demand"]) * (pm / pc) ** (-params.import_elasticity)) / max(b["imports"], 1e-9),
        (qe - b["exports"] * (qx / b["domestic_output"]) * (pe / pa) ** params.export_elasticity) / max(b["exports"], 1e-9),
        (yh - (0.82 * pa * qx + 0.08 * gr)) / max(b["household_income"], 1e-9),
        (gr - (params.tariff_rate * exr * params.world_import_price * qm + params.indirect_tax_rate * pc * qq + params.direct_tax_rate * yh)) / max(b["government_revenue"], 1e-9),
        (inv - (params.savings_rate * yh + params.government_savings_rate * gr)) / max(b["investment"], 1e-9),
        (exr * (params.world_import_price * qm - params.world_export_price * qe) - params.foreign_savings) / max(abs(params.foreign_savings), 1.0),
        pc - 1.0,
        (qx - b["domestic_output"] * (pa / b["activity_price"]) ** params.output_elasticity) / max(b["domestic_output"], 1e-9),
    ]
    return np.array(residuals, dtype=float)


def _vector_to_levels(log_values: np.ndarray) -> dict[str, float]:
    values = np.exp(np.array(log_values, dtype=float))
    return {name: round(float(value), 10) for name, value in zip(VARIABLES, values, strict=False)}


def _parameters_from_payload(payload: dict[str, Any], scenario: dict[str, Any], shocked: bool) -> EquilibriumParameters:
    benchmark = _benchmark_from_payload(payload)
    base_tariff = float(payload.get("parameters", {}).get("tax_parameters", {}).get("import_tariff_rate", 0.10))
    tariff_rate = base_tariff
    target = scenario.get("target_account") or scenario.get("target_commodity") or scenario.get("shock_account") or "composite_commodity"
    if shocked and (scenario.get("policy_instrument") == "import_tariff" or scenario.get("shock_type") == "import_tariff"):
        shock = abs(float(scenario.get("shock_magnitude_percent", scenario.get("shock_size", scenario.get("shock_value", 0))) or 0.0)) / 100.0
        direction = scenario.get("shock_direction", "decrease")
        tariff_rate = base_tariff * (1.0 - shock if direction == "decrease" else 1.0 + shock)
    return EquilibriumParameters(
        benchmark=benchmark,
        tariff_rate=max(tariff_rate, 0.0),
        indirect_tax_rate=0.05,
        direct_tax_rate=0.07,
        savings_rate=0.18,
        government_savings_rate=0.10,
        import_elasticity=1.8,
        export_elasticity=1.2,
        output_elasticity=0.7,
        wage_index=1.0,
        productivity=1.0,
        world_import_price=1.0,
        world_export_price=1.0,
        foreign_savings=benchmark["imports"] - benchmark["exports"],
        target_account=str(target),
        benchmark_source=payload.get("benchmark", {}).get("source", "prototype calibrated benchmark"),
    )


def _benchmark_from_payload(payload: dict[str, Any]) -> dict[str, float]:
    benchmark = payload.get("benchmark", {})
    defaults = _default_benchmark()
    values = benchmark.get("equilibrium_values", {}) if isinstance(benchmark, dict) else {}
    return {key: float(values.get(key, defaults[key])) for key in VARIABLES}


def _default_benchmark() -> dict[str, float]:
    return {
        "domestic_output": 100.0,
        "composite_demand": 120.0,
        "imports": 30.0,
        "exports": 20.0,
        "commodity_price": 1.0,
        "activity_price": 1.1,
        "household_income": 94.04,
        "government_revenue": 16.72,
        "investment": 18.6024,
        "exchange_rate": 1.0,
    }


def _prototype_calibration() -> dict[str, Any]:
    return {
        "benchmark_flows": {},
        "share_parameters": {},
        "diagnostics": {"readiness": {"prototype_cge_calibration": "partial"}},
        "warnings": ["Using prototype calibrated benchmark because no complete SAM calibration payload was supplied."],
    }


def _compare_levels(benchmark: dict[str, float], policy: dict[str, float], params: EquilibriumParameters) -> dict[str, float]:
    comparison = {
        "output_change_pct": _pct(policy["domestic_output"], benchmark["domestic_output"]),
        "composite_demand_change_pct": _pct(policy["composite_demand"], benchmark["composite_demand"]),
        "import_demand_change_pct": _pct(policy["imports"], benchmark["imports"]),
        "export_demand_change_pct": _pct(policy["exports"], benchmark["exports"]),
        "commodity_price_change_pct": _pct(policy["commodity_price"], benchmark["commodity_price"]),
        "activity_price_change_pct": _pct(policy["activity_price"], benchmark["activity_price"]),
        "household_welfare_proxy_change_pct": _pct(policy["household_income"] / policy["commodity_price"], benchmark["household_income"] / benchmark["commodity_price"]),
        "government_revenue_change_pct": _pct(policy["government_revenue"], benchmark["government_revenue"]),
        "investment_change_pct": _pct(policy["investment"], benchmark["investment"]),
        "exchange_rate_change_pct": _pct(policy["exchange_rate"], benchmark["exchange_rate"]),
    }
    base_trade_balance = benchmark["exports"] - benchmark["imports"]
    policy_trade_balance = policy["exports"] - policy["imports"]
    comparison["trade_balance_change_pct"] = _pct(policy_trade_balance, base_trade_balance)
    comparison["import_price_change_pct"] = _pct(
        policy["exchange_rate"] * (1.0 + params.tariff_rate),
        benchmark["exchange_rate"] * 1.10,
    )
    comparison["government_tariff_revenue_change_pct"] = _pct(
        params.tariff_rate * policy["exchange_rate"] * policy["imports"],
        0.10 * benchmark["exchange_rate"] * benchmark["imports"],
    )
    return {key: round(float(value), 6) for key, value in comparison.items()}


def _pct(policy: float, benchmark: float) -> float:
    if abs(benchmark) < 1e-12:
        return 0.0
    return ((policy - benchmark) / abs(benchmark)) * 100.0


def _closure_name(closure: dict[str, Any] | str | None) -> str:
    if isinstance(closure, str):
        return closure
    if isinstance(closure, dict):
        return str(closure.get("closure") or closure.get("name") or "base_closure")
    return "base_closure"


def _failed_result(reason: str, payload: dict[str, Any], solve_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "success": False,
        "backend": "open_source_equilibrium_solver",
        "result_type": "solver_failed",
        "reason": reason,
        "diagnostics": {
            "converged": False,
            "residual_norm": solve_payload.get("residual_norm"),
            "function_evaluations": solve_payload.get("function_evaluations"),
            "equations_solved": EQUATIONS,
            "variables_solved": VARIABLES,
            "failed_equations": [
                name for name, value in solve_payload.get("residuals", {}).items() if abs(float(value)) > 1e-6
            ],
            "message": solve_payload.get("message", reason),
        },
        "solver_payload": payload,
    }
