"""Source registry loading for Open Signals aggregate ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

REGISTRY_PATH = Path("Behavioral_Signals_AI/config/source_registry.yaml")


def load_ingestion_source_registry(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load source registry without PyYAML, accepting simple list-of-maps YAML."""
    target = Path(path or REGISTRY_PATH)
    if not target.exists():
        return []
    sources: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw_line in target.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line == "sources:" or line.startswith("#"):
            continue
        if line.startswith("- "):
            if current:
                sources.append(_normalize_source(current))
            current = {}
            line = line[2:].strip()
        if ":" not in line or current is None:
            continue
        key, value = line.split(":", 1)
        current[key.strip()] = _coerce(value.strip())
    if current:
        sources.append(_normalize_source(current))
    return sources


def _normalize_source(source: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(source)
    source_name = str(normalized.get("source_name") or normalized.get("name") or "unknown_source")
    env_var = str(normalized.get("env_var") or normalized.get("environment_key") or "")
    normalized.setdefault("source_name", source_name)
    normalized.setdefault("name", source_name)
    normalized.setdefault("source_type", "official_statistics")
    normalized.setdefault("enabled", False)
    normalized.setdefault("requires_api_key", False)
    normalized.setdefault("env_var", env_var)
    normalized.setdefault("environment_key", env_var)
    normalized.setdefault("update_frequency_seconds", 3600)
    normalized.setdefault("privacy_level", "public_aggregate")
    normalized.setdefault("kenya_relevance_prior", 50)
    normalized.setdefault("reliability_prior", 50)
    return normalized


def _coerce(value: str) -> Any:
    value = value.strip().strip('"').strip("'")
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value == "":
        return ""
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
