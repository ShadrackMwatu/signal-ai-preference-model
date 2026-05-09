"""Collect experiment results into a consistent Signal CGE payload."""

from __future__ import annotations

from typing import Any


def collect_experiment_results(run_payload: dict[str, Any]) -> dict[str, Any]:
    indicators = run_payload.get("directional_indicators", {})
    return {
        "result_type": run_payload.get("result_type", "prototype_directional_indicator"),
        "macro": {"output_pressure": indicators.get("aggregate_output_pressure", 0.0)},
        "trade": {key: value for key, value in indicators.items() if "trade" in key or "import" in key},
        "government": {"revenue_pressure": indicators.get("government_revenue_pressure", 0.0)},
        "welfare": {"proxy_pressure": indicators.get("welfare_proxy_pressure", 0.0)},
    }
