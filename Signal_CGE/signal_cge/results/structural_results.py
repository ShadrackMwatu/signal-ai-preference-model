"""Structural result summaries for sector, trade, and factor shifts."""

from __future__ import annotations

from typing import Any


def summarize_structural_results(results: dict[str, Any]) -> dict[str, Any]:
    accounts = results.get("account_effects", {})
    return {
        "factor_income": results.get("factor income effect", 0.0),
        "trade": results.get("trade effect", 0.0),
        "largest_account_effects": sorted(accounts.items(), key=lambda item: abs(float(item[1])), reverse=True)[:5] if isinstance(accounts, dict) else [],
    }
