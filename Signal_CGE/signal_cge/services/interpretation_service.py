"""Interpretation service for Signal CGE outputs."""

from __future__ import annotations

from typing import Any


def summarize_results(results: dict[str, Any]) -> dict[str, Any]:
    """Generate lightweight interpretation metadata from solver outputs."""

    payload = results.get("results", {}) if isinstance(results, dict) else {}
    accounts = payload.get("accounts", {}) if isinstance(payload, dict) else {}
    total_effect = sum(float(value) for value in accounts.values()) if accounts else 0.0

    return {
        "headline": "Expansionary effect detected" if total_effect >= 0 else "Contractionary effect detected",
        "aggregate_effect": round(total_effect, 6),
        "solver_backend": results.get("backend", "unknown"),
        "policy_note": "Results remain conditional on SAM quality, closure assumptions, and available equilibrium structure.",
    }
