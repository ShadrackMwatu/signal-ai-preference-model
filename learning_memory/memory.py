"""High-level learning-memory capture for Signal model runs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .pattern_extractor import extract_diagnostics, extract_error_patterns, extract_result_patterns
from .rule_engine import recommendations_for_patterns, summarize_memory
from .schema import RunMemory, utc_now
from .store import LearningMemoryStore


def build_run_memory(run_result: dict[str, Any]) -> RunMemory:
    """Build a privacy-safe memory record from a run result."""

    error_patterns = extract_error_patterns(run_result)
    result_patterns = extract_result_patterns(run_result)
    recommendations = recommendations_for_patterns(error_patterns + result_patterns)
    return RunMemory(
        run_id=str(run_result.get("run_id", "")),
        timestamp=utc_now(),
        status=str(run_result.get("status", "")),
        requested_backend=str(run_result.get("requested_backend", "")),
        actual_backend=str(run_result.get("backend", "")),
        model_name=str(run_result.get("model_name", "")),
        error_patterns=error_patterns,
        result_patterns=result_patterns,
        diagnostics=extract_diagnostics(run_result),
        recommendations=recommendations,
    )


def capture_run_memory(run_result: dict[str, Any], memory_path: str | Path) -> dict[str, object]:
    """Persist run memory and return a compact memory summary."""

    store = LearningMemoryStore(memory_path)
    memory = build_run_memory(run_result)
    store.append(memory)
    summary = summarize_memory(store.load())
    return {
        "memory_path": str(Path(memory_path)),
        "latest_memory": memory.to_dict(),
        "summary": summary,
    }
