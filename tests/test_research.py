import csv
import unittest
from pathlib import Path

from src.data import load_examples
from src.model import PreferenceModel
from src.research import cge_sam_row, export_cge_sam_csv
from src.schemas import PreferenceRequest


class ResearchOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PreferenceModel().train(load_examples(Path("data/sample_preferences.csv")))
        self.request = PreferenceRequest(
            user_id="user_001",
            item_id="dashboard_plus",
            category="analytics",
            price=24.0,
            rating=4.7,
            popularity=0.8,
        )

    def test_prediction_contains_research_metadata(self) -> None:
        prediction = self.model.predict(self.request)

        self.assertTrue(prediction.drivers)
        self.assertIn("preference", prediction.policy_signal)
        self.assertEqual(prediction.cge_sam_account, "DIGITAL_SERVICES")
        self.assertGreater(len(prediction.publication_notes), 0)

    def test_cge_sam_export_row_and_csv(self) -> None:
        prediction = self.model.predict(self.request)
        row = cge_sam_row(self.request, prediction, scenario_id="policy_scenario_1")
        export_path = Path("tests/_tmp/cge_sam_export.csv")

        export_cge_sam_csv(export_path, [row])

        with export_path.open(newline="", encoding="utf-8") as handle:
            exported_rows = list(csv.DictReader(handle))

        self.assertEqual(row["scenario_id"], "policy_scenario_1")
        self.assertEqual(row["sam_account"], "DIGITAL_SERVICES")
        self.assertEqual(exported_rows[0]["sam_account"], "DIGITAL_SERVICES")


if __name__ == "__main__":
    unittest.main()
