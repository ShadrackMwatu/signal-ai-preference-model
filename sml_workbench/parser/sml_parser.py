"""Convenience parser for the integrated Signal SML workbench."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from signal_modeling_language.parser import SMLParseError, parse_sml_file as _parse_file, parse_sml_text


def load_sml_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def parse_sml(text: str) -> dict[str, Any]:
    model = parse_sml_text(text)
    return {
        "sets": model.sets,
        "parameters": model.parameters,
        "variables": [symbol.name for symbol in model.variables],
        "equations": [symbol.name for symbol in model.equations],
        "shocks": [shock.name for shock in model.shocks],
        "closure": model.closure,
        "solve": {
            "model": model.solve.model,
            "backend": model.solve.backend,
            "solver": model.solve.solver,
        },
        "output": {
            "gdx": model.output.gdx,
            "excel": model.output.excel,
            "report": model.output.report,
            "gams": model.output.gams,
        },
        "model": model,
    }


def parse_sml_file(path: str | Path) -> dict[str, Any]:
    model = _parse_file(path)
    return parse_sml_text_to_dict(model)


def parse_sml_text_to_dict(model: Any) -> dict[str, Any]:
    return {
        "sets": model.sets,
        "parameters": model.parameters,
        "variables": [symbol.name for symbol in model.variables],
        "equations": [symbol.name for symbol in model.equations],
        "shocks": [shock.name for shock in model.shocks],
        "closure": model.closure,
        "solve": {
            "model": model.solve.model,
            "backend": model.solve.backend,
            "solver": model.solve.solver,
        },
        "output": {
            "gdx": model.output.gdx,
            "excel": model.output.excel,
            "report": model.output.report,
            "gams": model.output.gams,
        },
        "model": model,
    }


__all__ = ["SMLParseError", "load_sml_text", "parse_sml", "parse_sml_file"]
