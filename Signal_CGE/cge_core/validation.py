"""Combined model and data validation for Signal CGE runs."""

from __future__ import annotations

import pandas as pd

from signal_modeling_language.schema import SMLModel
from signal_modeling_language.validator import validate_model

from .closures import validate_closure_rules
from .sam import balance_check, is_balanced


def validate_cge_inputs(model: SMLModel, sam_matrix: pd.DataFrame, tolerance: float = 0.01) -> dict[str, object]:
    sml_validation = validate_model(model)
    closure_issues = validate_closure_rules(model)
    balance = balance_check(sam_matrix)
    errors = list(sml_validation.errors) + closure_issues
    warnings = list(sml_validation.warnings)
    if not is_balanced(sam_matrix, tolerance=tolerance):
        warnings.append("SAM is outside the selected balance tolerance.")
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "balance_check": balance.to_dict(orient="records"),
    }
