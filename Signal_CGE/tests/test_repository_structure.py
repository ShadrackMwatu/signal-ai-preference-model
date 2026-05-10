"""Import-safety tests for the Signal repository structure."""

from __future__ import annotations

import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "signal_cge",
        "signal_ai",
        "policy_ai",
        "sml_workbench",
        "learning",
    ],
)
def test_production_packages_import(module_name: str) -> None:
    """Production and active packages should remain importable."""

    assert importlib.import_module(module_name)


def test_app_imports_successfully() -> None:
    """The Hugging Face Gradio entrypoint should import without side effects that fail tests."""

    app = importlib.import_module("app")

    assert hasattr(app, "demo")


def test_cge_workbench_compatibility_imports() -> None:
    """Old CGE workbench imports should continue to resolve during migration."""

    calibration = importlib.import_module("cge_workbench.calibration.calibration_pipeline")
    model_equations = importlib.import_module("cge_workbench.model_core.model_equations")
    python_runner = importlib.import_module("cge_workbench.runners.python_runner")

    assert hasattr(calibration, "calibrate_signal_cge")
    assert hasattr(model_equations, "get_equation_registry")
    assert hasattr(python_runner, "PythonSAMRunner")


def test_signal_cge_canonical_modules_import() -> None:
    """The canonical CGE package should expose the main engine layers."""

    modules = [
        "signal_cge.calibration.calibration_pipeline",
        "signal_cge.model_core.model_equations",
        "signal_cge.solvers.sam_multiplier_solver",
        "signal_cge.diagnostics.model_readiness",
        "signal_cge.reporting.result_explainer",
        "signal_cge.workbench",
    ]

    for module_name in modules:
        assert importlib.import_module(module_name)
