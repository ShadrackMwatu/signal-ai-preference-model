import unittest
from pathlib import Path

from src.data_ingestion import (
    DEFAULT_SYNTHETIC_DATA_PATH,
    CATEGORIES,
    SyntheticDataConfig,
    generate_synthetic_examples,
    ingest_preferences,
    summarize_examples,
    write_synthetic_dataset,
)


class DataIngestionTests(unittest.TestCase):
    def test_synthetic_generation_is_deterministic(self) -> None:
        config = SyntheticDataConfig(users_per_segment=3, items_per_category=4, seed=42)

        first = generate_synthetic_examples(config)
        second = generate_synthetic_examples(config)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 192)
        self.assertEqual({example.label for example in first}, {0, 1})
        self.assertEqual({example.category for example in first}, set(CATEGORIES))

    def test_ingest_preferences_reads_generated_dataset(self) -> None:
        examples = ingest_preferences(DEFAULT_SYNTHETIC_DATA_PATH, generate_if_missing=False)
        summary = summarize_examples(examples)

        self.assertEqual(summary["examples"], 192)
        self.assertEqual(summary["categories"], 4)
        self.assertGreater(summary["positive_rate"], 0)
        self.assertLess(summary["positive_rate"], 1)

    def test_write_synthetic_dataset_creates_csv(self) -> None:
        output_path = Path("tests/_tmp/module1_synthetic_preferences.csv")
        config = SyntheticDataConfig(users_per_segment=2, items_per_category=4, seed=99)

        examples = write_synthetic_dataset(output_path, config=config)
        ingested = ingest_preferences(output_path, generate_if_missing=False)

        self.assertTrue(output_path.exists())
        self.assertEqual(ingested, examples)
        self.assertEqual(len(ingested), 128)


if __name__ == "__main__":
    unittest.main()
