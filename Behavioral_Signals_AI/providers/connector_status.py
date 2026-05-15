"""Connector status diagnostics for aggregate/public source readiness."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(os.getenv("SIGNAL_SOURCE_REGISTRY_PATH", "Behavioral_Signals_AI/config/source_registry.yaml"))


def load_source_registry(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load the lightweight YAML source registry without requiring PyYAML."""
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
                sources.append(current)
            current = {}
            line = line[2:].strip()
        if ":" not in line or current is None:
            continue
        key, value = line.split(":", 1)
        current[key.strip()] = _coerce_yaml_value(value.strip())
    if current:
        sources.append(current)
    return sources


def connector_status_report(path: str | Path | None = None) -> dict[str, Any]:
    sources = load_source_registry(path)
    rows = []
    live_available = 0
    enabled_count = 0
    for source in sources:
        enabled = bool(source.get("enabled"))
        requires_key = bool(source.get("requires_api_key"))
        env_key = str(source.get("environment_key") or "")
        has_credentials = (not requires_key) or bool(env_key and os.getenv(env_key))
        status = "available" if enabled and has_credentials else "missing credentials" if enabled and requires_key else "using fallback" if enabled else "disabled"
        if enabled:
            enabled_count += 1
        if status == "available":
            live_available += 1
        rows.append(
            {
                "source": source.get("name"),
                "enabled": enabled,
                "requires_api_key": requires_key,
                "status": status,
                "last_successful_fetch": None,
                "update_frequency_seconds": source.get("update_frequency_seconds"),
                "reliability_prior": source.get("reliability_prior"),
                "kenya_relevance_prior": source.get("kenya_relevance_prior"),
            }
        )
    overall = "available" if live_available else "using fallback" if enabled_count else "failed"
    return {"generated_at": datetime.now(UTC).isoformat(), "overall_status": overall, "sources": rows}


def _coerce_yaml_value(value: str) -> Any:
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
