"""Closed registry of safe internal Open Signals tools."""

from __future__ import annotations

from typing import Any

from Behavioral_Signals_AI.tools.tool_schemas import TOOL_SCHEMAS, ToolSchema


def list_tools() -> list[dict[str, Any]]:
    """Return tool descriptions safe to pass to an LLM or deterministic router."""
    return [schema.to_dict() for schema in TOOL_SCHEMAS.values()]


def get_tool(name: str) -> ToolSchema | None:
    return TOOL_SCHEMAS.get(str(name or ""))


def registered_tool_names() -> set[str]:
    return set(TOOL_SCHEMAS)
