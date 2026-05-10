from __future__ import annotations

import unittest

from learning.ai_teaching.explainer import explain_concept


class LearningExplainerTests(unittest.TestCase):
    def test_learning_explainer_returns_readable_text(self) -> None:
        text = explain_concept("SML")

        self.assertIsInstance(text, str)
        self.assertIn("Signal Modelling Language", text)

    def test_unknown_concept_still_returns_helpful_text(self) -> None:
        text = explain_concept("unknown topic")

        self.assertIn("does not yet have a dedicated teaching note", text)


if __name__ == "__main__":
    unittest.main()
