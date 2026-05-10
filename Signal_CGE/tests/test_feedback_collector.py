import unittest
from pathlib import Path

from signal_learning.feedback_collector import collect_lst_feedback, collect_run_feedback, user_feedback


class FeedbackCollectorTests(unittest.TestCase):
    def test_collects_run_feedback_from_solver_and_validation(self) -> None:
        entries = collect_run_feedback(
            {
                "run_id": "run002",
                "status": "ok",
                "message": "GAMS backend unavailable; using experimental Python backend or validation-only mode. Experimental Python NLP backend; not production-grade.",
                "validation": {"errors": [], "warnings": ["GAMS backend selected with default solver"], "sam_balanced": True},
            }
        )
        issue_types = {entry.issue_type for entry in entries}

        self.assertIn("gams_unavailable", issue_types)
        self.assertIn("experimental_solver", issue_types)
        self.assertIn("successful_model_run", issue_types)
        self.assertTrue(all(entry.evidence.source_run == "run002" for entry in entries))

    def test_collects_gams_lst_feedback(self) -> None:
        path = Path("tests/_tmp/sample.lst")
        path.write_text("**** uncontrolled set entered as constant", encoding="utf-8")
        entries = collect_lst_feedback("run003", path)

        self.assertTrue(all(entry.issue_type == "gams_error" for entry in entries))
        self.assertIn("indexing", " ".join(entry.lesson_learned.lower() for entry in entries))

    def test_user_feedback_preserves_source(self) -> None:
        feedback = user_feedback(
            "run004",
            "closure_inconsistency",
            "government savings fixed",
            "government savings endogenous",
            "Tax shocks need government balance closure review.",
            source="user_edit",
        )

        self.assertEqual(feedback.source, "user_edit")
        self.assertEqual(feedback.evidence.validation_status, "user_reviewed")


if __name__ == "__main__":
    unittest.main()
