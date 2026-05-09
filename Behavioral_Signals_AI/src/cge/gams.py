"""GAMS compatibility export for Signal CGE scenarios."""

from __future__ import annotations

import pandas as pd

from .sam import sam_matrix
from .schema import CGEScenario


def export_gams_model(sam: pd.DataFrame, scenario: CGEScenario) -> str:
    """Create a GAMS-compatible text model skeleton from a SAM and scenario."""

    matrix = sam_matrix(sam)
    accounts = list(matrix.index)
    lines = [
        "* Signal CGE model export",
        f"* Scenario: {scenario.name}",
        f"* Closure: {scenario.closure}",
        f"* Numeraire: {scenario.numeraire}",
        "Sets",
        f"    i accounts / {', '.join(accounts)} /;",
        "Alias (i,j);",
        "",
        "Parameter SAM(i,j) social accounting matrix /",
    ]
    for row_account in accounts:
        for column_account in accounts:
            value = float(matrix.loc[row_account, column_account])
            if value:
                lines.append(f"    {row_account}.{column_account} {value:.6f}")
    lines.extend(["/;", "", "Scalars"])
    for index, shock in enumerate(scenario.shocks, start=1):
        lines.append(
            f"    shock_{index}_{shock.shock_type}_{shock.target} / {shock.change_decimal:.6f} /"
        )
    lines.extend(
        [
            ";",
            "",
            "Variables output(i), price(i), income(i);",
            "Equations market_clear(i), income_balance(i);",
            "market_clear(i).. output(i) =g= sum(j, SAM(i,j));",
            "income_balance(i).. income(i) =e= sum(j, SAM(j,i));",
            "Model signal_cge / all /;",
            "Solve signal_cge using CNS;",
        ]
    )
    return "\n".join(lines)
