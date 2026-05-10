"""Repo-safe adaptive learning helpers for Signal CGE."""

from .adaptive_rules import apply_adaptive_prompt_rules
from .learning_registry import summarize_learning_memory, write_learning_summary
from .model_improvement_suggestions import generate_model_improvement_suggestions
from .simulation_memory import record_simulation_learning_event
from .model_gap_detector import generate_model_gap_report
from .recommendation_engine import recommend_adaptive_next_simulations
from .scenario_pattern_learning import find_similar_simulations, learn_prompt_patterns

__all__ = [
    "apply_adaptive_prompt_rules",
    "generate_model_improvement_suggestions",
    "record_simulation_learning_event",
    "summarize_learning_memory",
]
