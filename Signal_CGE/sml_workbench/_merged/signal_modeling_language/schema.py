"""Dataclasses for the Signal Modelling Language (SML)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class IndexedSymbol:
    """A variable or equation with optional index sets."""

    name: str
    indices: tuple[str, ...] = ()


@dataclass(frozen=True)
class ShockDefinition:
    """A named shock expression from the SML SHOCKS section."""

    name: str
    target: str
    operator: str
    value: float


@dataclass(frozen=True)
class SolveCommand:
    """Backend, model, and solver choices from the SML SOLVE section."""

    model: str
    backend: str = "gams"
    solver: str = "default"


@dataclass(frozen=True)
class OutputCommand:
    """Output paths requested by the SML OUTPUT section."""

    gdx: str | None = None
    excel: str | None = None
    report: str | None = None
    gams: str | None = None


@dataclass
class SMLModel:
    """Parsed Signal Modelling Language model specification."""

    sets: dict[str, list[str]] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    variables: list[IndexedSymbol] = field(default_factory=list)
    equations: list[IndexedSymbol] = field(default_factory=list)
    closure: dict[str, str] = field(default_factory=dict)
    shocks: list[ShockDefinition] = field(default_factory=list)
    solve: SolveCommand = field(default_factory=lambda: SolveCommand(model="signal_cge"))
    output: OutputCommand = field(default_factory=OutputCommand)
    source_path: str | None = None

    def symbol_names(self) -> set[str]:
        return {symbol.name for symbol in self.variables}.union({symbol.name for symbol in self.equations})
