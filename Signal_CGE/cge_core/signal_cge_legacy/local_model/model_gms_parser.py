"""Lightweight parser for Signal CGE GAMS model metadata."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def parse_model_gms_metadata(model_file: str | Path | None = None) -> dict[str, Any]:
    """Parse model.gms into safe structural metadata without requiring GAMS."""

    if model_file is None:
        from .local_model_detector import detect_local_signal_cge_model

        model_file = detect_local_signal_cge_model()["model_file"]
    path = Path(model_file)
    if not path.exists():
        return _empty_metadata(path, ["model.gms was not found."])
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    metadata = {
        "model_file": str(path),
        "model_file_exists": True,
        "folder_controls": _find_folder_controls(lines),
        "active_data_file_declarations": _find_data_files(lines),
        "declared_sets": _find_declared_names(lines, "sets?"),
        "declared_parameters": _find_declared_names(lines, "parameters?"),
        "declared_variables": _find_declared_names(lines, "variables?"),
        "declared_equations": _find_declared_names(lines, "equations?"),
        "include_files": _find_include_files(lines),
        "closure_references": _find_keywords(lines, ["closure", "numeraire", "savings", "exchange", "factor market"]),
        "solve_statement_type": _find_solve_type(lines),
        "model_name": _find_model_name(lines),
        "solver_options": _find_solver_options(lines),
        "model_structure_comments": _safe_structure_comments(lines),
        "warnings": [],
    }
    return metadata


def _empty_metadata(path: Path, warnings: list[str]) -> dict[str, Any]:
    return {
        "model_file": str(path),
        "model_file_exists": False,
        "folder_controls": [],
        "active_data_file_declarations": [],
        "declared_sets": [],
        "declared_parameters": [],
        "declared_variables": [],
        "declared_equations": [],
        "include_files": [],
        "closure_references": [],
        "solve_statement_type": "",
        "model_name": "",
        "solver_options": [],
        "model_structure_comments": [],
        "warnings": warnings,
    }


def _find_folder_controls(lines: list[str]) -> list[str]:
    return _unique(_sanitize(line) for line in lines if any(token in line.lower() for token in ["00_save", "00_save", "10_gdx", "20_data", "70_result"]))


def _find_data_files(lines: list[str]) -> list[str]:
    pattern = re.compile(r"[\w./\\-]+\.(?:xlsx|xls|csv|gdx)", re.IGNORECASE)
    found: list[str] = []
    for line in lines:
        if any(token in line.lower() for token in ["data", "sam", "xls", "xlsx", "csv", "gdx"]):
            found.extend(pattern.findall(line))
    return _unique(found)


def _find_declared_names(lines: list[str], keyword_pattern: str) -> list[str]:
    names: list[str] = []
    active = False
    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()
        if re.match(rf"^{keyword_pattern}\b", lower):
            active = True
            names.extend(_symbols_from_line(stripped))
            continue
        if active:
            names.extend(_symbols_from_line(stripped))
            if ";" in stripped:
                active = False
    return _unique(names)


def _symbols_from_line(line: str) -> list[str]:
    clean = line.split("*", 1)[0]
    return [match for match in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", clean) if match.lower() not in _reserved_words()]


def _find_include_files(lines: list[str]) -> list[str]:
    include_pattern = re.compile(r"\$(?:include|batinclude)\s+([^\s;]+)", re.IGNORECASE)
    return _unique(match.group(1) for line in lines for match in [include_pattern.search(line)] if match)


def _find_keywords(lines: list[str], keywords: list[str]) -> list[str]:
    return _unique(_sanitize(line) for line in lines if any(keyword in line.lower() for keyword in keywords))[:50]


def _find_solve_type(lines: list[str]) -> str:
    for line in lines:
        match = re.search(r"\bsolve\b.+?\busing\s+([A-Za-z0-9_]+)", line, flags=re.IGNORECASE)
        if match:
            return match.group(1).lower()
    return ""


def _find_model_name(lines: list[str]) -> str:
    for line in lines:
        match = re.search(r"\bmodel\s+([A-Za-z0-9_]+)", line, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return ""


def _find_solver_options(lines: list[str]) -> list[str]:
    return _unique(_sanitize(line) for line in lines if re.search(r"\b(option|solveopt|limrow|limcol|iterlim|reslim)\b", line, flags=re.IGNORECASE))[:50]


def _safe_structure_comments(lines: list[str]) -> list[str]:
    comments: list[str] = []
    blocked = ["http", "@", "copyright", "licence", "license", "commission", "joint", "contact", "distributed", "terms"]
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("*"):
            continue
        lower = stripped.lower()
        if any(term in lower for term in blocked):
            continue
        if any(term in lower for term in ["folder", "file", "command", "closure", "set", "parameter", "equation", "variable", "solve"]):
            comments.append(_sanitize(stripped))
    return _unique(comments)[:60]


def _sanitize(text: str) -> str:
    text = re.sub(r"https?://\S+", "[link removed]", text)
    text = re.sub(r"[\w.\-+]+@[\w.\-]+", "[email removed]", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _reserved_words() -> set[str]:
    return {"set", "sets", "parameter", "parameters", "variable", "variables", "equation", "equations", "positive", "free", "binary", "integer", "alias", "model", "all"}


def _unique(values) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        value = str(value).strip()
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result
