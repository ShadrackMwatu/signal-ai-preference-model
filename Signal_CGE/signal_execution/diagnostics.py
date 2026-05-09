"""Diagnostics for Signal CGE execution workflows."""

from __future__ import annotations

import pandas as pd

from cge_core.sam import balance_check, is_balanced
from signal_modeling_language.schema import SMLModel
from signal_modeling_language.validator import validate_model


def build_diagnostics(model: SMLModel, sam_matrix: pd.DataFrame, tolerance: float = 0.01) -> dict[str, object]:
    validation = validate_model(model)
    balance = balance_check(sam_matrix)
    return {
        "valid": validation.valid,
        "errors": validation.errors,
        "warnings": validation.warnings,
        "sam_balanced": is_balanced(sam_matrix, tolerance),
        "balance_check": balance.to_dict(orient="records"),
    }
