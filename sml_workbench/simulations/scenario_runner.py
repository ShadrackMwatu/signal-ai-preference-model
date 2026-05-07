"""Prepare future-ready simulation bundles for SML scenarios."""

from __future__ import annotations

from typing import Any

from sml_workbench.exporters.gams_exporter import export_to_gams
from sml_workbench.exporters.pyomo_exporter import export_to_pyomo
from sml_workbench.validators.sml_validator import validate_sml


def prepare_simulation_bundle(parsed: dict[str, Any]) -> dict[str, Any]:
    validation = validate_sml(parsed)
    return {
        "validation": validation,
        "gams_preview": export_to_gams(parsed),
        "pyomo_preview": export_to_pyomo(parsed),
        "status": "ready" if validation["valid"] else "validation_failed",
        "message": "Simulation bundle prepared for future CGE/SAM execution workflows.",
    }
