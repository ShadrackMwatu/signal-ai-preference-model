"""Parser for the Signal Modelling Language (SML)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .grammar import ASSIGNMENT_PATTERN, SECTION_ORDER, SHOCK_PATTERN, SYMBOL_PATTERN, normalize_identifier
from .schema import IndexedSymbol, OutputCommand, SMLModel, ShockDefinition, SolveCommand


class SMLParseError(ValueError):
    """Raised when SML syntax cannot be parsed."""


def parse_sml_file(path: str | Path) -> SMLModel:
    source = Path(path)
    if not source.exists() and source.parts and source.parts[0] == "signal_modeling_language":
        source = Path("Signal_CGE").joinpath(*source.parts)
    model = parse_sml_text(source.read_text(encoding="utf-8"))
    model.source_path = str(source)
    return model


def parse_sml_text(text: str) -> SMLModel:
    """Parse SML text into an SMLModel dataclass."""

    sections = _split_sections(text)
    model = SMLModel()
    for section, lines in sections.items():
        if section == "SETS":
            model.sets = _parse_sets(lines)
        elif section == "PARAMETERS":
            model.parameters = _parse_parameters(lines)
        elif section == "VARIABLES":
            model.variables = [_parse_symbol(line, section) for line in lines]
        elif section == "EQUATIONS":
            model.equations = [_parse_symbol(line, section) for line in lines]
        elif section == "CLOSURE":
            model.closure = {key: str(value) for key, value in _parse_assignments(lines, section).items()}
        elif section == "SHOCKS":
            model.shocks = [_parse_shock(line) for line in lines]
        elif section == "SOLVE":
            values = _parse_assignments(lines, section)
            model.solve = SolveCommand(
                model=str(values.get("model", "signal_cge")),
                backend=str(values.get("backend", "gams")).lower(),
                solver=str(values.get("solver", "default")).lower(),
            )
        elif section == "OUTPUT":
            values = _parse_assignments(lines, section)
            model.output = OutputCommand(
                gdx=_optional_str(values.get("gdx")),
                excel=_optional_str(values.get("excel")),
                report=_optional_str(values.get("report")),
                gams=_optional_str(values.get("gams")),
            )
    return model


def _split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_section: str | None = None
    for line_number, raw_line in enumerate(str(text).splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        candidate = stripped.rstrip(":").upper()
        if stripped.endswith(":") and candidate in SECTION_ORDER:
            current_section = candidate
            sections.setdefault(current_section, [])
            continue
        if current_section is None:
            raise SMLParseError(f"Line {line_number}: content appears before a valid SML section header")
        sections[current_section].append(stripped)
    return sections


def _parse_sets(lines: list[str]) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    for line in lines:
        match = ASSIGNMENT_PATTERN.match(line)
        if not match:
            raise SMLParseError(f"Invalid SETS assignment: {line}")
        key = normalize_identifier(match.group("key"))
        raw_value = match.group("value").strip()
        if not (raw_value.startswith("[") and raw_value.endswith("]")):
            raise SMLParseError(f"Set {key} must use [item1, item2] syntax")
        parsed[key] = [
            normalize_identifier(item)
            for item in raw_value[1:-1].split(",")
            if item.strip()
        ]
        if not parsed[key]:
            raise SMLParseError(f"Set {key} must contain at least one member")
    return parsed


def _parse_parameters(lines: list[str]) -> dict[str, Any]:
    return _parse_assignments(lines, "PARAMETERS")


def _parse_assignments(lines: list[str], section: str) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for line in lines:
        match = ASSIGNMENT_PATTERN.match(line)
        if not match:
            raise SMLParseError(f"Invalid {section} assignment: {line}")
        values[normalize_identifier(match.group("key"))] = _parse_value(match.group("value"))
    return values


def _parse_symbol(line: str, section: str) -> IndexedSymbol:
    match = SYMBOL_PATTERN.match(line)
    if not match:
        raise SMLParseError(f"Invalid {section} symbol: {line}")
    indices = tuple(
        normalize_identifier(index)
        for index in (match.group("indices") or "").split(",")
        if index.strip()
    )
    return IndexedSymbol(name=normalize_identifier(match.group("name")), indices=indices)


def _parse_shock(line: str) -> ShockDefinition:
    match = SHOCK_PATTERN.match(line)
    if not match:
        raise SMLParseError(f"Invalid SHOCKS expression: {line}")
    return ShockDefinition(
        name=normalize_identifier(match.group("name")),
        target=normalize_identifier(match.group("target").replace("[", "_").replace("]", "")),
        operator=match.group("operator"),
        value=float(match.group("value")),
    )


def _parse_value(value: str) -> Any:
    cleaned = value.strip()
    if cleaned.startswith('"') and cleaned.endswith('"'):
        return cleaned[1:-1]
    if cleaned.startswith("'") and cleaned.endswith("'"):
        return cleaned[1:-1]
    lowered = cleaned.lower()
    if lowered in {"fixed", "endogenous", "exogenous"}:
        return lowered
    try:
        return float(cleaned) if "." in cleaned else int(cleaned)
    except ValueError:
        return normalize_identifier(cleaned)


def _optional_str(value: Any) -> str | None:
    return None if value is None else str(value)
