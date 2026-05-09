"""Generate placeholder Pyomo-ready text from parsed SML."""

from __future__ import annotations

from typing import Any


def export_to_pyomo(parsed: dict[str, Any]) -> str:
    variables = parsed.get("variables", [])
    equations = parsed.get("equations", [])
    return (
        "# Signal SML to Pyomo export preview\n"
        "from pyomo.environ import ConcreteModel, Var, Constraint\n\n"
        "model = ConcreteModel()\n"
        f"# Variables: {', '.join(variables) or 'none'}\n"
        f"# Equations: {', '.join(equations) or 'none'}\n"
        "model.placeholder = Var(initialize=1.0)\n"
        "model.balance = Constraint(expr=model.placeholder >= 0)\n"
    )
