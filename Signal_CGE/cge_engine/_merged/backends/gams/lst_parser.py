"""Parse GAMS .lst logs for common model and solver errors."""

from __future__ import annotations

from pathlib import Path


COMMON_ERROR_PATTERNS = {
    "****": "GAMS compilation or execution error marker found.",
    "uncontrolled set": "Uncontrolled set entered as constant.",
    "domain violation": "Domain violation; check set membership and indexed symbols.",
    "infeasible": "Solver reported infeasibility.",
    "execution error": "GAMS execution error.",
}


def parse_lst(path: str | Path) -> dict[str, object]:
    source = Path(path)
    if not source.exists():
        return {"available": False, "errors": [f"LST file not found: {source}"]}
    text = source.read_text(encoding="utf-8", errors="ignore")
    errors = [
        message
        for pattern, message in COMMON_ERROR_PATTERNS.items()
        if pattern.lower() in text.lower()
    ]
    return {"available": True, "errors": errors, "line_count": len(text.splitlines())}
