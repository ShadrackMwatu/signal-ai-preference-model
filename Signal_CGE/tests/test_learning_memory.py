import unittest
import uuid
from pathlib import Path

from learning_memory.memory import build_run_memory, capture_run_memory
from learning_memory.store import LearningMemoryStore
from signal_execution.config import ExecutionConfig
from signal_execution.runner import SignalRunner


class LearningMemoryTests(unittest.TestCase):
    def test_run_memory_extracts_patterns_and_recommendations(self) -> None:
        memory = build_run_memory(
            {
                "run_id": "abc123",
                "status": "ok",
                "requested_backend": "gams",
                "backend": "python_nlp",
                "model_name": "kenya_cge",
                "message": "GAMS backend unavailable; using experimental Python backend or validation-only mode. Experimental Python NLP backend; not production-grade.",
                "validation": {"errors": [], "warnings": [], "sam_balanced": True},
                "metrics": {"gdp_impact": 1.2, "household_welfare_impact": 0.6, "government_revenue_impact": 0.3},
            }
        )

        self.assertIn("gams_unavailable", memory.error_patterns)
        self.assertIn("experimental_solver_used", memory.error_patterns)
        self.assertIn("positive_gdp_response", memory.result_patterns)
        self.assertTrue(memory.recommendations)

    def test_learning_memory_store_round_trips_jsonl(self) -> None:
        path = Path(f"tests/_tmp/learning_memory/memory_{uuid.uuid4().hex}.jsonl")
        summary = capture_run_memory(
            {
                "run_id": "def456",
                "status": "ok",
                "requested_backend": "gams",
                "backend": "python_nlp",
                "model_name": "kenya_cge",
                "message": "GAMS backend unavailable; using experimental Python backend or validation-only mode.",
                "validation": {"errors": [], "warnings": [], "sam_balanced": True},
                "metrics": {"gdp_impact": 0.2, "household_welfare_impact": 0.1, "government_revenue_impact": 0.0},
            },
            path,
        )
        records = LearningMemoryStore(path).load()

        self.assertEqual(len(records), 1)
        self.assertEqual(summary["summary"]["runs_observed"], 1)
        self.assertEqual(records[0].run_id, "def456")

    def test_runner_attaches_learning_memory_summary(self) -> None:
        runner = SignalRunner(
            ExecutionConfig(
                output_dir=Path("tests/_tmp/learning_runner_outputs"),
                memory_path=Path("tests/_tmp/learning_runner_outputs/memory.jsonl"),
                learning_store_path=Path("tests/_tmp/learning_runner_outputs/learning_store.json"),
                learning_version_root=Path("tests/_tmp/learning_runner_outputs/learning_versions"),
            )
        )
        result = runner.run("signal_modeling_language/examples/basic_cge.sml")

        self.assertIn("learning_memory", result)
        self.assertTrue(Path(result["learning_memory"]["memory_path"]).exists())
        self.assertGreaterEqual(result["learning_memory"]["summary"]["runs_observed"], 1)
        self.assertIn("recommended_template_rules", result["learning_memory"]["summary"])


if __name__ == "__main__":
    unittest.main()
