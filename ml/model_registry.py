"""Simple JSON model registry for Signal ML artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_REGISTRY_PATH = Path("models_ml") / "metadata" / "model_registry.json"


@dataclass(frozen=True)
class ModelRecord:
    """Metadata for a trained Signal model."""

    model_name: str
    model_type: str
    training_date: str
    dataset_used: str
    performance: dict[str, Any]
    version: int
    file_path: str
    notes: str = ""


class ModelRegistry:
    """Persist model metadata to a local JSON registry."""

    def __init__(self, path: str | Path = DEFAULT_REGISTRY_PATH) -> None:
        self.path = Path(path)

    def list_models(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8")).get("models", [])

    def register_model(
        self,
        model_name: str,
        model_type: str,
        dataset_used: str,
        performance: dict[str, Any],
        file_path: str,
        notes: str = "",
    ) -> ModelRecord:
        models = self.list_models()
        next_version = max(
            [int(record.get("version", 0)) for record in models if record.get("model_name") == model_name],
            default=0,
        ) + 1
        record = ModelRecord(
            model_name=model_name,
            model_type=model_type,
            training_date=datetime.now(UTC).isoformat(),
            dataset_used=dataset_used,
            performance=performance,
            version=next_version,
            file_path=file_path,
            notes=notes,
        )
        models.append(asdict(record))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"models": models}, indent=2, sort_keys=True), encoding="utf-8")
        return record

    def latest_model(self, model_name: str) -> dict[str, Any] | None:
        matches = [record for record in self.list_models() if record.get("model_name") == model_name]
        if not matches:
            return None
        return sorted(matches, key=lambda record: int(record.get("version", 0)))[-1]
