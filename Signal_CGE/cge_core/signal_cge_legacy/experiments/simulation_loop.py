"""Simulation-loop blueprint for baseline and policy experiments."""

from __future__ import annotations

from typing import Any

from .experiment_runner import run_prototype_experiment


def run_simulation_loop(prompts: list[str]) -> dict[str, Any]:
    return {
        "status": "prototype_loop",
        "runs": [run_prototype_experiment(prompt) for prompt in prompts],
        "future_loop_steps": ["solve baseline", "apply shock", "solve policy", "collect differences"],
    }
