import unittest
import uuid
from pathlib import Path

from signal_learning.implementation_engine import implement_adaptation, rollback_adaptation
from signal_learning.memory_schema import AdaptationProposal


class ImplementationEngineTests(unittest.TestCase):
    def test_recommend_mode_does_not_overwrite_core_templates(self) -> None:
        proposal = _proposal("v001", "medium")
        result = implement_adaptation(proposal, mode="recommend", version_root=Path(f"tests/_tmp/impl_{uuid.uuid4().hex}"))

        self.assertEqual(result.status, "suggested")
        self.assertEqual(result.validation_status, "requires_user_review")

    def test_safe_apply_creates_versioned_adapted_template(self) -> None:
        version_root = Path(f"tests/_tmp/impl_{uuid.uuid4().hex}")
        result = implement_adaptation(_proposal("v001", "low"), mode="safe_apply", version_root=version_root)

        self.assertEqual(result.status, "applied")
        self.assertTrue((version_root / "v001" / "adapted_rule.md").exists())
        self.assertIn("Core templates were not overwritten", (version_root / "v001" / "adapted_rule.md").read_text(encoding="utf-8"))

    def test_rollback_reports_missing_copy_clearly(self) -> None:
        result = rollback_adaptation("v999", version_root=Path(f"tests/_tmp/impl_{uuid.uuid4().hex}"))

        self.assertEqual(result.status, "blocked")
        self.assertIn("No rollback copy", result.message)


def _proposal(version_id: str, risk_level: str) -> AdaptationProposal:
    return AdaptationProposal(
        version_id=version_id,
        change_summary="Improve fallback guidance.",
        reason_for_change="Observed GAMS unavailable.",
        affected_templates_or_rules=["knowledge_base/solver_diagnostics.md"],
        confidence_score=0.9,
        risk_level=risk_level,  # type: ignore[arg-type]
        recommended_mode="safe_apply" if risk_level == "low" else "recommend",
        evidence_run_ids=["run001"],
        rollback_instructions="Remove adapted_rule.md.",
    )


if __name__ == "__main__":
    unittest.main()
