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
    equilibrium_values = _equilibrium_values_from_benchmark(benchmark)
    variables = get_variable_registry()
    parameter_registry = get_parameter_registry()
    parameters = {
        "registry": parameter_registry,
        "share_parameters": shares,
        "elasticities": {
            "import_elasticity": 1.8,
            "export_elasticity": 1.2,
            "output_elasticity": 0.7,
        },
        "tax_parameters": {
            "import_tariff_rate": 0.10,
            "indirect_tax_rate": 0.05,
            "direct_tax_rate": 0.07,
        },
    }
    equations = get_equation_registry()
    closure = default_closure_payload(closure_name)
    return {
        "status": "solver_ready_blueprint",
        "variables": variables,
        "parameters": parameters,
        "initial_values": {key: value for key, value in equilibrium_values.items()},
        "equations": equations,
        "closure": closure,
        "benchmark": {
            "source": "SAM calibration" if benchmark else "prototype calibrated benchmark",
            "flows": benchmark,
            "equilibrium_values": equilibrium_values,
        },
        "benchmark_variables": benchmark_variables,
        "benchmark_parameters": benchmark_parameters,
        "equation_inputs": {
            "equations": equations,
            "variables": variables,
            "parameters": parameter_registry,
        },
        "closure_settings": closure,
        "diagnostics": diagnostics,
        "warnings": [
            "Elasticities use prototype defaults until a full elasticity dataset is available.",
            "Payload is structured for the open-source prototype equilibrium solver.",
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


def _equilibrium_values_from_benchmark(benchmark: dict[str, Any]) -> dict[str, float]:
    activity_output = _sum_values(benchmark.get("activity_output", {}))
    commodity_demand = _sum_values(benchmark.get("commodity_demand", {}))
    imports = _sum_nested(benchmark.get("imports", {}))
    exports = _sum_nested(benchmark.get("exports", {}))
    household_income = _sum_values(benchmark.get("household_income", {}))
    government_demand = _sum_nested(benchmark.get("government_demand", {}))
    investment_demand = _sum_nested(benchmark.get("investment_demand", {}))
    domestic_output = activity_output or 100.0
    composite_demand = commodity_demand or max(domestic_output + imports - exports, 1.0)
    import_value = imports or max(0.25 * composite_demand, 1.0)
    export_value = exports or max(0.18 * domestic_output, 1.0)
    gov_revenue = government_demand or 0.14 * composite_demand
    income = household_income or 0.82 * domestic_output + 0.08 * gov_revenue
    investment = investment_demand or 0.18 * income + 0.10 * gov_revenue
    return {
        "domestic_output": float(max(domestic_output, 1.0)),
        "composite_demand": float(max(composite_demand, 1.0)),
        "imports": float(max(import_value, 1.0)),
        "exports": float(max(export_value, 1.0)),
        "commodity_price": 1.0,
        "activity_price": 1.1,
        "household_income": float(max(income, 1.0)),
        "government_revenue": float(max(gov_revenue, 1.0)),
        "investment": float(max(investment, 1.0)),
        "exchange_rate": 1.0,
    }


def _sum_values(payload: dict[str, Any]) -> float:
    total = 0.0
    if not isinstance(payload, dict):
        return total
    for value in payload.values():
        try:
            total += float(value)
        except (TypeError, ValueError):
            continue
    return total


def _sum_nested(payload: dict[str, Any]) -> float:
    total = 0.0
    if not isinstance(payload, dict):
        return total
    for value in payload.values():
        if isinstance(value, dict):
            total += _sum_values(value)
        else:
            try:
                total += float(value)
            except (TypeError, ValueError):
                continue
    return total
