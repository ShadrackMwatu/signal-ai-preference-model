import unittest

from signal_learning.feedback_collector import user_feedback
from signal_learning.pattern_extractor import extract_patterns, recurring_issue_summary


class SignalLearningPatternExtractorTests(unittest.TestCase):
    def test_extracts_recurring_patterns_from_feedback(self) -> None:
        feedback = [
            user_feedback("run001", "sam_imbalance", "bad row", "fixed row", "Balance account.", 0.8).to_dict(),
            user_feedback("run002", "sam_imbalance", "bad col", "fixed col", "Balance account.", 0.8).to_dict(),
            user_feedback("run003", "gams_error", "uncontrolled set", "add index", "Fix indexing.", 0.85).to_dict(),
        ]

        patterns = extract_patterns({"feedback": feedback}, min_occurrences=2)
        summary = recurring_issue_summary({"feedback": feedback})

        self.assertEqual(len(patterns), 1)
        self.assertEqual(patterns[0].issue_type, "sam_imbalance")
        self.assertIn("recommended_action", summary["recurring_issues"][0])


if __name__ == "__main__":
    unittest.main()
