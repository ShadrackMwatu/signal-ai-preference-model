import unittest
import uuid
from pathlib import Path

from signal_learning.adaptation_engine import generate_learning_report, propose_adaptations, write_adaptation_version
from signal_learning.feedback_collector import user_feedback


class AdaptationEngineTests(unittest.TestCase):
    def test_proposes_versioned_adaptations_from_patterns(self) -> None:
        data = {
            "feedback": [
                user_feedback("run001", "gams_unavailable", "missing gams", "use fallback", "Install GAMS.", 0.9).to_dict()
            ],
            "adaptations": [],
        }
        proposals = propose_adaptations(data, Path("tests/_tmp/adaptations"))
        manifest = write_adaptation_version(proposals[0], Path(f"tests/_tmp/adaptations_{uuid.uuid4().hex}"))

        self.assertEqual(proposals[0].version_id, "v001")
        self.assertEqual(proposals[0].risk_level, "low")
        self.assertTrue(Path(manifest).exists())

    def test_learning_report_is_written(self) -> None:
        proposal = propose_adaptations(
            {
                "feedback": [
                    user_feedback("run001", "experimental_solver", "fallback", "gams validation", "Use GAMS.", 0.9).to_dict()
                ],
                "adaptations": [],
            }
        )[0]
        path = generate_learning_report(
            {"run_id": "run001", "status": "ok", "requested_backend": "gams", "backend": "python_nlp"},
            [user_feedback("run001", "experimental_solver", "fallback", "gams validation", "Use GAMS.", 0.9).to_dict()],
            [proposal],
            [],
            Path("tests/_tmp/learning_report"),
        )

        self.assertTrue(Path(path).exists())
        self.assertIn("What Was Learned", Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
