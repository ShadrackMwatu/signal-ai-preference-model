"""Execution configuration for Signal CGE runs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from signal_learning.memory_schema import LearningMode


@dataclass(frozen=True)
class ExecutionConfig:
    project_root: Path = Path(".")
    output_dir: Path = Path("outputs")
    memory_path: Path = Path("outputs") / "learning_memory.jsonl"
    learning_store_path: Path = Path("outputs") / "signal_learning_store.json"
    learning_mode: LearningMode = "recommend"
    learning_version_root: Path = Path("learning_versions")
    default_sml_path: Path = Path("signal_modeling_language/examples/basic_cge.sml")
    balance_tolerance: float = 0.01

    def resolve(self, path: str | Path) -> Path:
        candidate = Path(path)
        return candidate if candidate.is_absolute() else self.project_root / candidate
