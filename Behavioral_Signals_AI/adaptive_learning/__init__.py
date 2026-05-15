from .adaptive_learning import aggregate_feedback_for_retraining, record_feedback
"""Adaptive learning loop for Behavioral Signals AI."""

from .learning_registry import summarize_learning_state
from .prediction_memory import save_prediction_snapshot, load_prediction_memory
from .online_calibrator import calibrate_prediction

__all__ = ["summarize_learning_state", "save_prediction_snapshot", "load_prediction_memory", "calibrate_prediction", "aggregate_feedback_for_retraining", "log_feedback", "should_trigger_retraining"]

def log_feedback(*args, **kwargs):
    """Backward-compatible alias for aggregate feedback logging."""

    return record_feedback(*args, **kwargs)


def should_trigger_retraining(*args, **kwargs) -> bool:
    """Compatibility placeholder; adaptive weighting is active, batch retraining is manual."""

    return False