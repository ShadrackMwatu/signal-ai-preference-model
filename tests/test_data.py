import unittest
from pathlib import Path

from src.data import load_examples, save_examples
from src.schemas import PreferenceExample


class DataTests(unittest.TestCase):
    def test_load_examples_reads_csv(self) -> None:
        examples = load_examples(Path("data/sample_preferences.csv"))

        self.assertEqual(len(examples), 12)
        self.assertEqual(examples[0].user_id, "user_001")
        self.assertEqual(examples[0].label, 1)

    def test_save_examples_round_trips(self) -> None:
        temp_dir = Path("tests/_tmp")
        temp_dir.mkdir(exist_ok=True)
        path = temp_dir / "examples.csv"
        examples = [
            PreferenceExample(
                user_id="user_1",
                item_id="item_1",
                category="analytics",
                price=10.0,
                rating=4.0,
                popularity=0.5,
                label=1,
            )
        ]

        save_examples(path, examples)

        self.assertEqual(load_examples(path), examples)


if __name__ == "__main__":
    unittest.main()
