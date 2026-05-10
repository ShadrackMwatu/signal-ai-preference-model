"""Structured shock containers for Signal CGE experiments."""

from __future__ import annotations

import re
from typing import Any


def parse_shock_prompt(prompt: str) -> dict[str, Any]:
    """Parse a natural-language policy prompt into a structured shock."""

    text = (prompt or "").lower()
    magnitude = _extract_percent(text)
    target = _extract_target(text)
    direction = "decrease" if any(term in text for term in ["reduce", "lower", "cut"]) else "increase"
    signed_value = -abs(magnitude) if direction == "decrease" else abs(magnitude)
    if "tariff" in text:
        return {
            "experiment_type": "trade_policy",
            "instrument": "import_tariff",
            "target_commodity": target,
            "shock_direction": direction,
            "shock_value_percent": signed_value,
            "future_solver_payload": {
                "target_equation_blocks": ["imports", "price_equations", "government_balance", "external_balance"],
                "instrument_variable": f"import_tariff_rate[{target}]" if target else "import_tariff_rate",
            },
        }
    if "vat" in text:
        return {"experiment_type": "tax_policy", "instrument": "vat_tax", "target_commodity": target, "shock_direction": direction, "shock_value_percent": signed_value}
    if "productivity" in text:
        return {"experiment_type": "productivity", "instrument": "sector_productivity", "target_activity": target, "shock_direction": direction, "shock_value_percent": signed_value}
    return {"experiment_type": "custom", "instrument": "generic_shock", "target_account": target, "shock_direction": direction, "shock_value_percent": signed_value}


def _extract_percent(text: str) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent)", text)
    return float(match.group(1)) if match else 0.0


def _extract_target(text: str) -> str:
    match = re.search(r"\bon\s+([a-zA-Z][a-zA-Z0-9_/-]*)", text)
    return match.group(1).strip(" .,/;:") if match else ""
