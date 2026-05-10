"""Calibration and baseline consistency checks."""

from __future__ import annotations

from typing import Any

import pandas as pd


def validate_calibration(sam: pd.DataFrame | None = None) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    if sam is None:
        warnings.append("No external SAM supplied; using the built-in demonstration SAM.")
    elif sam.shape[0] != sam.shape[1]:
        errors.append("Calibration requires a square SAM.")
    return {"valid": not errors, "errors": errors, "warnings": warnings}


def validate_shock(scenario: dict[str, Any], accounts: list[str] | None = None) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    value = float(scenario.get("shock_value", 0.0))
    if abs(value) > 500:
        warnings.append("Shock value is very large; interpret multiplier results cautiously.")
    targets = scenario.get("target_accounts", [])
    if not targets:
        errors.append("Scenario has no target accounts.")
    if accounts and targets and targets != ["all"]:
        matched = [target for target in targets if any(str(target).lower() in account.lower() for account in accounts)]
        if not matched:
            warnings.append("No target account directly matched the supplied SAM accounts; fallback targeting may be used.")
    return {"valid": not errors, "errors": errors, "warnings": warnings}
