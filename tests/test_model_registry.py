from __future__ import annotations

import unittest
from pathlib import Path

from ml.model_registry import ModelRegistry


class ModelRegistryTests(unittest.TestCase):
    def test_register_and_fetch_latest_model(self) -> None:
        scratch = Path("tests") / "_scratch" / "model_registry"
        scratch.mkdir(parents=True, exist_ok=True)
        registry_path = scratch / "registry_test_case.json"
        if registry_path.exists():
            registry_path.unlink()
        registry = ModelRegistry(registry_path)
        first = registry.register_model(
            model_name="demo",
            model_type="classification",
            dataset_used="synthetic",
            performance={"accuracy": 0.9},
            file_path="model-v1.joblib",
        )
        second = registry.register_model(
            model_name="demo",
            model_type="classification",
            dataset_used="synthetic",
            performance={"accuracy": 0.95},
            file_path="model-v2.joblib",
        )
        latest = registry.latest_model("demo")

        self.assertEqual(first.version, 1)
        self.assertEqual(second.version, 2)
        self.assertIsNotNone(latest)
        self.assertEqual(latest["file_path"], "model-v2.joblib")


if __name__ == "__main__":
    unittest.main()
