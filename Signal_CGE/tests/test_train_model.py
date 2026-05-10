from __future__ import annotations

import json
import unittest
from pathlib import Path

import joblib

from data.synthetic.generate_synthetic_signal_data import generate_synthetic_signal_data
from train_model import train_signal_model


class TrainModelTests(unittest.TestCase):
    def test_training_creates_latest_and_versioned_artifacts(self) -> None:
        scratch = Path("tests") / "_scratch" / "phase2_train"
        scratch.mkdir(parents=True, exist_ok=True)
        data_path = scratch / "signal_training_data.csv"
        model_path = scratch / "model.pkl"
        metadata_path = scratch / "metadata.json"

        generate_synthetic_signal_data(data_path, n_rows=240, random_state=11)
        result = train_signal_model(data_path=data_path, model_path=model_path, metadata_path=metadata_path, random_state=11)

        self.assertTrue(model_path.exists())
        self.assertTrue(metadata_path.exists())
        artifact = joblib.load(model_path)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        version_dir = Path("Behavioral_Signals_AI") / "models" / "versions" / result.model_version

        self.assertIn("model", artifact)
        self.assertEqual(metadata["model_version"], result.model_version)
        self.assertTrue((version_dir / "model.pkl").exists())
        self.assertTrue((version_dir / "metadata.json").exists())


if __name__ == "__main__":
    unittest.main()
