"""Policy shock utilities for the Signal Static CGE Solver."""

from __future__ import annotations

import re
from typing import Any


SUPPORTED_SHOCKS = {
    "import_tariff_change",
    "export_price_change",
    "productivity_change",
    "government_demand_change",
    "investment_demand_change",
    "household_transfer_change",
    "factor_supply_change",
    "commodity_tax_change",
    "activity_tax_change",
}


def normalize_shock(shock: dict[str, Any] | None = None) -> dict[str, Any]:
    """Normalize a JSON/YAML-friendly shock payload."""

    if not shock:
        return {"shock_type": "none", "target_account": "aggregate", "shock_value": 0.0, "shock_unit": "percent"}
    normalized = {
        "shock_type": str(shock.get("shock_type") or shock.get("policy_instrument") or "none"),
        "target_account": str(shock.get("target_account") or shock.get("target_commodity") or shock.get("shock_account") or "aggregate"),
        "shock_value": float(shock.get("shock_value", shock.get("shock_size", shock.get("shock_magnitude_percent", 0.0))) or 0.0),
        "shock_unit": str(shock.get("shock_unit") or "percent"),
        "shock_direction": str(shock.get("shock_direction") or ""),
    }
    if normalized["shock_type"] in {"import_tariff", "tariff"}:
        normalized["shock_type"] = "import_tariff_change"
    if normalized["shock_type"] in {"vat_tax", "vat"}:
        normalized["shock_type"] = "commodity_tax_change"
    if normalized["shock_direction"] == "decrease" and normalized["shock_value"] > 0:
        normalized["shock_value"] *= -1.0
    return normalized


def parse_policy_shock(prompt: str) -> dict[str, Any]:
    """Parse common policy prompts into a static-CGE shock dictionary."""

    text = (prompt or "").lower()
    value = _extract_percent(text)
    direction = "decrease" if any(term in text for term in ["reduce", "cut", "lower", "decrease"]) else "increase"
    signed_value = -abs(value) if direction == "decrease" else abs(value)
    target = _extract_target(text)
    if "tariff" in text:
        shock_type = "import_tariff_change"
    elif "vat" in text or "commodity tax" in text:
        shock_type = "commodity_tax_change"
    elif "productivity" in text:
        shock_type = "productivity_change"
    elif "government" in text or "spending" in text:
        shock_type = "government_demand_change"
    elif "investment" in text:
        shock_type = "investment_demand_change"
    elif "transfer" in text:
        shock_type = "household_transfer_change"
    else:
        shock_type = "government_demand_change"
    return normalize_shock(
        {
            "shock_type": shock_type,
            "target_account": target,
            "shock_value": signed_value,
            "shock_unit": "percent",
            "shock_direction": direction,
        }
    )


def apply_shock(parameters: dict[str, float], shock: dict[str, Any] | None) -> dict[str, float]:
    """Apply a policy shock to calibrated scalar parameters."""

    params = dict(parameters)
    normalized = normalize_shock(shock)
    shock_type = normalized["shock_type"]
    value = float(normalized["shock_value"])
    proportional = value / 100.0 if normalized["shock_unit"] in {"percent", "%"} else value
    if shock_type == "import_tariff_change":
        if normalized["shock_unit"] == "percentage_point":
            params["tariff_rate"] = max(params["tariff_rate"] + value, 0.0)
        else:
            params["tariff_rate"] = max(params["tariff_rate"] * (1.0 + proportional), 0.0)
    elif shock_type == "export_price_change":
        params["world_export_price"] *= 1.0 + proportional
    elif shock_type == "productivity_change":
        params["productivity"] *= 1.0 + proportional
    elif shock_type == "government_demand_change":
        params["government_demand_multiplier"] *= 1.0 + proportional
    elif shock_type == "investment_demand_change":
        params["investment_demand_multiplier"] *= 1.0 + proportional
    elif shock_type == "household_transfer_change":
        params["household_transfer"] += params["household_income"] * proportional
    elif shock_type == "factor_supply_change":
        params["factor_supply"] *= 1.0 + proportional
    elif shock_type == "commodity_tax_change":
        params["commodity_tax_rate"] = max(params["commodity_tax_rate"] * (1.0 + proportional), 0.0)
    elif shock_type == "activity_tax_change":
        params["activity_tax_rate"] = max(params["activity_tax_rate"] * (1.0 + proportional), 0.0)
    return params


def _extract_percent(text: str) -> float:
    match = re.search(r"([-+]?\d+(?:\.\d+)?)\s*(?:%|percent)", text)
    return float(match.group(1)) if match else 10.0


def _extract_target(text: str) -> str:
    patterns = [r"\bon\s+([a-zA-Z0-9_]+)", r"\bfor\s+([a-zA-Z0-9_]+)", r"\bin\s+([a-zA-Z0-9_]+)"]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return "aggregate"
