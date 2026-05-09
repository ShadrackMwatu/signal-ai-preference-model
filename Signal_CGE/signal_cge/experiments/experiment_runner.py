"""Prototype experiment runner for Signal CGE."""

from __future__ import annotations

from typing import Any

from .shock_container import parse_shock_prompt


def run_prototype_experiment(prompt: str, base_results: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return directional indicators and a future full-solve payload."""

    shock = parse_shock_prompt(prompt)
    value = float(shock.get("shock_value_percent", 0.0))
    indicators = _directional_indicators(shock, value)
    return {
        "shock": shock,
        "result_type": "prototype_directional_indicator",
        "directional_indicators": indicators,
        "base_results": base_results or {},
        "future_full_equilibrium_payload": shock.get("future_solver_payload", {}),
    }


def _directional_indicators(shock: dict[str, Any], value: float) -> dict[str, float]:
    if shock.get("instrument") == "import_tariff":
        reduction = abs(value) if value < 0 else -abs(value)
        return {
            "import_price_pressure": round(reduction * 0.6, 4),
            "government_revenue_pressure": round(value * 0.4, 4),
            "import_demand_pressure": round(abs(value) * 0.5, 4),
            "domestic_substitute_pressure": round(-abs(value) * 0.25, 4),
            "welfare_proxy_pressure": round(abs(value) * 0.2, 4),
            "trade_balance_pressure": round(-abs(value) * 0.15, 4),
        }
    return {"aggregate_output_pressure": round(value * 0.1, 4)}
