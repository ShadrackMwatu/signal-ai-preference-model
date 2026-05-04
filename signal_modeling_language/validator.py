"""Validation for parsed Signal Modelling Language models."""

from __future__ import annotations

from dataclasses import dataclass, field

from .grammar import REQUIRED_SECTIONS, SUPPORTED_BACKENDS, SUPPORTED_SOLVERS
from .schema import SMLModel


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def raise_for_errors(self) -> None:
        if not self.valid:
            raise ValueError("; ".join(self.errors))


def validate_model(model: SMLModel) -> ValidationResult:
    """Validate SML structure, index references, and backend choices."""

    errors: list[str] = []
    warnings: list[str] = []
    present_sections = _present_sections(model)
    missing_sections = REQUIRED_SECTIONS - present_sections
    if missing_sections:
        errors.append(f"Missing required section(s): {', '.join(sorted(missing_sections))}")

    for symbol in model.variables + model.equations:
        for index in symbol.indices:
            if index not in model.sets:
                errors.append(f"Symbol {symbol.name} references unknown set {index}")

    if "sam" not in model.parameters:
        errors.append("PARAMETERS must define SAM path")
    if model.solve.backend not in SUPPORTED_BACKENDS:
        errors.append(f"Unsupported SOLVE backend: {model.solve.backend}")
    if model.solve.solver not in SUPPORTED_SOLVERS:
        errors.append(f"Unsupported SOLVE solver: {model.solve.solver}")
    if not model.closure:
        warnings.append("No CLOSURE section was provided; default closure assumptions will be used.")
    if not model.shocks:
        warnings.append("No SHOCKS were provided; run will behave like a baseline validation.")
    if model.solve.backend == "gams" and model.solve.solver == "default":
        warnings.append("GAMS backend selected with default solver; production runs should specify PATH, CONOPT, or IPOPT.")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def _present_sections(model: SMLModel) -> set[str]:
    present: set[str] = set()
    if model.sets:
        present.add("SETS")
    if model.parameters:
        present.add("PARAMETERS")
    if model.variables:
        present.add("VARIABLES")
    if model.equations:
        present.add("EQUATIONS")
    if model.closure:
        present.add("CLOSURE")
    if model.shocks:
        present.add("SHOCKS")
    if model.solve:
        present.add("SOLVE")
    if model.output:
        present.add("OUTPUT")
    return present
