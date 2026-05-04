"""Equation inventory helpers."""

from __future__ import annotations

from signal_modeling_language.schema import SMLModel


def equation_inventory(model: SMLModel) -> list[dict[str, object]]:
    """Return a structured list of declared equations and their domains."""

    return [
        {
            "equation": equation.name,
            "indices": list(equation.indices),
            "status": "declared",
        }
        for equation in model.equations
    ]
