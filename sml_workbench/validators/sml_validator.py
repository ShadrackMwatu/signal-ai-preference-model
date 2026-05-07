"""Validation wrapper for the integrated Signal SML workbench."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from signal_modeling_language.parser import SMLParseError, parse_sml_file as _parse_file, parse_sml_text
from signal_modeling_language.validator import validate_model


def validate_sml(source: str | Path | dict[str, Any]) -> dict[str, Any]:
    try:
        if isinstance(source, dict) and "model" in source:
            model = source["model"]
        elif isinstance(source, Path):
            model = _parse_file(source)
        elif isinstance(source, str) and "\n" not in source and "\r" not in source and Path(source).exists():
            model = _parse_file(source)
        else:
            model = parse_sml_text(str(source))
    except (SMLParseError, OSError) as exc:
        return {
            "valid": False,
            "errors": [str(exc)],
            "warnings": [],
            "message": f"SML validation failed: {exc}",
        }

    validation = validate_model(model)
    return {
        "valid": validation.valid,
        "errors": validation.errors,
        "warnings": validation.warnings,
        "message": "SML validation passed." if validation.valid else "SML validation failed.",
    }
