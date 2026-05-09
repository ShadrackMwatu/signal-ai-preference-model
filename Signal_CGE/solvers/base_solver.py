"""Solver abstraction for Signal execution backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseSolver(ABC):
    """Common solver interface for production and experimental backends."""

    name = "base"
    production_grade = False

    @abstractmethod
    def solve(self, model_spec: Any, data: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Solve a model specification using backend-specific data and options."""
