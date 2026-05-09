"""Canonical Signal CGE package.

`signal_cge` is the unified home for the economic model engine, calibration,
diagnostics, solvers, scenarios, dynamics, and reporting. The older
`cge_workbench` package remains available as a compatibility layer during the
transition.
"""

from .model_registry import get_model_registry
from .workbench import run_chat_scenario

__all__ = ["get_model_registry", "run_chat_scenario"]
