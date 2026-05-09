"""Welfare and household result helpers."""

from __future__ import annotations

from typing import Any


def summarize_welfare_results(results: dict[str, Any]) -> dict[str, Any]:
    return {
        "proxy_welfare": results.get("welfare/proxy welfare effect", 0.0),
        "household_income": results.get("household income effect", 0.0),
        "interpretation": "Proxy welfare uses household income or aggregate output until full consumer-price feedbacks are active.",
    }
