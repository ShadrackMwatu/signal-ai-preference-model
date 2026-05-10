"""Formal Signal CGE model-core architecture.

The model core exposes transparent block registries, placeholder equations,
calibration helpers, and closure validation used by future full-equilibrium
solver pathways. These modules do not run a full CGE solve yet.
"""

from .calibration import calibrate_from_sam
from .closure_system import validate_closure_rules
from .model_equations import get_equation_registry

__all__ = ["calibrate_from_sam", "get_equation_registry", "validate_closure_rules"]
