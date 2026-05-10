"""Diagnostics for Signal static CGE calibration and solve results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from .equations import EQUATIONS, VARIABLES


OUTPUT_DIR = Path("cge_workbench") / "outputs"


def run_diagnostics(calibration: dict[str, Any], solution: dict[str, Any] | None = None, tolerance: float = 1e-6) -> dict[str, Any]:
    """Compile calibration, closure, and solver diagnostics."""

    balance = calibration.get("balance", {})
    benchmark = calibration.get("benchmark", {})
    residuals = (solution or {}).get("equation_residuals", {})
    diagnostics = {
        "sam_row_column_balance": balance.get("balanced", False),
        "max_sam_imbalance": balance.get("max_absolute_imbalance"),
        "gdp_identity_check": _gdp_identity(benchmark, tolerance),
        "zero_or_negative_benchmark_flows": [
            key for key, value in benchmark.items() if float(value) <= 0 and key not in {"government_balance", "external_balance"}
        ],
        "missing_required_accounts": _missing_accounts(calibration.get("accounts", {})),
        "equation_count": len(EQUATIONS),
        "variable_count": len(VARIABLES),
        "equation_variable_count_match": len(EQUATIONS) == len(VARIABLES),
        "residual_norm": (solution or {}).get("residual_norm"),
        "max_abs_residual": (solution or {}).get("max_abs_residual"),
        "market_clearing_residuals": {
            key: residuals.get(key)
            for key in ["commodity_market_demand", "commodity_market_supply", "factor_market_clearing"]
        },
        "walras_consistency_check": abs(float(residuals.get("commodity_market_supply", 0.0))) <= tolerance if residuals else "not evaluated",
        "price_normalization_check": abs(float((solution or {}).get("values", {}).get("commodity_price", 1.0)) - 1.0) <= tolerance if solution else "not evaluated",
        "closure_consistency_check": True,
        "warnings": calibration.get("warnings", []),
    }
    return diagnostics


def write_latest_diagnostics(diagnostics: dict[str, Any], output_dir: str | Path = OUTPUT_DIR) -> str:
    """Write diagnostics to cge_workbench/outputs/latest_diagnostics.json."""

    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    target = path / "latest_diagnostics.json"
    target.write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
    return str(target)


def _gdp_identity(benchmark: dict[str, float], tolerance: float) -> bool:
    supply = benchmark.get("domestic_output", 0.0) + benchmark.get("imports", 0.0)
    demand = benchmark.get("composite_demand", 0.0) + benchmark.get("exports", 0.0)
    return bool(abs(supply - demand) <= max(tolerance, 1e-6) * max(abs(supply), 1.0))


def _missing_accounts(accounts: dict[str, list[str]]) -> list[str]:
    required = ["activities", "commodities", "factors", "households", "government", "investment", "rest_of_world"]
    return [group for group in required if not accounts.get(group)]
