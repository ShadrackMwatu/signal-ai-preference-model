"""Local JSONL storage for Signal learning memory."""

from __future__ import annotations

import json
from pathlib import Path

from .schema import RunMemory


DEFAULT_MEMORY_PATH = Path("outputs") / "learning_memory.jsonl"


class LearningMemoryStore:
    """Append-only local memory store for aggregate run diagnostics."""

    def __init__(self, path: str | Path = DEFAULT_MEMORY_PATH) -> None:
        self.path = Path(path)

    def append(self, memory: RunMemory) -> str:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(memory.to_dict(), sort_keys=True) + "\n")
        return str(self.path)

    def load(self) -> list[RunMemory]:
        if not self.path.exists():
            return []
        memories: list[RunMemory] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            values = json.loads(line)
            memories.append(
                RunMemory(
                    run_id=str(values["run_id"]),
                    timestamp=str(values["timestamp"]),
                    status=str(values["status"]),
                    requested_backend=str(values["requested_backend"]),
                    actual_backend=str(values["actual_backend"]),
                    model_name=str(values["model_name"]),
                    error_patterns=list(values.get("error_patterns", [])),
                    result_patterns=list(values.get("result_patterns", [])),
                    diagnostics=list(values.get("diagnostics", [])),
                    recommendations=list(values.get("recommendations", [])),
                )
            )
        return memories
