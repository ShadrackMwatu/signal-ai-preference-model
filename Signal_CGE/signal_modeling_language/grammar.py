"""SML section names, grammar hints, and parsing helpers."""

from __future__ import annotations

import re


SECTION_ORDER = (
    "SETS",
    "PARAMETERS",
    "VARIABLES",
    "EQUATIONS",
    "CLOSURE",
    "SHOCKS",
    "SOLVE",
    "OUTPUT",
)
REQUIRED_SECTIONS = {"SETS", "PARAMETERS", "VARIABLES", "EQUATIONS", "SOLVE"}
SUPPORTED_BACKENDS = {"gams", "python_nlp", "fixed_point", "validation"}
SUPPORTED_SOLVERS = {"path", "conopt", "ipopt", "default", "scipy", "fixed_point", "none"}
SYMBOL_PATTERN = re.compile(r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:\[(?P<indices>[A-Za-z0-9_,\s]+)\])?$")
ASSIGNMENT_PATTERN = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>.+)$")
SHOCK_PATTERN = re.compile(
    r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
    r"(?P<target>[A-Za-z_][A-Za-z0-9_]*(?:\[[A-Za-z0-9_,\s]+\])?)\s*"
    r"(?P<operator>[+-])\s*(?P<value>[-+]?\d+(?:\.\d+)?)$"
)


def normalize_identifier(value: str) -> str:
    """Normalize an SML identifier while preserving semantic names."""

    return str(value).strip().lower().replace("-", "_").replace(" ", "_")
