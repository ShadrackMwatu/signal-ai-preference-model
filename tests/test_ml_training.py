from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from ml.model_registry import ModelRegistry
from ml.model_training import train_county_topic_clusterer, train_demand_classifier, train_regression_model


def _sample_frame(rows: int = 72) -> pd.DataFrame:
    records = []
    classes = ["Low", "Moderate", "High"]
    for index in range(rows):
        tier = index % 3
        likes = 10 + tier * 90 + index
        comments = 3 + tier * 20
        shares = 2 + tier * 12
        searches = 8 + tier * 100
        records.append(
            {
                "county": ["Nairobi", "Kisumu", "Turkana"][tier],
                "category": ["retail", "transport", "agriculture"][tier],
                "time_period": f"2026-Q{(index % 4) + 1}",
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "searches": searches,
                "views": 500 + tier * 100,
                "demand_class": classes[tier],
                "aggregate_demand_score": 0.2 + tier * 0.3,
            }
        )
    return pd.DataFrame(records)


class MLTrainingTests(unittest.TestCase):
    def test_classifier_regression_and_clustering_train(self) -> None:
        frame = _sample_frame()
        scratch = Path("tests") / "_scratch" / "ml_training"
        scratch.mkdir(parents=True, exist_ok=True)
        registry = ModelRegistry(scratch / "registry.json")
        classifier = train_demand_classifier(
            frame,
            output_dir=scratch,
            registry=registry,
            model_name="signal_demand_classifier_ml_training",
        )
        regressor = train_regression_model(
            frame,
            target_column="aggregate_demand_score",
            output_dir=scratch,
            registry=registry,
            model_name="signal_regression_model_ml_training",
        )
        clusterer = train_county_topic_clusterer(frame, n_clusters=3)
        self.assertTrue(Path(classifier["model_path"]).exists())
        self.assertGreaterEqual(classifier["metrics"]["accuracy"], 0.8)
        self.assertTrue(Path(regressor["model_path"]).exists())
        self.assertIn("rmse", regressor["metrics"])
        self.assertEqual(len(clusterer["labels"]), len(frame))
        self.assertEqual(classifier["prediction_source"], "trained ML model")


if __name__ == "__main__":
    unittest.main()
