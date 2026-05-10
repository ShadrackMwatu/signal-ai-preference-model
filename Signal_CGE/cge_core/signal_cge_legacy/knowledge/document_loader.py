"""Load canonical Signal CGE reference documents without external dependencies."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
REFERENCE_ROOT = REPO_ROOT / "Documentation" / "signal_cge_reference"
CANONICAL_MODEL_ROOT = REPO_ROOT / "Signal_CGE" / "models" / "canonical"
MODEL_PROFILE_PATH = CANONICAL_MODEL_ROOT / "signal_cge_master" / "model_profile.yaml"
KNOWLEDGE_BASE_PATH = REPO_ROOT / "Documentation" / "SIGNAL_CGE_KNOWLEDGE_BASE.md"
ADDITIONAL_KNOWLEDGE_PATHS = [
    REPO_ROOT / "Documentation" / "SIGNAL_CGE_MODEL_STRUCTURE.md",
    REPO_ROOT / "Documentation" / "SIGNAL_CGE_REORGANIZATION_PLAN.md",
    REPO_ROOT / "Documentation" / "SIGNAL_CGE_REPO_KNOWLEDGE_INTEGRATION.md",
]


def _repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


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
                "path": _repo_relative(path),
                "section": path.parent.name,
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
            }
        )
    return documents


def list_repo_knowledge_sources() -> list[dict[str, Any]]:
    """Return all repo-stored knowledge sources used by the adaptive engine."""

    sources = list_reference_documents()
    for path in [MODEL_PROFILE_PATH, KNOWLEDGE_BASE_PATH, *ADDITIONAL_KNOWLEDGE_PATHS]:
        if path.exists():
            sources.append(
                {
                    "path": _repo_relative(path),
                    "section": path.parent.name,
                    "extension": path.suffix.lower(),
                    "size_bytes": path.stat().st_size,
                }
            )
    for path in sorted(CANONICAL_MODEL_ROOT.rglob("*")):
        if path.is_file():
            sources.append(
                {
                    "path": _repo_relative(path),
                    "section": "canonical_models",
                    "extension": path.suffix.lower(),
                    "size_bytes": path.stat().st_size,
                }
            )
    return sources


def load_knowledge_base() -> str:
    """Load the implementation knowledge base."""

    return KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8")


def load_reference_bundle() -> dict[str, str]:
    """Load key text references by relative path."""

    bundle: dict[str, str] = {"SIGNAL_CGE_KNOWLEDGE_BASE.md": load_knowledge_base()}
    for document in list_reference_documents():
        if document["extension"] != ".md":
            continue
        relative = Path(document["path"]).relative_to("Documentation/signal_cge_reference")
        bundle[str(relative).replace("\\", "/")] = load_reference_text(str(relative))
    return bundle


def load_repo_knowledge_bundle() -> dict[str, str]:
    """Load lightweight text knowledge from repo documentation and canonical profiles."""

    bundle = load_reference_bundle()
    for path in [MODEL_PROFILE_PATH, *ADDITIONAL_KNOWLEDGE_PATHS]:
        if path.exists() and path.suffix.lower() in {".md", ".yaml", ".yml", ".txt"}:
            bundle[str(path.relative_to(REPO_ROOT)).replace("\\", "/")] = path.read_text(encoding="utf-8")
    return bundle


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
