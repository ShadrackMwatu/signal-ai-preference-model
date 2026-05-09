"""Repo-safe adaptive learning helpers for Signal CGE."""

from signal_cge.learning.adaptive_rules import apply_adaptive_prompt_rules
from signal_cge.learning.learning_registry import summarize_learning_memory
from signal_cge.learning.model_improvement_suggestions import generate_model_improvement_suggestions
from signal_cge.learning.simulation_memory import record_simulation_learning_event

__all__ = [
    "apply_adaptive_prompt_rules",
    "generate_model_improvement_suggestions",
    "record_simulation_learning_event",
    "summarize_learning_memory",
]
