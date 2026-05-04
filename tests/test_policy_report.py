import unittest
from pathlib import Path

from policy_intelligence.report_generator import generate_policy_report
from signal_execution.config import ExecutionConfig
from signal_execution.runner import SignalRunner


class PolicyReportTests(unittest.TestCase):
    def test_policy_report_is_generated(self) -> None:
        result = {
            "run_id": "test_run",
            "status": "ok",
            "backend": "fixed_point",
            "message": "Experimental fixed-point fallback completed; not production-grade.",
            "metrics": {
                "gdp_impact": 1.2,
                "household_welfare_impact": 0.7,
                "sectoral_output_impact": 1.1,
                "employment_factor_income_impact": 0.5,
                "government_revenue_impact": 0.2,
                "trade_impact": 0.1,
                "distributional_impact": 0.05,
            },
        }
        path = generate_policy_report(result, "tests/_tmp/policy_report.md")

        self.assertTrue(Path(path).exists())
        self.assertIn("GDP impact", Path(path).read_text(encoding="utf-8"))

    def test_runner_generates_report_and_outputs(self) -> None:
        runner = SignalRunner(
            ExecutionConfig(
                output_dir=Path("tests/_tmp/runner_outputs"),
                memory_path=Path("tests/_tmp/runner_outputs/memory.jsonl"),
                learning_store_path=Path("tests/_tmp/runner_outputs/learning_store.json"),
                learning_version_root=Path("tests/_tmp/runner_outputs/learning_versions"),
            )
        )
        result = runner.run("signal_modeling_language/examples/basic_cge.sml")

        self.assertTrue(Path(result["report_path"]).exists())
        self.assertTrue(Path(result["gams_file"]).exists())
        self.assertIn("metrics", result)
        self.assertIn("GAMS backend unavailable", result["message"])


if __name__ == "__main__":
    unittest.main()
