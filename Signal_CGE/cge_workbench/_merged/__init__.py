"""Compatibility package for the canonical `signal_cge` package.

New code should import from `signal_cge`. This package remains during the
transition so existing Signal app and test imports continue to work.
"""

from signal_cge.scenarios.scenario_schema import ScenarioSpec, parse_scenario_prompt
from signal_cge.solvers.python_runner import PythonSAMRunner
from signal_cge.solvers.runner_interface import ModelRunResult, RunnerConfig, SignalModelRunner

__all__ = [
    "ModelRunResult",
    "PythonSAMRunner",
    "RunnerConfig",
    "ScenarioSpec",
    "SignalModelRunner",
    "parse_scenario_prompt",
]
