"""Factor market block for labour, capital, and gender-care factors."""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "factor_market"
CARE_FACTOR_SUFFIXES = {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"}


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "factor_income",
            "equation": "YF[f] = WF[f] * FSUP[f]",
            "role": "Factor income equals factor price times factor supply.",
        },
        {
            "name": "factor_market_balance",
            "equation": "sum(a, FD[a, f]) = FSUP[f]",
            "role": "Factor demand equals factor supply under the selected factor closure.",
        },
    ]


def validate_factor_data(data: dict[str, Any]) -> dict[str, Any]:
    factors = {str(factor).lower() for factor in data.get("factors", [])}
    warnings = []
    if not factors:
        warnings.append("No factor accounts were supplied.")
    if data.get("kenya_gender_care") and not CARE_FACTOR_SUFFIXES.issubset(factors):
        missing = ", ".join(sorted(CARE_FACTOR_SUFFIXES.difference(factors)))
        warnings.append(f"Kenya gender-care factor suffixes missing: {missing}")
    return {"valid": True, "errors": [], "warnings": warnings}


def build_factor_market_block(parameters: dict[str, Any]) -> dict[str, Any]:
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validate_factor_data(parameters)}
