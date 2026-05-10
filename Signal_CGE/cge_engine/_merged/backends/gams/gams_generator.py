"""Convert Signal Modelling Language models into GAMS-compatible .gms code."""

from __future__ import annotations

from signal_modeling_language.schema import SMLModel

from .gams_templates import HEADER_TEMPLATE, MODEL_FOOTER_TEMPLATE, solver_option_block


def generate_gams_code(model: SMLModel, calibration: dict[str, object] | None = None) -> str:
    """Generate reusable GAMS code from an SML model specification."""

    calibration = calibration or {}
    lines: list[str] = [HEADER_TEMPLATE.strip(), ""]
    lines.extend(_sets_block(model))
    lines.extend(_parameters_block(model, calibration))
    lines.extend(_variables_block(model))
    lines.extend(_equations_block(model))
    lines.extend(_shock_block(model))
    lines.append(solver_option_block(model.solve.solver))
    display_symbols = ", ".join(variable.name for variable in model.variables[:5]) or "output"
    lines.append(
        MODEL_FOOTER_TEMPLATE.format(
            model_name=model.solve.model,
            display_symbols=display_symbols,
            gdx_path=model.output.gdx or "outputs/results.gdx",
        ).strip()
    )
    return "\n".join(lines) + "\n"


def _sets_block(model: SMLModel) -> list[str]:
    lines = ["Sets"]
    entries = []
    for name, members in model.sets.items():
        entries.append(f"    {name} / {', '.join(members)} /")
    return lines + ["\n".join(entries) + ";", ""]


def _parameters_block(model: SMLModel, calibration: dict[str, object]) -> list[str]:
    lines = ["Parameters"]
    entries: list[str] = []
    for key, value in model.parameters.items():
        if key == "sam":
            entries.append(f"    sam_source / 0 /")
        elif isinstance(value, int | float):
            entries.append(f"    {key} / {float(value):.6f} /")
    total_activity = calibration.get("total_activity")
    if total_activity is not None:
        entries.append(f"    total_activity / {float(total_activity):.6f} /")
    if not entries:
        entries.append("    placeholder_parameter / 0 /")
    return lines + ["\n".join(entries) + ";", ""]


def _variables_block(model: SMLModel) -> list[str]:
    names = ", ".join(symbol.name for symbol in model.variables) or "output"
    return [f"Variables {names};", ""]


def _equations_block(model: SMLModel) -> list[str]:
    equation_names = ", ".join(symbol.name for symbol in model.equations) or "market_clearing"
    lines = [f"Equations {equation_names};"]
    for equation in model.equations:
        variable_name = model.variables[0].name if model.variables else "output"
        lines.append(f"{equation.name}.. {variable_name} =g= 0;")
    if not model.equations:
        lines.append("market_clearing.. output =g= 0;")
    lines.append("")
    return lines


def _shock_block(model: SMLModel) -> list[str]:
    if not model.shocks:
        return ["* No shocks declared.", ""]
    lines = ["Scalars"]
    entries = [
        f"    shock_{shock.name} / {shock.value:.6f} /"
        for shock in model.shocks
    ]
    return lines + ["\n".join(entries) + ";", ""]
