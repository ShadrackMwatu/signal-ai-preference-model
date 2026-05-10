"""Result tables for Signal CGE output payloads."""

from __future__ import annotations

from typing import Any


def build_result_table(results: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"indicator": key, "value": value} for key, value in results.items() if not isinstance(value, dict)]


def build_percentage_change_table(policy: dict[str, float], baseline: dict[str, float]) -> list[dict[str, float | str]]:
    rows = []
    for key, policy_value in policy.items():
        base = baseline.get(key, 0.0)
        change = 0.0 if base == 0 else ((policy_value - base) / base) * 100
        rows.append({"indicator": key, "baseline": base, "policy": policy_value, "percent_change": round(change, 6)})
    return rows
