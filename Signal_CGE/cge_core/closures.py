"""Closure rule validation for CGE scenarios."""

from __future__ import annotations

from signal_modeling_language.schema import SMLModel


REQUIRED_CLOSURE_KEYS = {"numeraire"}
ALLOWED_CLOSURE_VALUES = {"fixed", "endogenous", "exogenous", "consumer_price_index"}


def validate_closure_rules(model: SMLModel) -> list[str]:
    """Return closure-rule issues; empty list means valid for prototype execution."""

    issues: list[str] = []
    for key in REQUIRED_CLOSURE_KEYS:
        if key not in model.closure:
            issues.append(f"CLOSURE must define {key}")
    for key, value in model.closure.items():
        if value not in ALLOWED_CLOSURE_VALUES and key != "numeraire":
            issues.append(f"Unsupported closure value for {key}: {value}")
    return issues
