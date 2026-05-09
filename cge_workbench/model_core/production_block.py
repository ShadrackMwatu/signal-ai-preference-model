"""Production block for the formal Signal CGE model.

The production block maps activity output to intermediate demand and factor
use. A future solver can replace these placeholder equations with calibrated
CES, Leontief, or nested production functions.
"""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "production"


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "activity_output_identity",
            "equation": "QX[a] = FVA[a] + INT[a]",
            "role": "Activity output equals value added plus intermediate input bundle.",
        },
        {
            "name": "value_added_aggregation",
            "equation": "FVA[a] = VA_FUNCTION(F[a, f], alpha_va[a, f])",
            "role": "Value added is built from primary factor inputs.",
        },
    ]


def validate_production_data(data: dict[str, Any]) -> dict[str, Any]:
    required = {"activities", "factors"}
    missing = sorted(required.difference(data))
    return {"valid": not missing, "errors": [f"Missing production data: {item}" for item in missing]}


def build_production_block(parameters: dict[str, Any]) -> dict[str, Any]:
    """Return a transparent production-block specification."""

    validation = validate_production_data(parameters)
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validation}
