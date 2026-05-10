"""Blueprint modules for the future full Signal CGE equilibrium system."""

from .calibration_to_equilibrium import build_solver_ready_payload
from .closure_manager import validate_closure
from .equation_registry import get_equation_registry
from .model_gap_report import generate_full_cge_gap_report
from .parameter_registry import get_parameter_registry
from .variable_registry import get_variable_registry

__all__ = [
    "build_solver_ready_payload",
    "generate_full_cge_gap_report",
    "get_equation_registry",
    "get_parameter_registry",
    "get_variable_registry",
    "validate_closure",
]
