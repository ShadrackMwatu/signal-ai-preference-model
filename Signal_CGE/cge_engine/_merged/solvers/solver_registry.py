"""Registry for Signal solver backends."""

from __future__ import annotations

from .base_solver import BaseSolver
from .fixed_point_solver import FixedPointSolver
from .gams_solver import GamsSolver
from .python_nlp_solver import PythonNLPSolver


SOLVER_REGISTRY: dict[str, type[BaseSolver]] = {
    "gams": GamsSolver,
    "python_nlp": PythonNLPSolver,
    "fixed_point": FixedPointSolver,
    "validation": FixedPointSolver,
}


def get_solver(name: str) -> BaseSolver:
    key = str(name or "gams").lower()
    if key not in SOLVER_REGISTRY:
        raise ValueError(f"Unknown solver backend: {name}")
    return SOLVER_REGISTRY[key]()


def available_solvers() -> list[str]:
    return sorted(SOLVER_REGISTRY)
