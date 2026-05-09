"""Formatting helpers for Signal CGE reports."""

from __future__ import annotations


def format_warning_list(warnings: list[str]) -> str:
    return "\n".join(f"- {warning}" for warning in warnings) if warnings else "- No warnings."
