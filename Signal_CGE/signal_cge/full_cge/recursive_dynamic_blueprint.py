"""Recursive dynamic blueprint for Signal CGE."""

from __future__ import annotations

from typing import Any


def get_recursive_dynamic_blueprint() -> dict[str, Any]:
    return {
        "status": "blueprint",
        "modules": {
            "capital_accumulation": "K[t+1,a] = (1 - depreciation[a]) * K[t,a] + investment_allocation[t,a]",
            "labor_growth": "FS[t+1,f] = FS[t,f] * (1 + labor_growth[f,t])",
            "productivity_growth": "TFP[t+1,a] = TFP[t,a] * (1 + productivity_growth[a,t])",
            "baseline_projection": "Carry calibrated benchmark forward with exogenous growth assumptions.",
            "annual_simulation_loop": "Solve baseline and policy scenario period by period.",
            "period_result_storage": "Store macro, sectoral, factor, household, welfare, and diagnostics outputs by year.",
        },
    }
