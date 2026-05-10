import unittest
import uuid
from pathlib import Path

from signal_learning.feedback_collector import user_feedback
from signal_learning.learning_store import LearningStore


class LearningStoreTests(unittest.TestCase):
    def test_store_persists_feedback_snapshot_and_report(self) -> None:
        path = Path(f"tests/_tmp/signal_learning/store_{uuid.uuid4().hex}.json")
        store = LearningStore(path)
        feedback = user_feedback(
            run_id="run001",
            issue_type="sam_imbalance",
            source="user_correction",
            original_value="agriculture imbalance",
            corrected_value="review agriculture column",
            lesson_learned="Check agriculture account mapping.",
            confidence_score=0.8,
        )

        store.add_feedback(feedback)
        store.add_run_snapshot(
            {
                "run_id": "run001",
                "model_name": "kenya_cge",
                "sam_structure": {"accounts": ["agriculture", "households"]},
                "account_classifications": {"sectors": ["agriculture"]},
                "calibration_patterns": {"has_output_shares": True},
                "model_equations": ["market_clearing"],
                "closure_rules": {"numeraire": "consumer_price_index"},
                "shock_definitions": [{"name": "vat"}],
                "gams_errors": [],
                "solver_failures": [],
                "successful_model_run": False,
                "final_report": "outputs/report.md",
                "validation_status": "valid",
                "raw_sam_cells": "must not persist",
            }
        )
        store.add_report("run001", "tests/_tmp/report.md", {"feedback_entries": 1})
        data = store.load()

        self.assertEqual(len(data["feedback"]), 1)
        self.assertEqual(data["feedback"][0]["source"], "user_correction")
        self.assertEqual(data["run_snapshots"][0]["sam_structure"]["accounts"], ["agriculture", "households"])
        self.assertNotIn("raw_sam_cells", data["run_snapshots"][0])
        self.assertEqual(len(store.lessons()), 1)


if __name__ == "__main__":
    unittest.main()
