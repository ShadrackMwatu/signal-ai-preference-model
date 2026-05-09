"""Macro result summaries for Signal CGE."""

from __future__ import annotations

from typing import Any


def summarize_macro_results(results: dict[str, Any]) -> dict[str, Any]:
    return {
        "real_gdp": results.get("GDP/output effect", 0.0),
        "absorption": results.get("welfare/proxy welfare effect", 0.0),
        "government_balance": results.get("government balance effect", 0.0),
        "trade_balance_proxy": results.get("trade effect", 0.0),
    }
