"""Generate placeholder GAMS-ready text from parsed SML."""

from __future__ import annotations

from typing import Any


def export_to_gams(parsed: dict[str, Any]) -> str:
    sets = ", ".join(sorted(parsed.get("sets", {}).keys())) or "none"
    variables = ", ".join(parsed.get("variables", [])) or "none"
    equations = ", ".join(parsed.get("equations", [])) or "none"
    shocks = ", ".join(parsed.get("shocks", [])) or "baseline"
    solve = parsed.get("solve", {})
    return (
        "* Signal SML to GAMS export preview\n"
        f"* Sets: {sets}\n"
        f"* Variables: {variables}\n"
        f"* Equations: {equations}\n"
        f"* Shocks: {shocks}\n\n"
        "SETS\n"
        f"    section_names /{sets}/;\n\n"
        "VARIABLES\n"
        f"    {variables};\n\n"
        "EQUATIONS\n"
        f"    {equations};\n\n"
        f"MODEL {solve.get('model', 'signal_cge')} /all/;\n"
        f"SOLVE {solve.get('model', 'signal_cge')} USING CNS;\n"
    )
