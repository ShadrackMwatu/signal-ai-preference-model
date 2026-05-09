"""Load canonical Signal CGE reference documents without external dependencies."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_ROOT = REPO_ROOT / "Documentation" / "signal_cge_reference"
CANONICAL_MODEL_ROOT = REPO_ROOT / "models" / "canonical"
MODEL_PROFILE_PATH = CANONICAL_MODEL_ROOT / "signal_cge_master" / "model_profile.yaml"


def load_reference_text(relative_path: str) -> str:
    """Load a text reference file from `Documentation/signal_cge_reference/`."""

    path = (REFERENCE_ROOT / relative_path).resolve()
    if REFERENCE_ROOT.resolve() not in path.parents and path != REFERENCE_ROOT.resolve():
        raise ValueError("Reference path must stay within the Signal CGE reference directory.")
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def list_reference_documents() -> list[dict[str, Any]]:
    """Return a lightweight index of available canonical reference documents."""

    documents: list[dict[str, Any]] = []
    for path in sorted(REFERENCE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        documents.append(
            {
                "path": str(path.relative_to(REPO_ROOT)),
                "section": path.parent.name,
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
            }
        )
    return documents


def _parse_scalar(value: str) -> Any:
    """Parse a constrained YAML scalar used by the canonical model profile."""

    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value in {"[]", "{}"}:
        return ast.literal_eval(value)
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the simple top-level YAML shape used by `model_profile.yaml`.

    This parser intentionally supports only top-level scalar keys and top-level
    lists. It keeps the Hugging Face app free of an additional YAML dependency.
    """

    parsed: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            parsed.setdefault(current_key, []).append(_parse_scalar(stripped[2:]))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            parsed[current_key] = [] if value == "" else _parse_scalar(value)
    return parsed


def load_model_profile(path: str | Path = MODEL_PROFILE_PATH) -> dict[str, Any]:
    """Load the canonical Signal CGE model profile."""

    profile_path = Path(path)
    if not profile_path.exists():
        raise FileNotFoundError(profile_path)
    return parse_simple_yaml(profile_path.read_text(encoding="utf-8"))
