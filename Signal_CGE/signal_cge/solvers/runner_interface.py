"""Runner abstractions for Signal policy simulation backends."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


@dataclass(slots=True)
class RunnerConfig:
    model_type: str = "SAM multiplier"
    output_dir: Path = Path("cge_workbench/outputs")
    model_path: Path | None = None
    sam_path: Path | None = None
    endogenous_accounts: list[str] | None = None
    exogenous_accounts: list[str] | None = None


@dataclass(slots=True)
class ModelRunResult:
    success: bool
    backend: str
    scenario: dict[str, Any]
    diagnostics: dict[str, Any] = field(default_factory=dict)
    results: dict[str, Any] = field(default_factory=dict)
    logs: list[str] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)
    message: str = ""


class SignalModelRunner(Protocol):
    """Common interface for GAMS, Python, and future open-source CGE runners."""

    def run(self, scenario: dict[str, Any]) -> ModelRunResult:
        """Execute a scenario and return structured diagnostics/results."""
