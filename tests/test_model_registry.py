from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ml.model_registry import ModelRegistry


TMP_ROOT = Path("tests") / "_tmp"


class ModelRegistryTests(unittest.TestCase):
    def test_register_and_fetch_latest_model(self) -> None:
        TMP_ROOT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TMP_ROOT) as tmp:
            registry = ModelRegistry(Path(tmp) / "registry.json")
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
