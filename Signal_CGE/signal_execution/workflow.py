"""Convenience workflow entrypoints for Signal execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .runner import SignalRunner


def run_workflow(sml_path: str | Path = "signal_modeling_language/examples/basic_cge.sml") -> dict[str, Any]:
    return SignalRunner().run(sml_path)
