"""Learning and adaptive-memory service for Signal CGE."""

from __future__ import annotations

from typing import Any

from Signal_CGE.signal_cge.learning.learning_registry import write_learning_summary
from Signal_CGE.signal_cge.learning.simulation_memory import record_simulation_learning_event



def persist_learning_event(payload: dict[str, Any]) -> dict[str, Any]:
    """Persist a simulation event and refresh summary outputs."""

    event = record_simulation_learning_event(payload)
    summary = write_learning_summary(limit=100)
    return {
        "event": event,
        "summary": summary,
    }
