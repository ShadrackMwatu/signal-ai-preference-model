import unittest
import uuid
from pathlib import Path

from signal_learning.workflow import LEARNING_STAGES, run_learning_cycle


class LearningWorkflowTests(unittest.TestCase):
    def test_full_learning_cycle_reports_all_stages(self) -> None:
        root = Path(f"tests/_tmp/learning_cycle_{uuid.uuid4().hex}")
        result = run_learning_cycle(
            {
                "run_id": "cycle001",
                "status": "ok",
                "backend": "python_nlp",
                "requested_backend": "gams",
                "model_name": "kenya_cge",
                "message": "GAMS backend unavailable; using experimental Python backend or validation-only mode. Experimental Python NLP backend; not production-grade.",
                "validation": {"valid": True, "errors": [], "warnings": [], "sam_balanced": True},
                "calibration": {
                    "row_totals": {"agriculture": 10.0},
                    "account_classification": {"sectors": ["agriculture"]},
                    "output_shares": {"agriculture": 1.0},
                    "total_activity": 10.0,
                },
                "equations": [{"equation": "market_clearing"}],
                "closure_rules": {"numeraire": "consumer_price_index"},
                "shocks": [{"name": "productivity_growth"}],
                "solver_result": {},
                "metrics": {
                    "gdp_impact": 1.0,
                    "household_welfare_impact": 0.5,
                    "government_revenue_impact": 0.2,
                },
                "report_path": str(root / "policy_report.md"),
                "learning_mode": "recommend",
            },
            store_path=root / "store.json",
            output_dir=root / "outputs",
            version_root=root / "versions",
            mode="recommend",
        )

        self.assertEqual(result["cycle"], list(LEARNING_STAGES))
        self.assertEqual(result["observe"]["run_id"], "cycle001")
        self.assertTrue(result["store"]["stored"])
        self.assertTrue(result["recommend"])
        self.assertTrue(result["validate"]["valid"])
        self.assertTrue(result["retest"]["passed"])
        self.assertTrue(result["remember"]["remembered"])
        self.assertTrue(Path(result["learning_report_path"]).exists())

    def test_safe_apply_blocks_non_low_risk_adaptation_before_implementation(self) -> None:
        root = Path(f"tests/_tmp/learning_cycle_{uuid.uuid4().hex}")
        result = run_learning_cycle(
            {
                "run_id": "cycle002",
                "status": "failed",
                "backend": "gams",
                "requested_backend": "gams",
                "model_name": "kenya_cge",
                "message": "",
                "validation": {
                    "valid": False,
                    "errors": ["Symbol output references unknown set sectors_missing"],
                    "warnings": [],
                    "sam_balanced": True,
                },
                "calibration": {"row_totals": {}, "account_classification": {}, "output_shares": {}, "total_activity": 0},
                "equations": [],
                "closure_rules": {},
                "shocks": [],
                "solver_result": {},
                "metrics": {},
                "learning_mode": "safe_apply",
            },
            store_path=root / "store.json",
            output_dir=root / "outputs",
            version_root=root / "versions",
            mode="safe_apply",
        )

        self.assertFalse(result["validate"]["valid"])
        self.assertEqual(result["implement"][0]["status"], "blocked")
        self.assertEqual(result["implement"][0]["validation_status"], "failed_pre_implementation_validation")


if __name__ == "__main__":
    unittest.main()
